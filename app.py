import numpy as np
import pickle
import streamlit as st
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0a2540;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
}
.sub-title {
    font-size: 18px;
    color: #b9c3cf;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}
.predict-btn button {
    background: #635bff;
    color: white;
    font-size: 18px;
    border-radius: 12px;
    padding: 10px 24px;
}
.result-good {
    background: #e6f7ee;
    color: #0f5132;
    padding: 15px;
    border-radius: 12px;
    font-size: 20px;
}
.result-bad {
    background: #fdecea;
    color: #842029;
    padding: 15px;
    border-radius: 12px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD MODEL ----------
model_path = os.path.join(os.path.dirname(__file__), "trained_model.sav")

if not os.path.exists(model_path):
    st.error("❌ Model file not found: trained_model.sav")
    st.stop()

with open(model_path, "rb") as f:
    model = pickle.load(f)

# ---------- PREDICTION FUNCTION ----------
def predict_diabetes(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]

    try:
        confidence = max(model.predict_proba(arr)[0]) * 100
    except:
        confidence = None

    label = "Diabetic" if pred == 1 else "Not Diabetic"
    return label, confidence

# ---------- HEADER ----------
st.markdown("<div class='main-title'>🩺 Diabetes Prediction</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>AI-based health risk assessment</div>", unsafe_allow_html=True)

# ---------- INPUT CARD ----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input("Pregnancies", 0, 20)
        glucose = st.number_input("Glucose Level", 0)
        blood_pressure = st.number_input("Blood Pressure", 0)
        skin_thickness = st.number_input("Skin Thickness", 0)

    with col2:
        insulin = st.number_input("Insulin Level", 0)
        bmi = st.number_input("BMI", 0.0)
        pedigree = st.number_input("Diabetes Pedigree Function", 0.0)
        age = st.number_input("Age", 1)

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------- PREDICT BUTTON ----------
st.markdown("<div class='predict-btn'>", unsafe_allow_html=True)
clicked = st.button("🔍 Predict Diabetes")
st.markdown("</div>", unsafe_allow_html=True)

# ---------- RESULT ----------
if clicked:
    data = [
        pregnancies, glucose, blood_pressure,
        skin_thickness, insulin, bmi, pedigree, age
    ]

    result, confidence = predict_diabetes(data)

    st.write("")
    if result == "Diabetic":
        st.markdown(f"<div class='result-bad'>⚠️ Result: {result}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-good'>✅ Result: {result}</div>", unsafe_allow_html=True)

    if confidence:
        st.info(f"Model Confidence: {confidence:.2f}%")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Developed by Kartvaya Raikwar | Machine Learning Project")
