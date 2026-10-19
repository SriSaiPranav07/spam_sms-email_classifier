import os
import json
import joblib

from sklearn.model_selection import train_test_split

from src.data_loader import load_dataset
from src.model_utils import (
    build_nb_pipeline,
    build_svm_pipeline,
    evaluate_model
)

DATASET_PATH = "data/spam.csv"

os.makedirs("models", exist_ok=True)


def save_metrics(nb_metrics, svm_metrics, df, X_train, X_test):
    """
    Save evaluation metrics to metrics.json for inspection and Streamlit display.
    """
    metrics_data = {
        "naive_bayes": {
            "name": "Multinomial Naive Bayes",
            "accuracy": round(float(nb_metrics["accuracy"]), 4),
            "precision": round(float(nb_metrics["precision"]), 4),
            "recall": round(float(nb_metrics["recall"]), 4),
            "f1": round(float(nb_metrics["f1"]), 4),
            "confusion_matrix": nb_metrics["confusion_matrix"]
        },
        "linear_svm": {
            "name": "Linear SVM (Calibrated)",
            "accuracy": round(float(svm_metrics["accuracy"]), 4),
            "precision": round(float(svm_metrics["precision"]), 4),
            "recall": round(float(svm_metrics["recall"]), 4),
            "f1": round(float(svm_metrics["f1"]), 4),
            "confusion_matrix": svm_metrics["confusion_matrix"]
        },
        "dataset_summary": {
            "total_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "ham_count": int((df["label"] == "ham").sum()),
            "spam_count": int((df["label"] == "spam").sum())
        }
    }

    # Save to both models/metrics.json and root metrics.json
    metrics_destinations = ["models/metrics.json", "metrics.json"]
    for dest in metrics_destinations:
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=4)

    print("Metrics successfully saved to models/metrics.json and metrics.json")


def main():

    if not os.path.exists(DATASET_PATH):
        # Fallback to alternate dataset paths if present
        alternate_paths = ["data/spam.tsv", "data/SMSSpamCollection.txt", "data/SMSSpamCollection"]
        found_path = None
        for alt in alternate_paths:
            if os.path.exists(alt):
                found_path = alt
                break

        if found_path:
            print(f"Loading dataset from alternate path: {found_path}")
            df = load_dataset(found_path)
        else:
            raise FileNotFoundError(
                f"Dataset not found at '{DATASET_PATH}'. "
                "Please place the UCI SMS Spam dataset at 'data/spam.csv' or 'data/spam.tsv'."
            )
    else:
        df = load_dataset(DATASET_PATH)

    print(f"Loaded {len(df)} cleaned records ({sum(df['label'] == 'ham')} ham, {sum(df['label'] == 'spam')} spam)")

    X_train, X_test, y_train, y_test = train_test_split(
        df["message"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    nb_model = build_nb_pipeline()
    svm_model = build_svm_pipeline()

    print("Training NB...")
    nb_model.fit(X_train, y_train)

    print("Training SVM...")
    svm_model.fit(X_train, y_train)

    nb_metrics = evaluate_model(
        nb_model,
        X_test,
        y_test
    )

    svm_metrics = evaluate_model(
        svm_model,
        X_test,
        y_test
    )

    print("\nNB Metrics:")
    print(nb_metrics)

    print("\nSVM Metrics:")
    print(svm_metrics)

    joblib.dump(
        nb_model,
        "models/nb_model.pkl"
    )

    joblib.dump(
        svm_model,
        "models/svm_model.pkl"
    )

    print("Models Saved to models/")

    # Save evaluation metrics for Zelvora submission enhancement
    save_metrics(nb_metrics, svm_metrics, df, X_train, X_test)


if __name__ == "__main__":
    main()
