import os
import json
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SpamShield AI")

st.info(
    "Model trained on UCI SMS Spam Collection. "
    "Email text testing is supported but email-specific accuracy has not been validated."
)

MENU = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Model Evaluation",
        "Dataset Explorer",
        "About"
    ]
)


def get_metrics_data():
    """Load evaluation metrics from metrics.json or models/metrics.json."""
    candidates = ["models/metrics.json", "metrics.json"]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f), path
            except Exception:
                pass
    return None, None


if MENU == "Home":

    st.header("Live Spam Detector")

    model_choice = st.selectbox(
        "Select Model",
        [
            "Naive Bayes",
            "Linear SVM"
        ]
    )

    model_path = "models/nb_model.pkl" if model_choice == "Naive Bayes" else "models/svm_model.pkl"
    model = None

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
        except Exception as e:
            st.error(f"Error loading model from {model_path}: {e}")
    else:
        st.warning(
            f"⚠️ Model file '{model_path}' not found. "
            "Please run `python train_model.py` to train and serialize the models."
        )

    # Allow sample text selection
    sample_text = ""
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("Use Spam Sample"):
            st.session_state["message_input"] = "Congratulations! You won a free iPhone. Click now to claim."
    with col_s2:
        if st.button("Use Ham Sample"):
            st.session_state["message_input"] = "Hi Rahul, meeting moved to 3 PM today."

    current_val = st.session_state.get("message_input", "")
    message = st.text_area(
        "Enter SMS or Email Text",
        value=current_val,
        height=130
    )

    if st.button("Analyze Message", type="primary"):

        if not message.strip():
            st.error("Message cannot be empty")
        elif model is None:
            st.error("Model is not loaded. Train the models first using `python train_model.py`.")
        else:
            prediction = model.predict([message])[0]

            confidence = 0.0
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba([message])[0]
                confidence = float(probs.max())
            elif hasattr(model, "decision_function"):
                decision = model.decision_function([message])[0]
                import scipy.special
                prob_spam = scipy.special.expit(decision)
                confidence = float(max(prob_spam, 1 - prob_spam))
            else:
                confidence = 1.0

            if prediction == "spam":
                st.error(
                    f"🚨 **SPAM DETECTED**\n\n"
                    f"**Confidence:** {confidence:.2%}\n\n"
                    f"**Model:** {model_choice}"
                )
            else:
                st.success(
                    f"✅ **NOT SPAM (HAM)**\n\n"
                    f"**Confidence:** {confidence:.2%}\n\n"
                    f"**Model:** {model_choice}"
                )

    st.markdown("---")
    st.subheader("Sample Messages")

    st.code("Congratulations! You won a free iPhone. Click now.")
    st.code("Hi Rahul, meeting moved to 3 PM today.")


