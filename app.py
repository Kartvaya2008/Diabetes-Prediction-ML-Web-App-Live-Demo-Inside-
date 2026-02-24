import numpy as np
import pickle
import streamlit as st
import os
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="DiabetesIQ · Clinical Risk System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

/* ══ STRICT MONOCHROME TOKEN SYSTEM ══════════════════════════ */
:root {
    /* Backgrounds */
    --bg-0:          #080808;
    --bg-1:          #0f0f0f;
    --bg-2:          #161616;
    --bg-3:          #1e1e1e;
    --bg-4:          #242424;

    /* Surfaces */
    --surface-ghost: rgba(255,255,255,0.03);
    --surface-mid:   rgba(255,255,255,0.05);
    --surface-up:    rgba(255,255,255,0.08);
    --surface-white: rgba(255,255,255,0.96);

    /* Borders */
    --border-dim:    rgba(255,255,255,0.06);
    --border-mid:    rgba(255,255,255,0.10);
    --border-up:     rgba(255,255,255,0.18);
    --border-strong: rgba(255,255,255,0.35);

    /* Typography */
    --t-white:       #f7f7f7;
    --t-silver:      #a1a1aa;
    --t-steel:       #71717a;
    --t-iron:        #3f3f46;
    --t-black:       #0a0a0a;
    --t-charcoal:    #1c1c1e;

    /* Semantic — muted only */
    --ok-text:       #6ee7b7;   /* very desaturated green */
    --ok-bg:         rgba(110,231,183,0.07);
    --ok-border:     rgba(110,231,183,0.18);
    --risk-text:     #fca5a5;   /* very desaturated red   */
    --risk-bg:       rgba(252,165,165,0.07);
    --risk-border:   rgba(252,165,165,0.18);
    --warn-text:     #d4d4d8;
    --warn-bg:       rgba(255,255,255,0.04);
    --warn-border:   rgba(255,255,255,0.12);

    /* Radii */
    --r-xl:  22px;
    --r-lg:  16px;
    --r-md:  11px;
    --r-sm:  7px;

    /* Shadows */
    --sh-card:  0 1px 2px rgba(0,0,0,0.6), 0 8px 28px rgba(0,0,0,0.55);
    --sh-white: 0 1px 3px rgba(0,0,0,0.5), 0 12px 36px rgba(0,0,0,0.45), 0 1px 0 rgba(255,255,255,0.10) inset;
    --sh-hover: 0 2px 4px rgba(0,0,0,0.7), 0 20px 48px rgba(0,0,0,0.6);
}

/* ══ GLOBAL ══════════════════════════════════════════════════ */
html, body, [class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: var(--bg-0) !important;
    color: var(--t-white) !important;
    font-family: 'Instrument Sans', -apple-system, sans-serif !important;
}
[data-testid="stHeader"] {
    background: rgba(8,8,8,0.92) !important;
    backdrop-filter: blur(18px) !important;
    border-bottom: 1px solid var(--border-dim) !important;
}
.block-container { padding-top: 2.2rem !important; max-width: 1300px; }
#MainMenu, footer { visibility: hidden; }

/* ══ SIDEBAR ════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--border-dim) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
[data-testid="stSidebar"] * { color: var(--t-steel) !important; }

/* ══ INPUTS ══════════════════════════════════════════════════ */
[data-testid="stNumberInput"] [data-baseweb="input"] {
    background: var(--bg-2) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-sm) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
    border-color: var(--border-strong) !important;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.05) !important;
}
[data-testid="stNumberInput"] input {
    color: var(--t-white) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    background: transparent !important;
}
[data-testid="stNumberInput"] label {
    color: var(--t-steel) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
}
[data-baseweb="input"] svg { fill: var(--t-iron) !important; }

