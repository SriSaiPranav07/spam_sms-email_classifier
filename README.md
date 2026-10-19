# SpamShield AI

## Overview

Spam SMS and Email Classifier built using Machine Learning and Streamlit.

## Features

- TF-IDF Features
- Multinomial Naive Bayes
- Linear SVM
- Spam Detection
- Confidence Scores
- Interactive Dashboard

## Dataset

UCI SMS Spam Collection

https://archive.ics.uci.edu/dataset/228/sms+spam+collection

## Installation

```bash
pip install -r requirements.txt
```

## Training

```bash
python train_model.py
```

## Run App

```bash
streamlit run app.py
```

## Metrics

Actual measured metrics generated from training on the UCI SMS Spam Collection:

| Model | Accuracy | Precision (Spam) | Recall (Spam) | F1-Score (Spam) |
|---|---|---|---|---|
| **Multinomial Naive Bayes** | 95.54% | 100.00% | 64.06% | 78.10% |
| **Linear SVM (Calibrated)** | 98.16% | 90.37% | 95.31% | 92.78% |

*Metrics are automatically evaluated and saved to `metrics.json` and `models/metrics.json` during training (`python train_model.py`), and loaded dynamically in the Streamlit Evaluation page.*

## Streamlit Deployment

1. Push to GitHub
2. Open https://share.streamlit.io
3. Select repository
4. Choose `app.py`
5. Deploy

## Screenshots

Add:
- Home Page
- Evaluation Page
- Dataset Explorer
- Prediction Result

## Limitations

Model trained on SMS messages.
Email performance is not independently validated.

## Future Work

- BERT
- Email datasets
- Explainable AI
