import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score
import json


def train_model():
    X = pd.read_csv("data/processed/features.csv")
    y = pd.read_csv("data/processed/target.csv")

    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.1,
        depth=6,
        verbose=False
    )

    model.fit(X, y)

    y_pred = model.predict_proba(X)[:, 1]
    roc_auc = roc_auc_score(y, y_pred)

    print(f"Модель обучилась. ROC-AUC: {roc_auc:.4f}")

    model.save_model("models/model.cbm")

    metrics = {"roc_auc": roc_auc}
    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f)

    return model


if __name__ == "__main__":
    train_model()