/* ══ BUTTON ══════════════════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    background: var(--t-white) !important;
    color: var(--t-black) !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: .10em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 0.9rem 2rem !important;
    transition: all .25s cubic-bezier(.34,1.56,.64,1) !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.4), 0 4px 14px rgba(255,255,255,0.08) !important;
}
.stButton > button:hover {
    background: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.5), 0 12px 30px rgba(255,255,255,0.14) !important;
}
.stButton > button:active { transform: scale(.97) translateY(0) !important; }

/* ══ PROGRESS ════════════════════════════════════════════════ */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #d4d4d8, #f4f4f5) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: var(--surface-mid) !important;
    border-radius: 99px !important;
    height: 7px !important;
}

/* ══ SPINNER ══════════════════════════════════════════════════ */
.stSpinner > div { border-top-color: var(--t-silver) !important; }

/* ══ SCROLLBAR ════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb { background: var(--bg-4); border-radius: 99px; }
hr { border-color: var(--border-dim) !important; }

/* ══ ANIMATIONS ══════════════════════════════════════════════ */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes scaleIn {
    from { opacity:0; transform:scale(.93) translateY(8px); }
    to   { opacity:1; transform:scale(1)   translateY(0); }
}
@keyframes blinkDot {
    0%,100% { opacity:1; }
    50%     { opacity:.3; }
}

/* ══════════════════════════════════════════════════════════════
   COMPONENT LIBRARY
══════════════════════════════════════════════════════════════ */