elif MENU == "Model Evaluation":

    st.header("📊 Model Evaluation & Benchmarks")

    metrics_data, metrics_file = get_metrics_data()

    if metrics_data is not None:
        st.success(f"Loaded verified evaluation metrics from `{metrics_file}`")

        # Extract data
        nb_info = metrics_data.get("naive_bayes", {})
        svm_info = metrics_data.get("linear_svm", {})
        dataset_info = metrics_data.get("dataset_summary", {})

        # Dataset summary expander / banner
        if dataset_info:
            d_col1, d_col2, d_col3, d_col4 = st.columns(4)
            d_col1.metric("Total Cleaned Samples", dataset_info.get("total_samples", "N/A"))
            d_col2.metric("Training Samples (80%)", dataset_info.get("train_samples", "N/A"))
            d_col3.metric("Test Samples (20%)", dataset_info.get("test_samples", "N/A"))
            d_col4.metric(
                "Ham / Spam Split",
                f"{dataset_info.get('ham_count', 'N/A')} / {dataset_info.get('spam_count', 'N/A')}"
            )

        st.markdown("### Metric Comparison")
        col_nb, col_svm = st.columns(2)

        with col_nb:
            st.subheader("Multinomial Naive Bayes")
            m1, m2 = st.columns(2)
            m1.metric("Accuracy", f"{nb_info.get('accuracy', 0):.2%}")
            m2.metric("Precision", f"{nb_info.get('precision', 0):.2%}")
            m3, m4 = st.columns(2)
            m3.metric("Recall", f"{nb_info.get('recall', 0):.2%}")
            m4.metric("F1-Score", f"{nb_info.get('f1', 0):.2%}")

        with col_svm:
            st.subheader("Linear SVM (Calibrated)")
            s1, s2 = st.columns(2)
            s1.metric("Accuracy", f"{svm_info.get('accuracy', 0):.2%}")
            s2.metric("Precision", f"{svm_info.get('precision', 0):.2%}")
            s3, s4 = st.columns(2)
            s3.metric("Recall", f"{svm_info.get('recall', 0):.2%}")
            s4.metric("F1-Score", f"{svm_info.get('f1', 0):.2%}")

        # Comparison Chart
        st.markdown("### Performance Overview")
        chart_df = pd.DataFrame([
            {
                "Model": "Naive Bayes",
                "Accuracy": nb_info.get("accuracy", 0),
                "Precision": nb_info.get("precision", 0),
                "Recall": nb_info.get("recall", 0),
                "F1-Score": nb_info.get("f1", 0)
            },
            {
                "Model": "Linear SVM",
                "Accuracy": svm_info.get("accuracy", 0),
                "Precision": svm_info.get("precision", 0),
                "Recall": svm_info.get("recall", 0),
                "F1-Score": svm_info.get("f1", 0)
            }
        ])

        chart_melted = chart_df.melt(
            id_vars=["Model"],
            value_vars=["Accuracy", "Precision", "Recall", "F1-Score"],
            var_name="Metric",
            value_name="Score"
        )

        fig_bar = px.bar(
            chart_melted,
            x="Metric",
            y="Score",
            color="Model",
            barmode="group",
            text_auto=".2%",
            title="Model Evaluation Metrics Comparison",
            color_discrete_sequence=["#00E5FF", "#A78BFA"]
        )
        fig_bar.update_layout(yaxis=dict(range=[0, 1.05]))
        st.plotly_chart(fig_bar, use_container_width=True)

        # Confusion Matrices
        st.markdown("### Confusion Matrices (Test Set)")
        cm_col1, cm_col2 = st.columns(2)

        nb_cm = nb_info.get("confusion_matrix")
        svm_cm = svm_info.get("confusion_matrix")

        if nb_cm:
            with cm_col1:
                st.write("**Naive Bayes Confusion Matrix**")
                fig_nb = px.imshow(
                    nb_cm,
                    text_auto=True,
                    labels=dict(x="Predicted Label", y="Actual Label", color="Count"),
                    x=["Ham", "Spam"],
                    y=["Ham", "Spam"],
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(fig_nb, use_container_width=True)

        if svm_cm:
            with cm_col2:
                st.write("**Linear SVM Confusion Matrix**")
                fig_svm = px.imshow(
                    svm_cm,
                    text_auto=True,
                    labels=dict(x="Predicted Label", y="Actual Label", color="Count"),
                    x=["Ham", "Spam"],
                    y=["Ham", "Spam"],
                    color_continuous_scale="Purples"
                )
                st.plotly_chart(fig_svm, use_container_width=True)

    else:
        st.warning(
            "Evaluation metrics have not been generated yet. "
            "Please run `python train_model.py` to train models and save actual results to `metrics.json`."
        )


elif MENU == "Dataset Explorer":

    st.header("Dataset Explorer")

    uploaded = st.file_uploader(
        "Upload Dataset",
        type=["csv", "tsv"]
    )

    if uploaded is not None:

        if uploaded.name.endswith(".tsv"):
            df = pd.read_csv(
                uploaded,
                sep="\t",
                names=["label", "message"]
            )
        else:
            df = pd.read_csv(uploaded)

        st.dataframe(df.head())

        st.write(
            f"Total Records: {len(df)}"
        )

        counts = df.iloc[:, 0].value_counts()

        fig = px.pie(
            values=counts.values,
            names=counts.index,
            title="Class Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


elif MENU == "About":

    st.header("About")

    st.markdown("""
### Problem Statement

Detect spam SMS messages using NLP and Machine Learning.

### Models

- Multinomial Naive Bayes
- Linear SVM

### Workflow

Dataset → Cleaning → TF-IDF →
Training → Evaluation → Prediction

### Dataset

UCI SMS Spam Collection

https://archive.ics.uci.edu/dataset/228/sms+spam+collection

### Technologies

- Python
- Streamlit
- Scikit-learn
- Plotly

### Future Improvements

- Email spam dataset support
- Deep learning models
- Explainable AI
""")
