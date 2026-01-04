import numpy as np
import pickle
import streamlit as st
import os
import pandas as pd

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

# ---------- UI ----------
st.set_page_config(page_title="Diabetes Prediction", page_icon="🩺")

st.title("🩺 Diabetes Prediction App")
st.write("Enter patient details to predict diabetes")

# ---------- INPUTS ----------
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", 0, 20)
    glucose = st.number_input("Glucose Level", 0)
    blood_pressure = st.number_input("Blood Pressure", 0)
    skin_thickness = st.number_input("Skin Thickness", 0)

with col2:
    insulin = st.number_input("Insulin Level", 0)
    bmi = st.number_input("BMI", 0.0)
    pedigree = st.number_input("Diabetes Pedigree", 0.0)
    age = st.number_input("Age", 1)

# ---------- BUTTON ----------
if st.button("🔍 Predict"):
    data = [
        pregnancies, glucose, blood_pressure,
        skin_thickness, insulin, bmi, pedigree, age
    ]

    result, confidence = predict_diabetes(data)

    st.subheader("📊 Result")
    if result == "Diabetic":
        st.error(result)
    else:
        st.success(result)

    if confidence:
        st.info(f"Model Confidence: {confidence:.2f}%")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Developed by Kartvaya Raikwar | ML Project")
