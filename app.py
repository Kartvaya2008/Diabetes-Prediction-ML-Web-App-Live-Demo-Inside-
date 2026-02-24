import numpy as np
import pickle
import streamlit as st
import os
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="DiabetesIQ · Health Risk Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700&display=swap');

/* ─── ROOT TOKENS ─────────────────────────────────────────── */
:root {
    --bg-base:      #060d1a;
    --bg-surface:   #0c1829;
    --bg-card:      rgba(16, 28, 52, 0.85);
    --bg-glass:     rgba(255,255,255,0.04);
    --border:       rgba(99,179,237,0.15);
    --border-hover: rgba(99,179,237,0.40);
    --accent-cyan:  #38bdf8;
    --accent-teal:  #2dd4bf;
    --accent-rose:  #fb7185;
    --accent-amber: #fbbf24;
    --accent-green: #34d399;
    --text-primary: #e8f4ff;
    --text-muted:   #6b8cae;
    --text-dim:     #3a5470;
    --radius-lg:    18px;
    --radius-md:    12px;
    --radius-sm:    8px;
    --shadow-card:  0 8px 40px rgba(0,0,0,0.45), 0 1px 0 rgba(255,255,255,0.05) inset;
    --glow-cyan:    0 0 30px rgba(56,189,248,0.18);
}

/* ─── GLOBAL RESETS ───────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: var(--bg-base);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(56,189,248,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(45,212,191,0.07) 0%, transparent 60%);
    min-height: 100vh;
}

/* ─── SIDEBAR ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* ─── HIDE STREAMLIT CHROME ───────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* ─── HEADER HERO ─────────────────────────────────────────── */
.hero-wrap {
    background: linear-gradient(135deg, rgba(56,189,248,0.08) 0%, rgba(45,212,191,0.06) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-card);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.30);
    border-radius: 99px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    color: var(--accent-cyan);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(28px, 4vw, 46px);
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.15;
    margin: 0 0 0.5rem;
}
.hero-title span {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 15px;
    color: var(--text-muted);
    margin: 0;
    max-width: 520px;
    line-height: 1.6;
}

/* ─── GLASS CARD ──────────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-card);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 1.5rem;
}
.glass-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-card), var(--glow-cyan);
}

/* ─── SECTION LABELS ──────────────────────────────────────── */
.section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ─── FIELD LABELS ────────────────────────────────────────── */
.field-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.04em;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ─── STREAMLIT INPUT OVERRIDES ───────────────────────────── */
input[type="number"], input[type="text"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
input[type="number"]:focus, input[type="text"]:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.15) !important;
    outline: none !important;
}
label { color: var(--text-muted) !important; font-size: 13px !important; }
[data-testid="stNumberInput"] > label { color: var(--text-muted) !important; }

/* ─── BUTTON ──────────────────────────────────────────────── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #14b8a6 100%) !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.30) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(14,165,233,0.45) !important;
    filter: brightness(1.08) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── PROGRESS BAR ────────────────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-teal)) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 99px !important;
    height: 10px !important;
}

/* ─── METRIC CARD ─────────────────────────────────────────── */
.metric-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.4rem;
    text-align: center;
    transition: all 0.25s ease;
}
.metric-card:hover {
    border-color: var(--border-hover);
    background: rgba(255,255,255,0.06);
}
.metric-icon { font-size: 22px; margin-bottom: 4px; }
.metric-val {
    font-family: 'DM Mono', monospace;
    font-size: 20px;
    font-weight: 500;
    color: var(--accent-cyan);
    display: block;
}
.metric-lbl {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-top: 2px;
}

/* ─── RESULT PANELS ───────────────────────────────────────── */
.result-positive {
    background: linear-gradient(135deg, rgba(251,113,133,0.12) 0%, rgba(239,68,68,0.08) 100%);
    border: 1px solid rgba(251,113,133,0.35);
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
    animation: resultPop 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
}
.result-negative {
    background: linear-gradient(135deg, rgba(52,211,153,0.12) 0%, rgba(16,185,129,0.08) 100%);
    border: 1px solid rgba(52,211,153,0.35);
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
    animation: resultPop 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
}
.result-icon { font-size: 52px; display: block; margin-bottom: 0.75rem; }
.result-label {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 0.4rem;
}
.result-positive .result-label { color: var(--accent-rose); }
.result-negative .result-label { color: var(--accent-green); }
.result-sublabel {
    font-size: 14px;
    color: var(--text-muted);
}