/* HERO ─────────────────────────────────────────────────────── */
.hero {
    background: var(--surface-white);
    border-radius: var(--r-xl);
    padding: 2.6rem 3rem;
    margin-bottom: 2rem;
    box-shadow: var(--sh-white);
    animation: fadeUp .4s ease both;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:'';
    position:absolute; top:0; right:0;
    width:320px; height:320px;
    background: radial-gradient(circle at 85% 15%, rgba(0,0,0,0.025) 0%, transparent 65%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--t-black);
    color: var(--t-white);
    border-radius: 99px;
    padding: 5px 16px;
    font-size: 10px; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase;
    margin-bottom: 1.3rem;
}
.hero-pulse {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--ok-text);
    animation: blinkDot 2s ease-in-out infinite;
}
.hero-h1 {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(30px, 3.8vw, 50px);
    font-weight: 400;
    color: var(--t-black);
    line-height: 1.08;
    letter-spacing: -.025em;
    margin: 0 0 .7rem;
}
.hero-h1 em { font-style: italic; color: #3a3a3a; }
.hero-p {
    font-size: 15px;
    color: #636366;
    max-width: 480px;
    line-height: 1.7;
    margin: 0;
}

/* METRIC CARD ───────────────────────────────────────────────── */
.mc {
    background: var(--surface-ghost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-lg);
    padding: 1.25rem 1rem;
    text-align: center;
    transition: background .2s, box-shadow .2s, transform .22s;
    animation: fadeUp .4s .08s ease both;
    cursor: default;
}
.mc:hover {
    background: var(--surface-up);
    border-color: var(--border-mid);
    transform: translateY(-3px);
    box-shadow: var(--sh-hover);
}
.mc-ico { font-size: 20px; margin-bottom: 7px; opacity: .75; }
.mc-val {
    font-family: 'DM Mono', monospace;
    font-size: 18px; font-weight: 500;
    color: var(--t-white); display: block;
}
.mc-lbl {
    font-size: 9px; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase;
    color: var(--t-iron); margin-top: 4px;
}

/* FORM CARD ─────────────────────────────────────────────────── */
.fc {
    background: var(--surface-ghost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-xl);
    padding: 2rem 2rem 1.6rem;
    box-shadow: var(--sh-card);
    animation: fadeUp .4s .12s ease both;
    margin-bottom: 1.2rem;
    transition: border-color .25s;
}
.fc:hover { border-color: var(--border-mid); }

.sec-h {
    font-size: 9px; font-weight: 700;
    letter-spacing: .2em; text-transform: uppercase;
    color: var(--t-iron);
    margin-bottom: 1.4rem;
    display: flex; align-items: center; gap: 10px;
}
.sec-h::after {
    content:''; flex:1; height:1px;
    background: var(--border-dim);
}
.fl {
    font-size: 11px; font-weight: 600;
    color: var(--t-steel); letter-spacing: .05em;
    margin-bottom: 4px;
    display: flex; align-items: center; gap: 5px;
}

/* SUMMARY CARD ──────────────────────────────────────────────── */
.sc {
    background: var(--surface-ghost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-xl);
    padding: 1.8rem 1.8rem 1.4rem;
    animation: fadeUp .4s .16s ease both;
    margin-bottom: 1.2rem;
}
.sr {
    display:flex; justify-content:space-between; align-items:center;
    padding:.44rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.sr:last-child { border-bottom: none; }
.sr-k { font-size:13px; color: var(--t-steel); }
.sr-v {
    font-family:'DM Mono',monospace; font-size:13px;
    color: var(--t-white);
}

/* AWAIT BOX ─────────────────────────────────────────────────── */
.await {
    background: var(--surface-ghost);
    border: 1px dashed var(--border-mid);
    border-radius: var(--r-xl);
    padding: 3rem 2rem;
    text-align: center;
    animation: fadeUp .4s .18s ease both;
}
.await-ico { font-size: 38px; margin-bottom:.9rem; opacity:.3; }
.await-t { font-size:15px; font-weight:600; color:var(--t-steel); margin-bottom:.4rem; }
.await-s { font-size:13px; color:var(--t-iron); line-height:1.7; }
.await-cta { color:var(--t-silver); font-weight:600; }

/* RESULT ────────────────────────────────────────────────────── */
.res {
    border-radius: var(--r-xl);
    padding: 2.2rem 2rem;
    text-align: center;
    animation: scaleIn .42s cubic-bezier(.34,1.56,.64,1) both;
    margin-bottom: 1rem;
}
.res-risk  { background: var(--risk-bg);  border: 1px solid var(--risk-border); }
.res-clear { background: var(--ok-bg);    border: 1px solid var(--ok-border);   }
.res-ico  { font-size: 44px; margin-bottom: .75rem; }
.res-lbl  {
    font-family: 'Instrument Serif', serif;
    font-size: 27px; font-weight: 400;
    letter-spacing: -.015em; margin-bottom: .35rem;
}
.res-risk  .res-lbl  { color: var(--risk-text); }
.res-clear .res-lbl  { color: var(--ok-text); }
.res-desc { font-size:13px; color:var(--t-steel); line-height:1.65; }

/* CONFIDENCE ────────────────────────────────────────────────── */
.cc {
    background: var(--surface-ghost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-lg);
    padding: 1.4rem 1.6rem;
    animation: fadeUp .3s ease both;
    margin-bottom: .9rem;
}
.cc-top {
    display:flex; justify-content:space-between; align-items:baseline;
    margin-bottom: .75rem;
}
.cc-lbl {
    font-size:9px; font-weight:700;
    letter-spacing:.16em; text-transform:uppercase;
    color: var(--t-iron);
}
.cc-pct {
    font-family:'DM Mono',monospace;
    font-size:22px; font-weight:500;
    color: var(--t-white);
}
.cc-badge {
    display:inline-block; font-size:9px; font-weight:700;
    letter-spacing:.10em; text-transform:uppercase;
    border-radius:99px; padding:3px 12px; margin-top:.75rem;
}
.cc-high { color:#6ee7b7; background:rgba(110,231,183,.08); border:1px solid rgba(110,231,183,.2); }
.cc-mid  { color:#d4d4d8; background:rgba(212,212,216,.07); border:1px solid rgba(212,212,216,.18); }
.cc-low  { color:#fca5a5; background:rgba(252,165,165,.07); border:1px solid rgba(252,165,165,.18); }

/* DISCLAIMER ────────────────────────────────────────────────── */
.disc {
    background: var(--warn-bg);
    border: 1px solid var(--warn-border);
    border-radius: var(--r-md);
    padding: .8rem 1rem;
    font-size: 11px; color: var(--t-iron); line-height: 1.7;
}

/* SIDEBAR ───────────────────────────────────────────────────── */
.sb-name {
    font-family: 'Instrument Serif', serif;
    font-size: 22px; font-weight: 400;
    color: var(--t-white) !important;
    letter-spacing: -.015em;
}
.sb-sub {
    font-size: 9px !important; font-weight: 700 !important;
    letter-spacing: .16em !important; text-transform: uppercase !important;
    color: var(--t-iron) !important; margin-bottom: 1.6rem !important;
    display: block;
}
.sb-online {
    display:inline-flex; align-items:center; gap:6px;
    font-size:10px !important; font-weight:700 !important;
    letter-spacing:.1em !important; text-transform:uppercase !important;
    color: var(--ok-text) !important;
}
.sb-dot {
    width:6px; height:6px; border-radius:50%;
    background: var(--ok-text);
    display: inline-block;
    animation: blinkDot 2s ease-in-out infinite;
}
.sb-divider { height:1px; background:var(--border-dim); margin:1.3rem 0; }
.sb-sec-h {
    font-size:9px !important; font-weight:700 !important;
    letter-spacing:.18em !important; text-transform:uppercase !important;
    color: var(--t-iron) !important;
    margin-bottom: .9rem !important; display: block;
}
.sb-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:.5rem 0; border-bottom:1px solid var(--border-dim);
    font-size:12px !important;
}
.sb-row:last-child { border-bottom: none; }
.sb-row-k { color: var(--t-steel) !important; }
.sb-row-v {
    font-family:'DM Mono',monospace; font-size:11px !important;
    color: var(--t-silver) !important;
    background: var(--bg-3);
    border: 1px solid var(--border-dim);
    border-radius: 5px; padding: 2px 8px;
}
.sb-note {
    background: rgba(255,255,255,0.02);
    border-left: 2px solid var(--border-up);
    border-radius: 0 var(--r-sm) var(--r-sm) 0;
    padding: .9rem 1rem;
    font-size: 11px !important;
    color: var(--t-iron) !important;
    line-height: 1.7 !important;
    margin-top: .9rem;
}

/* FOOTER ────────────────────────────────────────────────────── */
.foot {
    text-align:center;
    padding: 2.5rem 1rem 1.5rem;
    border-top: 1px solid var(--border-dim);
    margin-top: 2.5rem;
}
.foot-brand {
    font-family:'Instrument Serif',serif;
    font-size:17px; font-weight:400;
    color: var(--t-silver); margin-bottom:.35rem;
}
.foot-sub  { font-size:11px; color:var(--t-iron); letter-spacing:.06em; line-height:1.9; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# LOAD MODEL
# ════════════════════════════════════════════════════════════════
model_path = os.path.join(os.path.dirname(__file__), "trained_model.sav")
if not os.path.exists(model_path):
    st.error("❌ Model file `trained_model.sav` not found. Place it next to this script.")
    st.stop()
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ════════════════════════════════════════════════════════════════
# PREDICTION  (logic unchanged)
# ════════════════════════════════════════════════════════════════
def predict_diabetes(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    try:
        confidence = max(model.predict_proba(arr)[0]) * 100
    except Exception:
        confidence = None
    label = "Diabetic" if pred == 1 else "Not Diabetic"
    return label, confidence

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-name">DiabetesIQ</div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-sub">Clinical Risk Intelligence</span>', unsafe_allow_html=True)
    st.markdown('<span class="sb-online"><span class="sb-dot"></span> Model Online</span>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-sec-h">About</span>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:13px;color:#52525b;line-height:1.75;margin:0'>
    This tool estimates diabetes risk using a trained ML model on the
    <strong style='color:#71717a'>PIMA Indian Diabetes Dataset</strong>.
    Enter all 8 clinical biomarkers for a prediction.
    </p>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-sec-h">Model Specs</span>', unsafe_allow_html=True)
    for k, v in [("Algorithm","SVM / RFC"), ("Dataset","PIMA Indians"),
                  ("Features","8 Clinical"), ("Output","Binary Class")]:
        st.markdown(f'<div class="sb-row"><span class="sb-row-k">{k}</span><span class="sb-row-v">{v}</span></div>',
                    unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-sec-h">Reference Ranges</span>', unsafe_allow_html=True)
    for k, v in [("Glucose (fasting)", "70–100 mg/dL"), ("Blood Pressure", "<120/80 mmHg"),
                  ("BMI (healthy)", "18.5–24.9"), ("Insulin", "16–166 μU/mL"),
                  ("Skin Thickness", "10–50 mm")]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;padding:.45rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px'>
            <span style='color:#52525b'>{k}</span>
            <span style='color:#71717a;font-family:"DM Mono",monospace;font-size:11px'>{v}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-note">⚠️ Educational use only. Not a substitute for professional clinical diagnosis.</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:11px;color:#3f3f46;text-align:center;line-height:1.9'>
        Built by <strong style='color:#52525b'>Kartvaya Raikwar</strong><br>
        Machine Learning · Healthcare AI
    </p>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">
        <span class="hero-pulse"></span>
        Clinical Screening System
    </div>
    <div class="hero-h1">Diabetes Risk <em>Assessment</em></div>
    <p class="hero-p">Enter patient biomarkers to receive an AI-assisted risk classification with model confidence scoring and instant clinical feedback.</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# METRIC STRIP
# ════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
for col, (ico, val, lbl) in zip([c1,c2,c3,c4], [
    ("🧬", "8",     "Input Features"),
    ("⚡", "< 1s",  "Inference Time"),
    ("🎯", "~77%",  "Model Accuracy"),
    ("📋", "Binary","Output Class"),
]):
    col.markdown(f"""
    <div class="mc">
        <div class="mc-ico">{ico}</div>
        <span class="mc-val">{val}</span>
        <div class="mc-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.write("")

# ════════════════════════════════════════════════════════════════
# INPUT FORM
# ════════════════════════════════════════════════════════════════
left, right = st.columns([3, 2], gap="large")

with left:
    # Group 1
    st.markdown('<div class="fc">', unsafe_allow_html=True)
    st.markdown('<div class="sec-h">Reproductive &amp; Physical Metrics</div>', unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="fl">Pregnancies</div>', unsafe_allow_html=True)
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0,
                                      label_visibility="collapsed",
                                      help="Number of times pregnant (0–20)")
    with cb:
        st.markdown('<div class="fl">BMI (kg/m²)</div>', unsafe_allow_html=True)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=0.0, step=0.1,
                              label_visibility="collapsed",
                              help="Body Mass Index. Healthy: 18.5–24.9")

    cc, cd = st.columns(2)
    with cc:
        st.markdown('<div class="fl">Age (years)</div>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=1, max_value=120, value=25,
                              label_visibility="collapsed",
                              help="Patient age in years")
    with cd:
        st.markdown('<div class="fl">Diabetes Pedigree Function</div>', unsafe_allow_html=True)
        pedigree = st.number_input("Pedigree", min_value=0.0, max_value=3.0,
                                   value=0.0, step=0.001, format="%.3f",
                                   label_visibility="collapsed",
                                   help="Hereditary diabetes likelihood (0.08–2.42)")
    st.markdown('</div>', unsafe_allow_html=True)

    # Group 2
    st.markdown('<div class="fc">', unsafe_allow_html=True)
    st.markdown('<div class="sec-h">Laboratory &amp; Biochemical Values</div>', unsafe_allow_html=True)

    ce, cf = st.columns(2)
    with ce:
        st.markdown('<div class="fl">Plasma Glucose (mg/dL)</div>', unsafe_allow_html=True)
        glucose = st.number_input("Glucose", min_value=0, max_value=300, value=0,
                                  label_visibility="collapsed",
                                  help="Fasting plasma glucose. Normal: 70–100 mg/dL")
    with cf:
        st.markdown('<div class="fl">Serum Insulin (μU/mL)</div>', unsafe_allow_html=True)
        insulin = st.number_input("Insulin", min_value=0, max_value=900, value=0,
                                  label_visibility="collapsed",
                                  help="2-hour serum insulin. Normal: 16–166 μU/mL")

    cg, ch = st.columns(2)
    with cg:
        st.markdown('<div class="fl">Diastolic BP (mmHg)</div>', unsafe_allow_html=True)
        blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=0,
                                         label_visibility="collapsed",
                                         help="Diastolic blood pressure. Normal: <80 mmHg")
    with ch:
        st.markdown('<div class="fl">Skin Thickness (mm)</div>', unsafe_allow_html=True)
        skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=0,
                                         label_visibility="collapsed",
                                         help="Triceps skin fold thickness. Normal: 10–50 mm")
    st.markdown('</div>', unsafe_allow_html=True)

    # Button
    predict_clicked = st.button("Run Diabetes Risk Assessment", use_container_width=True)

# ════════════════════════════════════════════════════════════════
# RIGHT COLUMN
# ════════════════════════════════════════════════════════════════
with right:
    # Live summary
    st.markdown('<div class="sc">', unsafe_allow_html=True)
    st.markdown('<div class="sec-h" style="margin-bottom:1.1rem">Parameter Summary</div>', unsafe_allow_html=True)

    summary = [
        ("Pregnancies",    str(pregnancies),       ""),
        ("Glucose",        str(glucose),           "mg/dL"),
        ("Blood Pressure", str(blood_pressure),    "mmHg"),
        ("Skin Thickness", str(skin_thickness),    "mm"),
        ("Insulin",        str(insulin),           "μU/mL"),
        ("BMI",            f"{bmi:.1f}",           "kg/m²"),
        ("Pedigree Fn.",   f"{pedigree:.3f}",      ""),
        ("Age",            str(age),               "yrs"),
    ]
    for name, val, unit in summary:
        u = f'<span style="font-size:10px;color:#3f3f46;margin-left:3px">{unit}</span>' if unit else ""
        st.markdown(f"""
        <div class="sr">
            <span class="sr-k">{name}</span>
            <span class="sr-v">{val}{u}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Result
    if predict_clicked:
        data_input = [pregnancies, glucose, blood_pressure,
                      skin_thickness, insulin, bmi, pedigree, age]

        with st.spinner("Analyzing clinical parameters…"):
            time.sleep(0.85)
            result, confidence = predict_diabetes(data_input)

        st.write("")
        is_risk = result == "Diabetic"

        if is_risk:
            st.markdown("""
            <div class="res res-risk">
                <div class="res-ico">⚠️</div>
                <div class="res-lbl">Diabetic</div>
                <div class="res-desc">Elevated risk detected.<br>Clinical follow-up is recommended.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="res res-clear">
                <div class="res-ico">✓</div>
                <div class="res-lbl">Not Diabetic</div>
                <div class="res-desc">Parameters within acceptable range.<br>Continue routine health monitoring.</div>
            </div>""", unsafe_allow_html=True)

        if confidence is not None:
            cv = confidence / 100.0
            if confidence >= 80:
                bc, bt = "cc-high", "High Confidence"
            elif confidence >= 60:
                bc, bt = "cc-mid",  "Moderate Confidence"
            else:
                bc, bt = "cc-low",  "Low Confidence"

            st.markdown(f"""
            <div class="cc">
                <div class="cc-top">
                    <span class="cc-lbl">Model Confidence</span>
                    <span class="cc-pct">{confidence:.1f}%</span>
                </div>""", unsafe_allow_html=True)
            st.progress(cv)
            st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin-top:.7rem">
                    <span class="cc-badge {bc}">{bt}</span>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="disc">
            <strong style="color:#71717a">Disclaimer:</strong>
            This result is generated by a machine learning model for educational purposes only.
            It does not constitute a medical diagnosis. Consult a licensed healthcare provider.
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="await">
            <div class="await-ico">🔬</div>
            <div class="await-t">Awaiting Assessment</div>
            <div class="await-s">
                Complete all biomarker fields and click<br>
                <span class="await-cta">Run Diabetes Risk Assessment</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="foot">
    <div class="foot-brand">DiabetesIQ · Clinical Risk Intelligence</div>
    <div class="foot-sub">
        Developed by <strong style="color:#52525b">Kartvaya Raikwar</strong>
        &nbsp;·&nbsp; Machine Learning · Healthcare AI
        &nbsp;·&nbsp; PIMA Indian Diabetes Dataset
        &nbsp;·&nbsp; © 2025
    </div>
</div>
""", unsafe_allow_html=True)
