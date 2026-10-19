from src.model_utils import (
    build_nb_pipeline,
    build_svm_pipeline
)


def test_nb_pipeline():

    model = build_nb_pipeline()

    assert model is not None


def test_svm_pipeline():

    model = build_svm_pipeline()

    assert model is not None