@keyframes resultPop {
    from { opacity: 0; transform: scale(0.88) translateY(10px); }
    to   { opacity: 1; transform: scale(1)    translateY(0);     }
}

/* ─── CONFIDENCE SECTION ──────────────────────────────────── */
.conf-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.conf-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.conf-value {
    font-family: 'DM Mono', monospace;
    font-size: 22px;
    font-weight: 500;
    color: var(--accent-cyan);
}

/* ─── SIDEBAR STYLES ──────────────────────────────────────── */
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--accent-cyan);
    margin-bottom: 0.25rem;
}
.sb-tagline {
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.sb-divider {
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
}
.sb-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
}
.sb-stat-key { color: var(--text-muted); }
.sb-stat-val {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--accent-teal);
    background: rgba(45,212,191,0.10);
    border: 1px solid rgba(45,212,191,0.20);
    border-radius: 6px;
    padding: 2px 8px;
}
.sb-tip {
    background: rgba(56,189,248,0.06);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 0.9rem 1rem;
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.6;
    margin-top: 1rem;
}

/* ─── STATUS DOT ──────────────────────────────────────────── */
.status-dot {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 600;
    color: var(--accent-green);
    letter-spacing: 0.06em; text-transform: uppercase;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 6px var(--accent-green);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.35; }
}

/* ─── TOOLTIP ─────────────────────────────────────────────── */
.tooltip-wrap { position: relative; display: inline-block; }
.tooltip-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 16px; height: 16px;
    background: rgba(107,140,174,0.25);
    border-radius: 50%;
    font-size: 9px; color: var(--text-muted);
    cursor: help;
    font-weight: 700;
}

/* ─── FOOTER ──────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}
.footer-brand {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    color: var(--accent-cyan);
    margin-bottom: 0.4rem;
}
.footer-sub {
    font-size: 12px;
    color: var(--text-dim);
    letter-spacing: 0.06em;
}
.footer-copy {
    font-size: 11px;
    color: var(--text-dim);
    margin-top: 0.8rem;
    opacity: 0.6;
}

/* ─── SELECTBOX / SPINNER OVERRIDES ──────────────────────── */
.stSpinner > div { border-top-color: var(--accent-cyan) !important; }

