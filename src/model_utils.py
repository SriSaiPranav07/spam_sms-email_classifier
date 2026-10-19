from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def build_nb_pipeline():

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2)
            )
        ),
        (
            "classifier",
            MultinomialNB()
        )
    ])


def build_svm_pipeline():

    svm = LinearSVC(
        class_weight="balanced",
        random_state=42
    )

    calibrated = CalibratedClassifierCV(
        svm,
        cv=5
    )

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2)
            )
        ),
        (
            "classifier",
            calibrated
        )
    ])


def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=["ham", "spam"]
    )

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(
            y_test,
            predictions,
            pos_label="spam"
        )),
        "recall": float(recall_score(
            y_test,
            predictions,
            pos_label="spam"
        )),
        "f1": float(f1_score(
            y_test,
            predictions,
            pos_label="spam"
        )),
        "confusion_matrix": cm.tolist() if hasattr(cm, "tolist") else cm
    }

    return metrics
