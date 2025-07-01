import pandas as pd
from catboost import CatBoostClassifier


def run_inference(new_data_csv="data/processed/features.csv"):
    X_new = pd.read_csv(new_data_csv)

    model = CatBoostClassifier()
    model.load_model("models/model.cbm")

    predictions = model.predict_proba(X_new)[:, 1]
    X_new["score"] = predictions

    X_new.to_csv("data/processed/scored_candidates.csv", index=False)
    print("✅ Inference completed. Scores saved to scored_candidates.csv")
    return X_new


if __name__ == "__main__":
    run_inference()