/* ─── ALERTS ──────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
}

/* ─── SCROLLBAR ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--text-dim);
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# LOAD MODEL
# ───────────────────────────────────────────────────────────────
model_path = os.path.join(os.path.dirname(__file__), "trained_model.sav")
if not os.path.exists(model_path):
    st.error("❌ Model file `trained_model.sav` not found. Please place it next to this script.")
    st.stop()

with open(model_path, "rb") as f:
    model = pickle.load(f)


# ───────────────────────────────────────────────────────────────
# PREDICTION LOGIC  (unchanged)
# ───────────────────────────────────────────────────────────────
def predict_diabetes(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    try:
        confidence = max(model.predict_proba(arr)[0]) * 100
    except:
        confidence = None
    label = "Diabetic" if pred == 1 else "Not Diabetic"
    return label, confidence


# ───────────────────────────────────────────────────────────────
# SIDEBAR
# ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">DiabetesIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tagline">Clinical Risk Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<span class="status-dot"><span class="dot"></span>Model Online</span>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown("**📋 About This Tool**")
    st.markdown("""
<p style="font-size:13px;color:#6b8cae;line-height:1.7;margin-top:0.5rem;">
This dashboard uses a trained machine learning model to estimate the likelihood of diabetes based on key clinical biomarkers from the <strong style="color:#38bdf8">PIMA Indian Diabetes Dataset</strong>.
</p>
""", unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("**📊 Model Specs**")

    stats = [
        ("Algorithm",   "SVM / RFC"),
        ("Dataset",     "PIMA Indians"),
        ("Features",    "8 Clinical"),
        ("Target",      "Binary Class"),
    ]
    for k, v in stats:
        st.markdown(f'<div class="sb-stat"><span class="sb-stat-key">{k}</span><span class="sb-stat-val">{v}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("**🩺 Reference Ranges**")
    refs = [
        ("Glucose (fasting)", "70 – 100 mg/dL"),
        ("Blood Pressure",    "< 120/80 mmHg"),
        ("BMI (healthy)",     "18.5 – 24.9"),
        ("Insulin",           "16 – 166 μU/mL"),
    ]
    for k, v in refs:
        st.markdown(f'<div class="sb-stat"><span class="sb-stat-key" style="font-size:11px">{k}</span><span style="font-size:11px;color:#6b8cae">{v}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-tip">⚠️ This tool is for educational purposes only. Always consult a qualified medical professional for clinical diagnosis.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;color:#3a5470;text-align:center;">Built by <strong style="color:#6b8cae">Kartvaya Raikwar</strong><br>Machine Learning · Healthcare AI</p>', unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# HERO HEADER
# ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🔬 &nbsp;AI-Powered · Clinical Grade</div>
    <div class="hero-title">Diabetes Risk <span>Assessment</span></div>
    <p class="hero-sub">Enter patient biomarkers below to receive an instant AI-driven risk prediction with model confidence scoring.</p>
</div>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# QUICK METRIC CARDS  (summary row)
# ───────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
cards = [
    ("🧬", "8", "Input Features"),
    ("⚡", "< 1s", "Inference Time"),
    ("📈", "Binary", "Output Class"),
    ("🎯", "~77%", "Model Accuracy"),
]
for col, (icon, val, lbl) in zip([m1, m2, m3, m4], cards):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <span class="metric-val">{val}</span>
        <div class="metric-lbl">{lbl}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ───────────────────────────────────────────────────────────────
# INPUT SECTIONS
# ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    # --- Group 1: Reproductive & Physical ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔵 &nbsp;Reproductive & Physical Metrics</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="field-label">🤰 Pregnancies</div>', unsafe_allow_html=True)
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0,
                                       label_visibility="collapsed",
                                       help="Number of times pregnant (0–20)")
    with c2:
        st.markdown('<div class="field-label">⚖️ BMI</div>', unsafe_allow_html=True)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=0.0, step=0.1,
                               label_visibility="collapsed",
                               help="Body Mass Index (kg/m²). Healthy range: 18.5–24.9")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="field-label">🧓 Age</div>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=1, max_value=120, value=25,
                               label_visibility="collapsed",
                               help="Patient age in years")
    with c4:
        st.markdown('<div class="field-label">🧬 Diabetes Pedigree</div>', unsafe_allow_html=True)
        pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0,
                                    value=0.0, step=0.001, format="%.3f",
                                    label_visibility="collapsed",
                                    help="Genetic likelihood of diabetes based on family history")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Group 2: Lab Values ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🟢 &nbsp;Laboratory & Biochemical Values</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="field-label">🍬 Glucose Level</div>', unsafe_allow_html=True)
        glucose = st.number_input("Glucose Level", min_value=0, max_value=300, value=0,
                                   label_visibility="collapsed",
                                   help="Plasma glucose concentration (mg/dL). Normal fasting: 70–100")
    with c6:
        st.markdown('<div class="field-label">💉 Insulin Level</div>', unsafe_allow_html=True)
        insulin = st.number_input("Insulin Level", min_value=0, max_value=900, value=0,
                                   label_visibility="collapsed",
                                   help="2-Hour serum insulin (μU/mL). Normal: 16–166")

    c7, c8 = st.columns(2)
    with c7:
        st.markdown('<div class="field-label">❤️ Blood Pressure</div>', unsafe_allow_html=True)
        blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=0,
                                          label_visibility="collapsed",
                                          help="Diastolic blood pressure (mmHg). Normal: < 80")
    with c8:
        st.markdown('<div class="field-label">📏 Skin Thickness</div>', unsafe_allow_html=True)
        skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=0,
                                          label_visibility="collapsed",
                                          help="Triceps skin fold thickness (mm)")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- Predict Button ---
    st.markdown('<div style="margin-top:0.5rem">', unsafe_allow_html=True)
    predict_clicked = st.button("🔍  Run Diabetes Risk Prediction", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# RIGHT COLUMN — Input Summary + Result
# ───────────────────────────────────────────────────────────────
with right_col:

    # Live input summary
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📋 &nbsp;Input Summary</div>', unsafe_allow_html=True)

    summary_data = [
        ("🤰", "Pregnancies",   pregnancies, ""),
        ("🍬", "Glucose",       glucose,     "mg/dL"),
        ("❤️", "Blood Pressure",blood_pressure,"mmHg"),
        ("📏", "Skin Thickness",skin_thickness,"mm"),
        ("💉", "Insulin",       insulin,     "μU/mL"),
        ("⚖️", "BMI",           bmi,         "kg/m²"),
        ("🧬", "Pedigree",      f"{pedigree:.3f}", ""),
        ("🧓", "Age",           age,         "yrs"),
    ]
    for icon, name, val, unit in summary_data:
        unit_html = f'<span style="font-size:10px;color:#3a5470;margin-left:3px">{unit}</span>' if unit else ""
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:0.42rem 0;border-bottom:1px solid rgba(99,179,237,0.08);">
            <span style="font-size:13px;color:#6b8cae">{icon} {name}</span>
            <span style="font-family:'DM Mono',monospace;font-size:13px;color:#e8f4ff">
                {val}{unit_html}
            </span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── RESULT PANEL ─────────────────────────────────────────
    if predict_clicked:
        data_input = [pregnancies, glucose, blood_pressure,
                      skin_thickness, insulin, bmi, pedigree, age]

        with st.spinner("Analyzing biomarkers…"):
            time.sleep(0.9)   # brief UX delay for realism
            result, confidence = predict_diabetes(data_input)

        st.write("")

        if result == "Diabetic":
            st.markdown("""
            <div class="result-positive">
                <span class="result-icon">⚠️</span>
                <div class="result-label">Diabetic</div>
                <div class="result-sublabel">Elevated risk detected — consult a physician</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-negative">
                <span class="result-icon">✅</span>
                <div class="result-label">Not Diabetic</div>
                <div class="result-sublabel">Low risk profile — maintain a healthy lifestyle</div>
            </div>
            """, unsafe_allow_html=True)

        # Confidence section
        if confidence is not None:
            st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="padding:1.4rem 1.6rem">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="conf-label">
                <span class="conf-title">Model Confidence</span>
                <span class="conf-value">{confidence:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(confidence))

            # Confidence tier badge
            if confidence >= 80:
                badge_color, badge_text = "#34d399", "High Confidence"
            elif confidence >= 60:
                badge_color, badge_text = "#fbbf24", "Moderate Confidence"
            else:
                badge_color, badge_text = "#fb7185", "Low Confidence"

            st.markdown(f"""
            <div style="margin-top:0.8rem;display:flex;justify-content:flex-end">
                <span style="font-size:11px;font-weight:600;color:{badge_color};
                             background:{'rgba(52,211,153,0.10)' if confidence >= 80 else 'rgba(251,191,36,0.10)' if confidence >= 60 else 'rgba(251,113,133,0.10)'};
                             border:1px solid {badge_color}40;
                             border-radius:99px;padding:3px 12px;letter-spacing:0.06em">
                    {badge_text}
                </span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Disclaimer
        st.markdown("""
        <div style="margin-top:0.75rem;padding:0.75rem 1rem;
                    background:rgba(251,191,36,0.06);
                    border:1px solid rgba(251,191,36,0.20);
                    border-radius:10px;
                    font-size:11px;color:#6b8cae;line-height:1.6">
            ℹ️ <strong style="color:#fbbf24">Disclaimer:</strong>
            This prediction is for informational purposes only and does not
            constitute medical advice. Please consult a licensed healthcare provider.
        </div>
        """, unsafe_allow_html=True)

    else:
        # Placeholder state
        st.markdown("""
        <div style="background:rgba(255,255,255,0.02);border:1px dashed rgba(99,179,237,0.20);
                    border-radius:16px;padding:2.5rem 2rem;text-align:center;margin-top:0">
            <div style="font-size:40px;margin-bottom:1rem">🔬</div>
            <div style="font-size:15px;font-weight:600;color:#6b8cae;margin-bottom:0.4rem">
                Awaiting Prediction
            </div>
            <div style="font-size:13px;color:#3a5470;line-height:1.6">
                Fill in the patient biomarkers and click<br>
                <strong style="color:#38bdf8">Run Diabetes Risk Prediction</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# FOOTER
# ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-brand">DiabetesIQ</div>
    <div class="footer-sub">Clinical Risk Intelligence · Powered by Machine Learning</div>
    <div class="footer-copy">
        Developed by <strong>Kartvaya Raikwar</strong> &nbsp;·&nbsp;
        Machine Learning Project &nbsp;·&nbsp;
        PIMA Indian Diabetes Dataset &nbsp;·&nbsp; © 2025
    </div>
</div>
""", unsafe_allow_html=True)
