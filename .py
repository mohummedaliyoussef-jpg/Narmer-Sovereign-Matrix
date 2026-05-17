@'
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3, json, hashlib, os, secrets, subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from io import BytesIO
from translations import translate

st.set_page_config(page_title="🔱 NARMER v53.3", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

PRIMARY = "#2563EB"
ACCENT = "#c9a050"
DIMS_AR = [
    "الحوكمة والامتثال", "القوة العسكرية", "المناعة السيبرانية", "البنية التحتية الرقمية",
    "سلاسل الإمداد", "رأس المال البشري", "السيادة المالية", "استقلالية الطاقة", "الأمن الغذائي",
    "الابتكار", "الدبلوماسية", "الاستقرار الاجتماعي", "الاستدامة البيئية", "السيادة الفضائية",
    "سيادة الذكاء الاصطناعي", "القوة الناعمة", "الأمن الصحي"
]
DIMS_EN = [
    "Governance & Compliance", "Military Power", "Cyber Resilience", "Digital Infrastructure",
    "Supply Chains", "Human Capital", "Financial Sovereignty", "Energy Independence", "Food Security",
    "Innovation", "Diplomacy", "Social Stability", "Environmental Sustainability", "Space Sovereignty",
    "AI Sovereignty", "Soft Power", "Health Security"
]
WEIGHTS = np.array([0.085,0.11,0.13,0.09,0.08,0.07,0.085,0.10,0.06,
                    0.065,0.05,0.055,0.04,0.035,0.06,0.03,0.045])
WEIGHTS /= WEIGHTS.sum()
DB_PATH = "narmer_v53.db"
AVAILABLE_LANGS = ["ar","en","fr","es","de","it","pt","ru","zh-cn","ja","ko","hi","tr","fa","ur","id","sw","ha","bn","th","vi","nl","pl"]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT, salt TEXT, role TEXT, last_login TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, event TEXT, details TEXT, username TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS score_history (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, score REAL, dimensions TEXT, mode TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS scenarios (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, timestamp TEXT, dimensions TEXT, score REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS auth_attempts (ip TEXT, timestamp TEXT)''')
    create_default_user(c, "admin", "Sovereign2026!", "مدير")
    create_default_user(c, "analyst", "Analyst2026!", "محلل")
    create_default_user(c, "viewer", "Viewer2026!", "مشاهد")
    conn.commit()
    conn.close()

def create_default_user(c, username, password, role):
    c.execute("SELECT salt FROM users WHERE username=?", (username,))
    if not c.fetchone():
        salt = secrets.token_hex(16)
        h = hashlib.sha256((password + salt).encode()).hexdigest()
        c.execute("INSERT OR IGNORE INTO users (username, password_hash, salt, role) VALUES (?,?,?,?)", (username, h, salt, role))

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash, salt, role FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hashlib.sha256((password + row[1]).encode()).hexdigest():
        return True, row[2]
    return False, ""

def record_auth_failure():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO auth_attempts (ip, timestamp) VALUES ('local', ?)", (datetime.now().isoformat(),))
    conn.commit()
    conn.close()

def recent_failures(minutes=5):
    cutoff = (datetime.now() - timedelta(minutes=minutes)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM auth_attempts WHERE timestamp > ?", (cutoff,))
    count = c.fetchone()[0]
    conn.close()
    return count

def add_audit(event, details, username="system"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO audit_log (timestamp, event, details, username) VALUES (?,?,?,?)", (datetime.now().isoformat(), event, details, username))
    conn.commit()
    conn.close()

def save_score(score, dims, mode="manual"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO score_history (timestamp, score, dimensions, mode) VALUES (?,?,?,?)", (datetime.now().isoformat(), score, json.dumps(dims, ensure_ascii=False), mode))
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM score_history ORDER BY timestamp DESC LIMIT ?", conn, params=(limit,))
    conn.close()
    return df

def save_scenario(name, dims, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO scenarios (name, timestamp, dimensions, score) VALUES (?,?,?,?)", (name, datetime.now().isoformat(), json.dumps(dims, ensure_ascii=False), score))
    conn.commit()
    conn.close()

def get_scenarios():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM scenarios ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("<h2 style='text-align:center; color:#c9a050;'>🔱 NARMER</h2>", unsafe_allow_html=True)
            username = st.text_input(translate("Username", st.session_state.get("lang","ar")))
            password = st.text_input(translate("Password", st.session_state.get("lang","ar")), type="password")
            if st.button(translate("Login Button", st.session_state.get("lang","ar"))):
                if recent_failures() >= 5:
                    st.error(translate("Account Locked", st.session_state.get("lang","ar")))
                else:
                    ok, role = verify_user(username, password)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.role = role
                        add_audit("Login", username, username)
                        st.rerun()
                    else:
                        record_auth_failure()
                        left = 5 - recent_failures()
                        st.error(f"{translate('Invalid Credentials', st.session_state.get('lang','ar'))}. {left} {translate('Remaining', st.session_state.get('lang','ar'))}")
        st.stop()

def v_score(inputs: Dict[str, float]) -> float:
    vals = np.clip([inputs.get(d, 50)/100.0 for d in DIMS_AR], 0.01, 1.0)
    return float(np.exp(np.sum(WEIGHTS * np.log(vals))) * 100)

@st.cache_data(ttl=120)
def monte_carlo_analysis(inputs_json: str, iterations=5000):
    inputs = json.loads(inputs_json)
    vals = np.array([inputs.get(d, 50)/100.0 for d in DIMS_AR])
    noise = np.random.normal(0, 0.035, (iterations, len(DIMS_AR)))
    sim_vals = np.clip(vals + noise, 0.01, 1.0)
    scores = np.exp(np.sum(WEIGHTS * np.log(sim_vals), axis=1)) * 100
    dims_low, dims_high = {}, {}
    for i, dim in enumerate(DIMS_AR):
        dim_sims = sim_vals[:, i] * 100
        dims_low[dim] = float(np.percentile(dim_sims, 2.5))
        dims_high[dim] = float(np.percentile(dim_sims, 97.5))
    chains = [np.random.choice(scores, size=len(scores), replace=True) for _ in range(4)]
    chains = np.array(chains)
    M, N = chains.shape[0], chains.shape[1]
    W = np.mean(np.var(chains, axis=1, ddof=1))
    B = N * np.var(np.mean(chains, axis=1), ddof=1)
    V = ((N-1)/N) * W + ((M+1)/(M*N)) * B
    rhat = np.sqrt(V/W) if W > 0 else 1.0
    return {"mean": float(np.mean(scores)), "ci_low": float(np.percentile(scores, 2.5)),
            "ci_high": float(np.percentile(scores, 97.5)), "risk": float(np.std(scores)/np.mean(scores)),
            "dims_low": dims_low, "dims_high": dims_high, "split_r_hat": float(rhat), "converged": rhat < 1.1}

_DEPENDENCY_MATRIX = {
    "السيادة المالية": {"المناعة السيبرانية": 0.20, "استقلالية الطاقة": 0.15, "الابتكار": 0.10},
    "استقلالية الطاقة": {"الأمن الغذائي": 0.25, "المناعة السيبرانية": 0.10},
    "المناعة السيبرانية": {"الحوكمة والامتثال": 0.30, "السيادة المالية": 0.15},
}

def calculate_ripple_effects(inputs, trigger_dim, delta=10.0):
    new_inputs = inputs.copy()
    new_inputs[trigger_dim] = max(0, min(100, new_inputs[trigger_dim] + delta))
    if trigger_dim in _DEPENDENCY_MATRIX:
        for dep, factor in _DEPENDENCY_MATRIX[trigger_dim].items():
            new_inputs[dep] = max(0, min(100, new_inputs[dep] + delta * factor))
    return {"trigger": trigger_dim, "delta": delta, "old_score": v_score(inputs),
            "new_score": v_score(new_inputs), "affected_dims": list(_DEPENDENCY_MATRIX.get(trigger_dim, {}).keys()),
            "new_inputs": new_inputs}

COMPLIANCE = {"NIST SP 800-53": {"المناعة السيبرانية": 90, "الحوكمة والامتثال": 80}}

def compliance_gaps(inputs, framework="NIST SP 800-53"):
    gaps = {}
    for dim, req in COMPLIANCE[framework].items():
        gaps[dim] = {"current": inputs[dim], "required": req, "gap": req - inputs[dim]}
    return gaps

def generate_strategic_advice(inputs, lang="ar"):
    score = v_score(inputs)
    weak_dims = sorted(inputs.items(), key=lambda x: x[1])[:3]
    if lang == "ar":
        summary = f"""
        المؤشر العام V-Score: {score:.1f}%
        • أضعف الأبعاد: {', '.join([d[0] for d in weak_dims])}
        """
    else:
        summary = f"""
        V-Score: {score:.1f}%
        Weakest: {', '.join([d[0] for d in weak_dims])}
        """
    return summary

def generate_pdf(score, dims, mc_data=None):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, f"NARMER Report - V-Score: {score:.2f}%", ln=1, align="C")
    for dim, val in dims.items():
        pdf.cell(0, 10, f"{dim}: {val:.1f}%", ln=1)
    f = BytesIO()
    pdf.output(f)
    return f.getvalue()

def run_unit_tests():
    if os.path.exists("test_engine.py"):
        result = subprocess.run(["python", "-m", "pytest", "test_engine.py", "-v"], capture_output=True, text=True)
        return result.stdout + result.stderr
    return "No tests found."

def main():
    init_db()
    if "lang" not in st.session_state:
        st.session_state.lang = "ar"
    lang = st.session_state.lang
    check_auth()
    if "dim_values" not in st.session_state:
        st.session_state.dim_values = {d: 75.0 for d in DIMS_AR}
    if "advanced_result" not in st.session_state:
        st.session_state.advanced_result = None

    # اختيار مصفوفة الأبعاد حسب اللغة
    if lang == "ar":
        DIMS = DIMS_AR
    else:
        DIMS = DIMS_EN

    score_now = v_score(st.session_state.dim_values)
    bg = "radial-gradient(circle at 10% 20%, #0f1a2f, #0c0e17)" if score_now > 60 else "radial-gradient(circle at 10% 20%, #3a0a0a, #0c0e17)" if score_now < 50 else "radial-gradient(circle at 10% 20%, #1a2a1a, #0c0e17)"
    st.markdown(f"<style>.stApp{{background:{bg};}}</style>", unsafe_allow_html=True)

    col_t, col_user = st.columns([3,1])
    with col_t:
        st.title("🔱 NARMER v53.3")
    with col_user:
        st.markdown(f"**{st.session_state.get('username','')}** | {st.session_state.get('role','')}")
        if st.button(translate("Logout", lang)):
            st.session_state.authenticated = False
            st.rerun()

    with st.sidebar:
        lang = st.selectbox("🌐 Language", AVAILABLE_LANGS, index=AVAILABLE_LANGS.index(lang) if lang in AVAILABLE_LANGS else 0,
                            format_func=lambda x: {"ar":"العربية","en":"English","fr":"Français","es":"Español","de":"Deutsch","it":"Italiano","pt":"Português","ru":"Русский","zh-cn":"中文","ja":"日本語","ko":"한국어","hi":"हिन्दी","tr":"Türkçe","fa":"فارسی","ur":"اردو","id":"Indonesia","sw":"Kiswahili","ha":"Hausa","bn":"বাংলা","th":"ไทย","vi":"Tiếng Việt","nl":"Nederlands","pl":"Polski"}[x])
        st.session_state.lang = lang
        if st.button(translate("Reset", lang)):
            st.session_state.dim_values = {d: 75.0 for d in DIMS_AR}
            st.rerun()
        if st.button(translate("Run Unit Tests", lang)):
            st.code(run_unit_tests(), language="text")

    tabs = st.tabs([
        translate("Central Command", lang),
        translate("Ripple Effects", lang),
        translate("Compliance", lang),
        translate("AI Advisor", lang),
        translate("PDF Report", lang),
        translate("CSV Import", lang),
        translate("History", lang),
        translate("Scenarios", lang),
        translate("Conflict Map", lang)
    ])

    # تبويب القيادة المركزية
    with tabs[0]:
        cols = st.columns(4)
        for i, dim in enumerate(DIMS):
            with cols[i % 4]:
                # استخدم المفتاح العربي للقيمة المخزنة
                ar_dim = DIMS_AR[i]
                val = st.slider(dim, 0, 100, int(st.session_state.dim_values[ar_dim]), key=f"dim_{ar_dim}")
                st.session_state.dim_values[ar_dim] = float(val)
        if st.button(translate("Run MC Analysis", lang)):
            with st.spinner("..."):
                result = monte_carlo_analysis(json.dumps(st.session_state.dim_values))
                st.session_state.advanced_result = result
                add_audit("MC Analysis", f"Score:{score_now:.2f}", st.session_state.username)
                st.success(translate("Analysis Complete", lang))
                st.rerun()
        col1, col2 = st.columns(2)
        col1.metric(translate("V-Score", lang), f"{score_now:.2f}%")
        weakest = min(st.session_state.dim_values, key=st.session_state.dim_values.get)
        col2.markdown(f"**{translate('Weakest', lang)}:** {translate(weakest, lang)}")
        if st.session_state.advanced_result:
            mc = st.session_state.advanced_result
            st.metric(translate("Bootstrap R-hat", lang), f"{mc['split_r_hat']:.4f}",
                     delta=translate("Converged", lang) if mc['converged'] else translate("Not Converged", lang))

    # تبويب التأثيرات المتسلسلة
    with tabs[1]:
        trigger_dim = st.selectbox(translate("Trigger Dimension", lang), DIMS)
        delta = st.slider(translate("Delta", lang), -30, 30, 10)
        if st.button(translate("Calculate Ripple", lang)):
            ripple = calculate_ripple_effects(st.session_state.dim_values, trigger_dim, delta)
            st.metric(translate("Old V-Score", lang), f"{ripple['old_score']:.2f}")
            st.metric(translate("New V-Score", lang), f"{ripple['new_score']:.2f}",
                     delta=f"{ripple['new_score']-ripple['old_score']:+.2f}")

    # تبويب الامتثال
    with tabs[2]:
        framework = st.selectbox(translate("Framework", lang), list(COMPLIANCE.keys()))
        gaps = compliance_gaps(st.session_state.dim_values, framework)
        if gaps:
            df_gaps = pd.DataFrame([{translate("Dimension", lang): translate(k, lang), **v} for k, v in gaps.items()])
            st.dataframe(df_gaps, use_container_width=True)

    # تبويب المستشار
    with tabs[3]:
        if st.button(translate("Get Advice", lang)):
            st.markdown(generate_strategic_advice(st.session_state.dim_values, lang))

    # تبويب PDF
    with tabs[4]:
        if st.button(translate("Generate PDF", lang)):
            pdf_bytes = generate_pdf(score_now, st.session_state.dim_values)
            st.download_button(label=translate("Download PDF", lang), data=pdf_bytes, file_name="Narmer_Report.pdf")

    # تبويب CSV
    with tabs[5]:
        uploaded = st.file_uploader(translate("Upload CSV", lang), type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
            if len(df.columns) >= 2:
                dims_map = dict(zip(df.iloc[:,0].astype(str), df.iloc[:,1].astype(float)))
                st.session_state.dim_values.update(dims_map)
                st.success(translate("CSV Loaded", lang))
                st.rerun()

    # تبويب التاريخ
    with tabs[6]:
        hist = get_history(30)
        if not hist.empty:
            st.line_chart(hist.set_index("timestamp")["score"])

    # تبويب السيناريوهات
    with tabs[7]:
        name = st.text_input(translate("Scenario Name", lang))
        if st.button(translate("Save Scenario", lang)):
            save_scenario(name, st.session_state.dim_values, score_now)
            st.success(translate("Scenario Saved", lang))
        scenarios = get_scenarios()
        if not scenarios.empty:
            sel = st.selectbox(translate("Load Scenario", lang), scenarios["name"])
            if st.button(translate("Load", lang)):
                row = scenarios[scenarios["name"]==sel].iloc[0]
                st.session_state.dim_values = json.loads(row["dimensions"])
                st.rerun()

    # تبويب خريطة النزاعات
    with tabs[8]:
        conflict_zones = pd.DataFrame({
            translate("Region", lang): ["Ukraine", "Gaza", "Sudan", "Yemen"],
            "latitude": [48.3794, 31.5, 15.5, 15.5],
            "longitude": [31.1656, 34.4, 30.5, 48.5],
            translate("Intensity", lang): [95, 90, 85, 80]
        })
        st.map(conflict_zones, latitude="latitude", longitude="longitude", size=translate("Intensity", lang))

if __name__ == "__main__":
    main()
'@ | Set-Content app.py -Encoding UTF8