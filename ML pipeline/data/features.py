import pandas as pd
from sklearn.preprocessing import LabelEncoder


def prepare_features(input_csv="data/raw/candidates.csv"):
    df = pd.read_csv(input_csv)

    df.dropna(subset=["age", "experience_years", "salary_expectation"], inplace=True)

    df["profession"].fillna("Unknown", inplace=True)
    df["city"].fillna("Unknown", inplace=True)
    df["education_level"].fillna("Unknown", inplace=True)

    # Кодируем категориальные признаки
    for col in ["profession", "city", "education_level"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    feature_cols = [
        "age", "experience_years", "salary_expectation",
        "profession", "city", "education_level",
        "num_prev_jobs", "num_interviews"
    ]
    X = df[feature_cols]
    y = df["was_hired"]

    X.to_csv("data/processed/features.csv", index=False)
    y.to_csv("data/processed/target.csv", index=False)
    print("✅ Features prepared with smart handling and saved.")
    return X, y


if __name__ == "__main__":
    prepare_features()