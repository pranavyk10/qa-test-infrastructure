"""
Model Monitoring Dashboard — run with: streamlit run phase4_ai_ml/monitor_dashboard.py
Flags when F1-Score drops below safety threshold.
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split

F1_THRESHOLD = 0.80

st.set_page_config(page_title="ML Model Monitor", layout="wide")
st.title("🤖 Model Monitoring Dashboard")
st.caption("Flags data drift and performance degradation in real time.")

# --- Simulate Training Data (Age 20–30) ---
np.random.seed(42)
X_train, y_train = make_classification(n_samples=1000, n_features=5, random_state=42)
X_train[:, 0] = np.random.uniform(20, 30, 1000)  # Feature 0 = Age

model = LogisticRegression()
model.fit(X_train, y_train)

# --- Simulate Production Data (Age 50–60 = DATA DRIFT) ---
drift_slider = st.slider("Simulated Data Drift (0 = No Drift, 1 = Full Drift)", 0.0, 1.0, 0.0, 0.1)

X_test, y_test = make_classification(n_samples=300, n_features=5, random_state=99)
X_test[:, 0] = np.random.uniform(
    20 + drift_slider * 30,
    30 + drift_slider * 30,
    300
)

y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred, average="weighted")

col1, col2, col3 = st.columns(3)
col1.metric("F1 Score", f"{f1:.3f}", delta=f"{f1 - F1_THRESHOLD:.3f} vs threshold")
col2.metric("Safety Threshold", f"{F1_THRESHOLD}")
col3.metric("Drift Level", f"{drift_slider * 100:.0f}%")

if f1 < F1_THRESHOLD:
    st.error(f"🚨 ALERT: F1 Score {f1:.3f} is BELOW the safety threshold of {F1_THRESHOLD}!")
else:
    st.success(f"✅ Model is HEALTHY. F1 Score {f1:.3f} is above threshold.")

# --- Distribution Drift Visualization ---
st.subheader("Input Feature Distribution (Age)")
train_ages = pd.DataFrame({"Age": X_train[:, 0], "Dataset": "Training"})
test_ages = pd.DataFrame({"Age": X_test[:, 0], "Dataset": "Production"})
combined = pd.concat([train_ages, test_ages])
st.bar_chart(combined.groupby(["Dataset", pd.cut(combined["Age"], bins=10)]).size().unstack(0))

# --- Adversarial / Prompt Injection Test Section ---
st.subheader("🛡️ Adversarial & Edge Case Tests")
prompt = st.text_input("Test Prompt Injection (for LLM features):", placeholder="Ignore previous instructions and...")
if prompt:
    injection_keywords = ["ignore", "forget", "pretend", "override", "system"]
    is_injection = any(kw in prompt.lower() for kw in injection_keywords)
    if is_injection:
        st.warning(f"⚠️ Potential Prompt Injection Detected: `{prompt}`")
    else:
        st.info("Input appears safe.")
