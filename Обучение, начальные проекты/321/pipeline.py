from datetime import datetime
import pandas as pd
import numpy as np
import dill

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


def main():
    df = pd.read_csv('data/Homework.csv')
    droped = Pipeline(steps=[
        ('filter', FunctionTransformer(lambda df: df.drop([
            'id', 'url', 'region', 'region_url', 'price', 'manufacturer',
            'image_url', 'description', 'posting_date', 'lat', 'long'
        ], axis=1)))
    ])
    df = droped.fit_transform(df)

    def smooth_outliers(df):
        def calculate_boundaries(data):
            q25 = data.quantile(0.25)
            q75 = data.quantile(0.75)
            iqr = q75 - q25
            boundaries = (q25 - 1.5 * iqr, q75 + 1.5 * iqr)
            return boundaries

        boundaries = calculate_boundaries(df['year'])
        df['year'] = np.clip(df['year'], boundaries[0], boundaries[1])
        return df

    filters = Pipeline(steps=[
        ('smooth_outliers', FunctionTransformer(smooth_outliers))
    ])

    age_category = Pipeline(steps=[
        ('create_age_category', FunctionTransformer(lambda df: df.assign(age_category=pd.cut(df['year'], bins=[0, 1990, 2000, 2010, 2020, np.inf], labels=[1, 2, 3, 4, 5]))))
    ])

    X = df.drop(['price_category'], axis=1)
    y = df['price_category']

    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('numerical', numerical_transformer, numerical_features),
        ("categorical", categorical_transformer, categorical_features)
    ])

    best_score = 0
    best_pipe = None
    models = (
        LogisticRegression(solver='liblinear'),
        RandomForestClassifier(),
        MLPClassifier(activation='logistic', hidden_layer_sizes=(128, 64),  max_iter=500 , tol=1e-3)
    )

    for model in models:
        pipe = Pipeline(steps=[
            ('filter', filters),
            ('age_category', age_category),
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        score = cross_val_score(pipe, X, y, cv= 4, scoring='accuracy')
        print(f'model: {type(model).__name__}, acc_mean: {score.mean():.4f}, acc_std: {score.std():.4f}')

        if score.mean() > best_score:
            best_score = score.mean()
            best_pipe = pipe

    best_pipe.fit(X, y)
    print(f'Best model: {type(best_pipe.named_steps["classifier"]).__name__}, acc_mean: {best_score:.4f}')
    with open('Homework_pipe.plk', 'wb') as file:
        dill.dump({
            'model':best_pipe,
            'metadata': {
                'name': 'prediction_model',
                'autor': 'Islam Yasoveev',
                'version': 1.0,
                'date': datetime.now(),
                'type': type(best_pipe.named_steps['classifier']).__name__,
                'accuracy': best_score
            }
        }, file)


if __name__ == '__main__':
    main()
