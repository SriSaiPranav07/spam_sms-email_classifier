import os
import json
import time
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Spam SMS & Email Classifier | AI Threat Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Cybersecurity Dashboard Styling (CSS)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Background and container overrides */
    .stApp {
        background-color: #0B1120;
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1E293B;
    }

    /* Clean spacing */
    .block-container {
        padding-top: 1.75rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Custom Header Card */
    .hero-card {
        background: linear-gradient(135deg, #172033 0%, #111827 100%);
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }

    .hero-header-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        color: #F8FAFC;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .hero-badge {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.35);
        padding: 0.2rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .hero-subtitle {
        color: #22D3EE;
        font-size: 1rem;
        font-weight: 500;
        margin: 0.2rem 0 0.5rem 0;
    }

    .hero-description {
        color: #94A3B8;
        font-size: 0.88rem;
        line-height: 1.5;
        margin: 0;
    }

    /* Card Containers */
    .cyber-card {
        background-color: #172033;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
    }

    .cyber-card-glow {
        background: linear-gradient(180deg, #172033 0%, #111827 100%);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.06);
    }

    /* Metric Box */
    .metric-box {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .metric-sub {
        color: #22D3EE;
        font-size: 0.72rem;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* Detection Result Styling */
    .result-card-spam {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(239, 68, 68, 0.04) 100%);
        border: 1.5px solid #EF4444;
        border-radius: 12px;
        padding: 1.35rem 1.6rem;
        margin-top: 1.25rem;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
    }

    .result-card-ham {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(34, 197, 94, 0.04) 100%);
        border: 1.5px solid #22C55E;
        border-radius: 12px;
        padding: 1.35rem 1.6rem;
        margin-top: 1.25rem;
        box-shadow: 0 4px 20px rgba(34, 197, 94, 0.15);
    }

    .result-title-spam {
        color: #EF4444;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.4rem;
    }

    .result-title-ham {
        color: #22C55E;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.4rem;
    }

    .result-explanation {
        color: #E2E8F0;
        font-size: 0.9rem;
        line-height: 1.55;
        margin-top: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 0.75rem;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 0.25rem;
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px 8px 0 0;
        background-color: transparent;
        color: #94A3B8;
        font-weight: 500;
        font-size: 0.92rem;
        padding: 0 1.25rem;
        border: none;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC;
        background-color: rgba(59, 130, 246, 0.05);
    }

    .stTabs [aria-selected="true"] {
        color: #3B82F6 !important;
        font-weight: 700 !important;
        border-bottom: 2.5px solid #3B82F6 !important;
        background-color: rgba(59, 130, 246, 0.08) !important;
    }

    /* Button Enhancements */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.18s ease;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: #FFFFFF;
        border: 1px solid #60A5FA;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.5);
        border-color: #93C5FD;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #172033;
        color: #F8FAFC;
        border: 1px solid #1E293B;
    }

    div.stButton > button[kind="secondary"]:hover {
        border-color: #3B82F6;
        background-color: #1E293B;
        color: #22D3EE;
    }

    /* Text Area Styling */
    div[data-baseweb="textarea"] {
        background-color: #111827 !important;
        border-radius: 8px !important;
        border: 1px solid #1E293B !important;
    }

    div[data-baseweb="textarea"]:focus-within {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 1px #3B82F6 !important;
    }

    textarea {
        color: #F8FAFC !important;
        background-color: #111827 !important;
        font-family: 'Inter', monospace, sans-serif !important;
        font-size: 0.92rem !important;
    }

    /* Sidebar Telemetry Pill */
    .telemetry-pill {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0.75rem;
        background-color: #172033;
        border: 1px solid #1E293B;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-size: 0.82rem;
    }

    .telemetry-label {
        color: #94A3B8;
    }

    .telemetry-val {
        color: #22C55E;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Data & Model Helpers
# -----------------------------------------------------------------------------
@st.cache_data
def get_metrics_data():
    """Load evaluation metrics from models/metrics.json or metrics.json."""
    candidates = ["models/metrics.json", "metrics.json"]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f), path
            except Exception:
                pass
    return None, None


@st.cache_resource
def load_trained_model(model_name: str):
    """Load cached model pipeline from disk."""
    model_path = "models/svm_model.pkl" if "SVM" in model_name else "models/nb_model.pkl"
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path), model_path
        except Exception as e:
            return None, str(e)
    return None, None


def classify_message(model, text: str):
    """
    Run prediction and extract calibrated confidence scores.
    Preserves exact mathematical model calibration without fabricating probabilities.
    """
    pred = model.predict([text])[0]
    classes = list(model.classes_)
    spam_idx = classes.index("spam") if "spam" in classes else 1
    ham_idx = classes.index("ham") if "ham" in classes else 0

    spam_prob = None
    ham_prob = None
    confidence = None

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([text])[0]
        spam_prob = float(probs[spam_idx])
        ham_prob = float(probs[ham_idx])
        confidence = spam_prob if pred == "spam" else ham_prob
    elif hasattr(model, "decision_function"):
        import scipy.special
        decision = model.decision_function([text])[0]
        prob_spam = float(scipy.special.expit(decision))
        spam_prob = prob_spam
        ham_prob = 1.0 - prob_spam
        confidence = spam_prob if pred == "spam" else ham_prob

    return pred, confidence, spam_prob, ham_prob


# -----------------------------------------------------------------------------
# Header / Hero Section
# -----------------------------------------------------------------------------
shield_svg = """
<svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2L3 6V12C3 17.52 6.84 22.74 12 24C17.16 22.74 21 17.52 21 12V6L12 2Z" fill="#172554" stroke="#3B82F6" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M9 12L11 14L15 9" stroke="#22D3EE" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-header-row">
            <div>{shield_svg}</div>
            <div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <h1 class="hero-title">Spam SMS & Email Classifier</h1>
                    <span class="hero-badge">Production v2.0</span>
                </div>
                <div class="hero-subtitle">AI-powered message threat detection</div>
            </div>
        </div>
        <p class="hero-description">
            Analyze incoming SMS and email messages in real time using dual trained NLP pipelines 
            (Linear SVM and Multinomial Naive Bayes) with calibrated probability outputs.
            Trained on the benchmark UCI SMS dataset for instant classification of unsolicited spam, phishing lures, and legitimate messages.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Sidebar Configuration & Telemetry
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ Threat Engine Controls")

    selected_model_choice = st.selectbox(
        "Active Classifier",
        [
            "Linear SVM (Calibrated)",
            "Multinomial Naive Bayes"
        ],
        index=0,
        help="Linear SVM delivers top overall recall (95.31%) & F1-score (92.78%). Naive Bayes offers 100% precision with 0 false positives."
    )

    st.markdown("---")
    st.markdown("#### System Diagnostics")

    svm_exists = os.path.exists("models/svm_model.pkl")
    nb_exists = os.path.exists("models/nb_model.pkl")
    metrics_data, metrics_source = get_metrics_data()

    st.markdown(
        f"""
        <div class="telemetry-pill">
            <span class="telemetry-label">Engine Status</span>
            <span class="telemetry-val">{"● Operational" if (svm_exists and nb_exists) else "⚠️ Attention"}</span>
        </div>
        <div class="telemetry-pill">
            <span class="telemetry-label">Linear SVM</span>
            <span style="color: {'#22C55E' if svm_exists else '#EF4444'}; font-weight:600;">
                {"Ready" if svm_exists else "Missing"}
            </span>
        </div>
        <div class="telemetry-pill">
            <span class="telemetry-label">Naive Bayes</span>
            <span style="color: {'#22C55E' if nb_exists else '#EF4444'}; font-weight:600;">
                {"Ready" if nb_exists else "Missing"}
            </span>
        </div>
        <div class="telemetry-pill">
            <span class="telemetry-label">Metrics Engine</span>
            <span style="color: {'#22C55E' if metrics_data else '#EF4444'}; font-weight:600;">
                {"Verified" if metrics_data else "Not Found"}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("#### Pipeline Architecture")
    st.caption("• Preprocessor: Lowercase & Regex Cleaning")
    st.caption("• Vectorizer: TF-IDF Bi-grams (1,2)")
    st.caption("• Calibration: CalibratedClassifierCV (5-Fold)")

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.78rem; color: #94A3B8;">
            <b>Repository:</b> <a href="https://github.com/SriSaiPranav07/spam_sms-email_classifier" target="_blank" style="color: #3B82F6; text-decoration: none;">GitHub</a><br>
            <b>Deployment:</b> <a href="https://spamsms-emailclassifier.streamlit.app" target="_blank" style="color: #22D3EE; text-decoration: none;">Streamlit Cloud</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# Main Navigation Tabs
# -----------------------------------------------------------------------------
tab_detector, tab_performance, tab_explorer, tab_about = st.tabs([
    "🛡️ Message Detector",
    "📊 Model Performance",
    "📁 Dataset Explorer",
    "ℹ️ About System"
])

# =============================================================================
# TAB 1: Message Detector
# =============================================================================
with tab_detector:
    col_input, col_sidebar_info = st.columns([7, 3])

    with col_input:
        st.markdown("### Message Inspection Console")

        # Session state management for sample inputs
        if "message_input" not in st.session_state:
            st.session_state["message_input"] = ""

        def set_sample_text(text: str):
            st.session_state["message_input"] = text

        # Sample quick select pills
        st.markdown(
            "<span style='color: #94A3B8; font-size: 0.85rem; font-weight: 500;'>Quick Test Samples:</span>",
            unsafe_allow_html=True
        )

        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            st.button(
                "🚨 Urgent Phishing",
                on_click=set_sample_text,
                args=("URGENT: Your bank account access has been suspended. Verify your identity immediately at https://auth-secure-ebank.com to unlock.",),
                use_container_width=True
            )
        with col_b2:
            st.button(
                "🎁 Prize Claim",
                on_click=set_sample_text,
                args=("Congratulations! You have been selected for a £1,000 Walmart Gift Card or iPhone 15. Call 0800-456-7890 now to claim your code.",),
                use_container_width=True
            )
        with col_b3:
            st.button(
                "💼 Work Sync",
                on_click=set_sample_text,
                args=("Hi Alex, let's reschedule our design review to Thursday 2 PM. Please review the updated Figma wireframes before we connect.",),
                use_container_width=True
            )
        with col_b4:
            st.button(
                "💬 Casual Chat",
                on_click=set_sample_text,
                args=("Hey, are we still meeting for dinner tonight at 7 PM? Let me know if you want me to pick you up on the way.",),
                use_container_width=True
            )

        # Message text area
        user_message = st.text_area(
            label="Message Content",
            value=st.session_state["message_input"],
            placeholder="Paste or type an SMS message or email text here to analyze threat signals...",
            height=140,
            key="user_text_input",
            help="Accepts any plain text message or email snippet for classification."
        )

        # Bottom action bar
        col_btn, col_stats, col_clear = st.columns([3, 5, 2])
        with col_btn:
            analyze_clicked = st.button("Analyze Message", type="primary", use_container_width=True)
        with col_stats:
            char_len = len(user_message.strip())
            word_count = len(user_message.strip().split()) if char_len > 0 else 0
            st.markdown(
                f"<div style='color: #94A3B8; font-size: 0.82rem; padding-top: 0.5rem;'>"
                f"Length: <b style='color:#F8FAFC;'>{char_len}</b> chars | "
                f"Tokens: <b style='color:#F8FAFC;'>{word_count}</b> words"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_clear:
            st.button("Clear Input", on_click=set_sample_text, args=("",), use_container_width=True)

    with col_sidebar_info:
        st.markdown("### Active Configuration")
        model, model_info = load_trained_model(selected_model_choice)

        is_svm = "SVM" in selected_model_choice
        model_badge_color = "#3B82F6" if is_svm else "#22D3EE"
        model_tag = "Recommended • Best F1 & Recall" if is_svm else "Conservative • Zero False Positives"

        st.markdown(
            f"""
            <div class="cyber-card">
                <div style="font-size: 0.78rem; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Engine Selected</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: {model_badge_color}; margin: 0.2rem 0;">{selected_model_choice}</div>
                <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.75rem;">{model_tag}</div>
                <div style="font-size: 0.82rem; color: #CBD5E1; border-top: 1px solid #1E293B; padding-top: 0.5rem;">
                    <b>Algorithm:</b> {"Linear Support Vector Machine (L2 loss)" if is_svm else "Multinomial Naive Bayes (Laplace α=1)"}<br>
                    <b>N-Gram Window:</b> (1, 2) Uni & Bi-grams<br>
                    <b>Probability Calibration:</b> Sigmoid (Platt Scaling)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------------------------------
    # Prediction Execution & Results Card
    # -------------------------------------------------------------------------
    if analyze_clicked:
        if not user_message.strip():
            st.warning("⚠️ Message cannot be empty. Please enter or select a message to analyze.")
        elif model is None:
            st.error(
                f"⚠️ Model file could not be loaded ({model_info}). "
                "Please run `python train_model.py` to train and serialize models."
            )
        else:
            with st.spinner("Analyzing message feature vectors and calculating threat confidence..."):
                time.sleep(0.18)  # Brief micro-delay for realistic interactive feel
                pred, confidence, spam_prob, ham_prob = classify_message(model, user_message)

            is_spam = (pred == "spam")

            if is_spam:
                conf_display = f"{confidence:.1%}" if confidence is not None else "High"
                spam_percent = f"{spam_prob:.1%}" if spam_prob is not None else "N/A"
                ham_percent = f"{ham_prob:.1%}" if ham_prob is not None else "N/A"

                st.markdown(
                    f"""
                    <div class="result-card-spam">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div class="result-title-spam">
                                <span>🚨</span> SPAM DETECTED
                            </div>
                            <span style="background-color: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">
                                High Threat Flagged
                            </span>
                        </div>
                        <div style="margin-top: 0.5rem; display: flex; gap: 2rem; flex-wrap: wrap;">
                            <div>
                                <span style="font-size: 0.78rem; color: #94A3B8;">Confidence Score:</span>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-left: 0.35rem;">{conf_display}</span>
                            </div>
                            <div>
                                <span style="font-size: 0.78rem; color: #94A3B8;">Spam Probability:</span>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #EF4444; margin-left: 0.35rem;">{spam_percent}</span>
                            </div>
                            <div>
                                <span style="font-size: 0.78rem; color: #94A3B8;">Legitimate Probability:</span>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #94A3B8; margin-left: 0.35rem;">{ham_percent}</span>
                            </div>
                        </div>
                        <div class="result-explanation">
                            <b>Detection Explanation:</b> The linguistic patterns and token distributions within this message 
                            strongly correlate with known promotional spam, coercive urgency, or phishing solicitations in the trained corpus. 
                            The calibrated statistical feature score exceeds the spam classification threshold.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                conf_display = f"{confidence:.1%}" if confidence is not None else "High"
                ham_percent = f"{ham_prob:.1%}" if ham_prob is not None else "N/A"
                spam_percent = f"{spam_prob:.1%}" if spam_prob is not None else "N/A"

                st.markdown(
                    f"""
                    <div class="result-card-ham">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div class="result-title-ham">
                                <span>✅</span> LEGITIMATE MESSAGE
                            </div>
                            <span style="background-color: rgba(34, 197, 94, 0.2); color: #22C55E; border: 1px solid #22C55E; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">
                                Clean / Normal Communication
                            </span>
                        </div>
                        <div style="margin-top: 0.5rem; display: flex; gap: 2rem; flex-wrap: wrap;">
                            <div>
                                <span style="font-size: 0.78rem; color: #94A3B8;">Confidence Score:</span>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-left: 0.35rem;">{conf_display}</span>
                            </div>
                            <div>
                                <span style="font-size: 0.78rem; color: #94A3B8;">Legitimate Probability:</span>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #22C55E; margin-left: 0.35rem;">{ham_percent}</span>
                            </div>
                            <div>
                                <span style="font-size: 0.78rem; color: #94A3B8;">Spam Probability:</span>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #94A3B8; margin-left: 0.35rem;">{spam_percent}</span>
                            </div>
                        </div>
                        <div class="result-explanation">
                            <b>Detection Explanation:</b> The lexical density and vocabulary align with standard human conversational 
                            or business syntax. The message lacks the high-density commercial trigger words or deceptive call-to-actions 
                            characteristic of malicious spam samples.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =============================================================================
# TAB 2: Model Performance & Benchmarks
# =============================================================================
with tab_performance:
    st.markdown("### Model Evaluation & Benchmarks")
    st.markdown(
        "<span style='color: #94A3B8; font-size: 0.9rem;'>"
        "Empirical performance measured on the held-out test split (20% of UCI SMS Spam Collection, 1,032 samples)."
        "</span>",
        unsafe_allow_html=True
    )

    metrics_data, metrics_file = get_metrics_data()

    if metrics_data is not None:
        nb_info = metrics_data.get("naive_bayes", {})
        svm_info = metrics_data.get("linear_svm", {})
        dataset_info = metrics_data.get("dataset_summary", {})

        # Top Executive KPI Cards
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)

        with col_k1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Production Accuracy</div>
                    <div class="metric-value" style="color: #3B82F6;">{svm_info.get('accuracy', 0):.2%}</div>
                    <div class="metric-sub">Linear SVM (Calibrated)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_k2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Spam Precision</div>
                    <div class="metric-value" style="color: #22D3EE;">{nb_info.get('precision', 0):.2%}</div>
                    <div class="metric-sub">Naive Bayes (Zero False Positives)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_k3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Spam Recall</div>
                    <div class="metric-value" style="color: #22C55E;">{svm_info.get('recall', 0):.2%}</div>
                    <div class="metric-sub">SVM Catches 95.3% of Spam</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_k4:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Production F1-Score</div>
                    <div class="metric-value" style="color: #F8FAFC;">{svm_info.get('f1', 0):.2%}</div>
                    <div class="metric-sub">Harmonic Precision-Recall Mean</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Side-by-side Model Metric Breakdown Cards
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        col_m_svm, col_m_nb = st.columns(2)

        with col_m_svm:
            st.markdown(
                """
                <div class="cyber-card-glow">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h4 style="margin: 0; color: #3B82F6;">Linear SVM (Calibrated)</h4>
                        <span style="background: rgba(59, 130, 246, 0.2); color: #60A5FA; border: 1px solid #3B82F6; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">RECOMMENDED</span>
                    </div>
                    <p style="color: #94A3B8; font-size: 0.82rem; margin-bottom: 1rem;">
                        Optimal balance between precision and threat recall. Identifies subtle phishing lures with calibrated confidence.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accuracy", f"{svm_info.get('accuracy', 0):.2%}")
            c2.metric("Precision", f"{svm_info.get('precision', 0):.2%}")
            c3.metric("Recall", f"{svm_info.get('recall', 0):.2%}")
            c4.metric("F1-Score", f"{svm_info.get('f1', 0):.2%}")

        with col_m_nb:
            st.markdown(
                """
                <div class="cyber-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h4 style="margin: 0; color: #22D3EE;">Multinomial Naive Bayes</h4>
                        <span style="background: rgba(34, 211, 238, 0.15); color: #22D3EE; border: 1px solid #22D3EE; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">BASELINE</span>
                    </div>
                    <p style="color: #94A3B8; font-size: 0.82rem; margin-bottom: 1rem;">
                        Ultra-conservative probabilistic classifier. Achieves 100% precision (0 legitimate messages incorrectly flagged).
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            n1, n2, n3, n4 = st.columns(4)
            n1.metric("Accuracy", f"{nb_info.get('accuracy', 0):.2%}")
            n2.metric("Precision", f"{nb_info.get('precision', 0):.2%}")
            n3.metric("Recall", f"{nb_info.get('recall', 0):.2%}")
            n4.metric("F1-Score", f"{nb_info.get('f1', 0):.2%}")

        # Model Comparison Chart
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        chart_metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
        svm_vals = [svm_info.get('accuracy', 0), svm_info.get('precision', 0), svm_info.get('recall', 0), svm_info.get('f1', 0)]
        nb_vals = [nb_info.get('accuracy', 0), nb_info.get('precision', 0), nb_info.get('recall', 0), nb_info.get('f1', 0)]

        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            name="Linear SVM (Calibrated)",
            x=chart_metrics,
            y=svm_vals,
            text=[f"{v:.1%}" for v in svm_vals],
            textposition="auto",
            marker=dict(color="#3B82F6", line=dict(color="#60A5FA", width=1))
        ))
        fig_compare.add_trace(go.Bar(
            name="Multinomial Naive Bayes",
            x=chart_metrics,
            y=nb_vals,
            text=[f"{v:.1%}" for v in nb_vals],
            textposition="auto",
            marker=dict(color="#22D3EE", line=dict(color="#67E8F9", width=1))
        ))
        fig_compare.update_layout(
            barmode="group",
            title=dict(text="Model Benchmark Metric Comparison (Held-out Test Split)", font=dict(size=14, color="#F8FAFC")),
            yaxis=dict(range=[0, 1.08], tickformat=".0%", gridcolor="#1E293B", color="#94A3B8"),
            xaxis=dict(gridcolor="#1E293B", color="#F8FAFC"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#F8FAFC")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC", family="Inter, sans-serif"),
            margin=dict(l=20, r=20, t=50, b=20),
            height=340
        )
        st.plotly_chart(fig_compare, use_container_width=True)

        # Confusion Matrices Section
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("### Test Set Confusion Matrices")

        def render_annotated_matrix(cm_data, model_title, accent_color):
            tn, fp = cm_data[0]
            fn, tp = cm_data[1]

            annotations = [
                [f"<b>{tn}</b><br><span style='font-size:10px;color:#94A3B8'>True Ham</span>",
                 f"<b>{fp}</b><br><span style='font-size:10px;color:#EF4444'>False Spam</span>"],
                [f"<b>{fn}</b><br><span style='font-size:10px;color:#EF4444'>Missed Spam</span>",
                 f"<b>{tp}</b><br><span style='font-size:10px;color:#22D3EE'>True Spam</span>"]
            ]

            fig = go.Figure(data=go.Heatmap(
                z=cm_data,
                x=["Predicted Ham", "Predicted Spam"],
                y=["Actual Ham", "Actual Spam"],
                colorscale=[[0, "#0B1120"], [0.3, "#111827"], [0.7, "#1E3A8A"], [1.0, accent_color]],
                showscale=False
            ))

            for r in range(2):
                for c in range(2):
                    fig.add_annotation(
                        x=c, y=r,
                        text=annotations[r][c],
                        showarrow=False,
                        font=dict(color="#F8FAFC", size=13)
                    )

            fig.update_layout(
                title=dict(text=model_title, font=dict(size=13, color="#F8FAFC")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC", family="Inter, sans-serif"),
                xaxis=dict(side="bottom", gridcolor="#1E293B", color="#94A3B8"),
                yaxis=dict(autorange="reversed", gridcolor="#1E293B", color="#94A3B8"),
                margin=dict(l=20, r=20, t=40, b=20),
                height=260
            )
            return fig

        col_cm1, col_cm2 = st.columns(2)
        svm_cm = svm_info.get("confusion_matrix")
        nb_cm = nb_info.get("confusion_matrix")

        if svm_cm:
            with col_cm1:
                st.plotly_chart(render_annotated_matrix(svm_cm, "Linear SVM Confusion Matrix (Test N=1,032)", "#3B82F6"), use_container_width=True)
        if nb_cm:
            with col_cm2:
                st.plotly_chart(render_annotated_matrix(nb_cm, "Naive Bayes Confusion Matrix (Test N=1,032)", "#22D3EE"), use_container_width=True)

        # Technical Engineering Insight
        st.markdown(
            """
            <div class="cyber-card">
                <h5 style="color: #F8FAFC; margin-bottom: 0.5rem;">Precision vs. Recall Architecture Trade-Off</h5>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                    In threat detection, a false negative (failing to detect phishing or malicious spam) exposes users to exploitation, 
                    while a false positive (flagging legitimate communication) causes friction. 
                    <b>Linear SVM achieves 95.31% recall</b>, catching 122 out of 128 spam messages on the test set while preserving 98.16% overall accuracy. 
                    Conversely, <b>Multinomial Naive Bayes achieves 100% precision</b> (0 false positives), but misses 35.94% of spam messages. 
                    For standard defense workloads, Calibrated Linear SVM is the optimal deployment candidate.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning(
            "⚠️ Verified evaluation metrics file (`metrics.json`) was not found. "
            "Run `python train_model.py` to evaluate pipelines on the dataset and generate benchmark files."
        )


# =============================================================================
# TAB 3: Dataset Explorer
# =============================================================================
with tab_explorer:
    st.markdown("### Corpus & Dataset Explorer")
    st.markdown(
        "<span style='color: #94A3B8; font-size: 0.9rem;'>"
        "Inspect the training distribution or upload custom CSV/TSV batches to inspect text structures and label balance."
        "</span>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Custom CSV or TSV Dataset",
        type=["csv", "tsv"],
        help="Upload a dataset containing message and label columns."
    )

    df_display = None
    source_label = ""

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".tsv"):
                df_display = pd.read_csv(uploaded_file, sep="\t", names=["label", "message"])
            else:
                df_display = pd.read_csv(uploaded_file)
            source_label = f"Uploaded File: `{uploaded_file.name}`"
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
    else:
        # Default fallback to bundled UCI dataset
        bundled_paths = ["data/spam.csv", "data/spam.tsv"]
        for p in bundled_paths:
            if os.path.exists(p):
                try:
                    df_display = pd.read_csv(p, encoding="latin-1")
                    # Clean standard UCI column artifacts if present
                    if "v1" in df_display.columns and "v2" in df_display.columns:
                        df_display = df_display[["v1", "v2"]].rename(columns={"v1": "label", "v2": "message"})
                    source_label = f"Bundled Benchmark: UCI SMS Spam Collection (`{p}`)"
                    break
                except Exception:
                    pass

    if df_display is not None and not df_display.empty:
        # Normalize columns if needed
        label_col = None
        for col in df_display.columns:
            if col.lower() in ["label", "target", "class", "v1"]:
                label_col = col
                break

        st.markdown(f"<span style='color: #22D3EE; font-size: 0.85rem; font-weight:600;'>{source_label}</span>", unsafe_allow_html=True)

        col_d1, col_d2, col_d3 = st.columns(3)
        total_records = len(df_display)
        col_d1.metric("Total Records", f"{total_records:,}")

        if label_col:
            val_dict = val_counts.to_dict()
            ham_ct = val_dict.get("ham", val_dict.get(0, "N/A"))
            spam_ct = val_dict.get("spam", val_dict.get(1, "N/A"))
            col_d2.metric("Legitimate (Ham)", f"{ham_ct:,}" if isinstance(ham_ct, int) else str(ham_ct))
            col_d3.metric("Spam Messages", f"{spam_ct:,}" if isinstance(spam_ct, int) else str(spam_ct))

            # Distribution chart and sample table
            col_table, col_chart = st.columns([6, 4])
            with col_table:
                st.markdown("#### Message Samples")
                st.dataframe(df_display.head(10), use_container_width=True, height=280)

            with col_chart:
                st.markdown("#### Label Distribution")
                pie_fig = go.Figure(data=[go.Pie(
                    labels=val_counts.index.map(lambda x: "Ham (Safe)" if str(x).lower() == "ham" else "Spam (Threat)" if str(x).lower() == "spam" else str(x)),
                    values=val_counts.values,
                    hole=0.55,
                    marker=dict(colors=["#3B82F6", "#EF4444"], line=dict(color="#111827", width=2)),
                    textinfo="label+percent",
                    textfont=dict(color="#F8FAFC", size=12)
                )])
                pie_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#F8FAFC", family="Inter, sans-serif"),
                    legend=dict(font=dict(color="#F8FAFC"), orientation="h", yanchor="bottom", y=-0.2),
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280
                )
                st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.dataframe(df_display.head(15), use_container_width=True)

    else:
        st.info("No dataset is loaded. Upload a CSV/TSV above or ensure `data/spam.csv` is present in the workspace.")


# =============================================================================
# TAB 4: About System & Architecture
# =============================================================================
with tab_about:
    st.markdown("### System Architecture & Technical Specifications")

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown(
            """
            <div class="cyber-card">
                <h4 style="color: #3B82F6; margin-bottom: 0.75rem;">End-to-End Threat Pipeline</h4>
                <div style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                    <b>1. Ingestion:</b> Message input via interactive web interface or API pipeline.<br>
                    <b>2. Preprocessing:</b> Token cleaning, lowercase conversion, and punctuation parsing.<br>
                    <b>3. TF-IDF Representation:</b> Term Frequency-Inverse Document Frequency matrix with uni-gram and bi-gram token combinations (ngram_range=(1,2)). English stop words filtered.<br>
                    <b>4. Classification:</b> Dual-engine support via calibrated Linear Support Vector Classification or Multinomial Naive Bayes.<br>
                    <b>5. Probability Calibration:</b> 5-fold cross-validated Platt scaling (sigmoid) to yield reliable posterior class confidence probabilities.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_a2:
        st.markdown(
            """
            <div class="cyber-card">
                <h4 style="color: #22D3EE; margin-bottom: 0.75rem;">Model Specifications</h4>
                <div style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                    <b>Production Engine:</b> <code>LinearSVC</code> with <code>CalibratedClassifierCV(cv=5)</code><br>
                    <b>Optimization:</b> Balanced class weighting to counter high class imbalance (87.5% Ham vs 12.5% Spam).<br>
                    <b>Baseline Engine:</b> <code>MultinomialNB(alpha=1.0)</code> for rapid Laplace-smoothed conditional probability estimates.<br>
                    <b>Dataset Benchmark:</b> UCI SMS Spam Collection (5,158 cleaned samples, 80/20 stratified split).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    col_limitations, col_tech = st.columns(2)

    with col_limitations:
        st.markdown(
            """
            <div class="cyber-card">
                <h4 style="color: #F8FAFC; margin-bottom: 0.75rem;">Limitations & Operational Boundary</h4>
                <div style="color: #94A3B8; font-size: 0.85rem; line-height: 1.55;">
                    • <b>Domain Shift:</b> The core weights were trained on SMS messages. While email plain text can be classified, email headers, HTML structures, and multi-paragraph corporate emails have not been specifically fine-tuned.<br>
                    • <b>Adversarial Evasions:</b> Character substitutions (leetspeak, zero-width characters) and homoglyph attacks may evade standard n-gram tokenization.<br>
                    • <b>Concept Drift:</b> Phishing lures evolve constantly; continual retraining with recent threat telemetry is advised for enterprise environments.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_tech:
        st.markdown(
            """
            <div class="cyber-card">
                <h4 style="color: #F8FAFC; margin-bottom: 0.75rem;">Technology Stack</h4>
                <div style="color: #94A3B8; font-size: 0.85rem; line-height: 1.55;">
                    • <b>Core Language:</b> Python 3.11<br>
                    • <b>Web Framework:</b> Streamlit 1.35+<br>
                    • <b>Machine Learning:</b> Scikit-Learn (TF-IDF, LinearSVC, MultinomialNB, CalibratedClassifierCV)<br>
                    • <b>Data & Visualization:</b> Pandas, Plotly Express & Graph Objects<br>
                    • <b>Serialization:</b> Joblib
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
