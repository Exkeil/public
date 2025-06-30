import logging
import os
from datetime import datetime

import dill
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from sklearn.svm import SVC

# Укажем путь к файлам проекта:
path = os.environ.get('my_project_path', '.')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет ненужные столбцы."""
    columns_to_drop = [
        'id', 'url', 'region', 'region_url', 'price', 'manufacturer',
        'image_url', 'description', 'posting_date', 'lat', 'long'
    ]
    return df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет выбросы по полю 'year'."""
    df = df.copy()
    if 'year' in df.columns:
        q25, q75 = df['year'].quantile([0.25, 0.75])
        iqr = q75 - q25
        lower, upper = q25 - 1.5 * iqr, q75 + 1.5 * iqr
        df['year'] = np.clip(df['year'], lower, upper)  # Обрезаем значения по границам
    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Создаёт новые признаки."""
    df = df.copy()

    if 'model' in df.columns:
        df['short_model'] = df['model'].fillna('unknown').str.lower().str.split().str[0]

    if 'year' in df.columns:
        df['age_category'] = df['year'].apply(lambda x: 'new' if x > 2013 else ('old' if x < 2006 else 'average'))

    return df


def pipeline() -> None:
    """Основной конвейер обработки данных и обучения модели."""
    df = pd.read_csv(os.path.join(path, 'data', 'train', 'homework.csv'))

    X = df.drop(columns=['price_category'], errors='ignore')
    y = df['price_category']

    # Проверка размеров перед обработкой
    logging.info(f"Размеры до обработки: X={X.shape}, y={y.shape}")

    # Предобработка
    preprocessor = Pipeline(steps=[
        ('filter', FunctionTransformer(filter_data)),
        ('outlier_remover', FunctionTransformer(remove_outliers)),
        ('feature_creator', FunctionTransformer(create_features))
    ])

    X_transformed = preprocessor.fit_transform(X)

    # Приводим `y` в соответствие с `X_transformed`
    if isinstance(X_transformed, np.ndarray):
        X_transformed = pd.DataFrame(X_transformed, index=X.index)

    y = y.loc[X_transformed.index]  # Синхронизируем X и y

    # Проверка размеров после обработки
    logging.info(f"Размеры после обработки: X={X_transformed.shape}, y={y.shape}")

    # Определяем числовые и категориальные признаки
    numerical_features = make_column_selector(dtype_include=['int64', 'float64'])
    categorical_features = make_column_selector(dtype_include=object)

    # Трансформеры
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    column_transformer = ColumnTransformer(transformers=[
        ('numerical', numerical_transformer, numerical_features),
        ('categorical', categorical_transformer, categorical_features)
    ])

    # Финальная обработка данных
    full_preprocessor = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('column_transformer', column_transformer)
    ])

    # Определяем модели
    models = [
        LogisticRegression(solver='liblinear', class_weight='balanced'),
        RandomForestClassifier(n_estimators=200, random_state=42),
        SVC(class_weight='balanced', probability=True),
        GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
    ]

    best_score = .0
    best_pipe = None

    for model in models:
        pipe = Pipeline([
            ('full_preprocessor', full_preprocessor),
            ('classifier', model)
        ])

        # Кросс-валидация
        score = cross_val_score(pipe, X, y, cv=4, scoring='accuracy')
        mean_score = score.mean()
        logging.info(f"Модель: {type(model).__name__}, Accuracy: {mean_score:.4f} (+/- {score.std():.4f})")

        if mean_score > best_score:
            best_score = mean_score
            best_pipe = pipe

    # Вывод лучшей модели
    logging.info(f"Лучшая модель: {type(best_pipe.named_steps['classifier']).__name__}, Accuracy: {best_score:.4f}")

    # Обучаем лучшую модель
    best_pipe.fit(X, y)

    # Сохраняем модель
    model_filename = f'{path}/data/models/cars_pipe_{datetime.now().strftime("%Y%m%d%H%M")}.pkl'
    with open(model_filename, 'wb') as file:
        dill.dump(best_pipe, file)

    logging.info(f"Модель сохранена: {model_filename}")


if __name__ == '__main__':
    pipeline()
