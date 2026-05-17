import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BACKEND_URL = "http://backend:8000"
st.set_page_config(page_title="NARMER", page_icon="🔱", layout="wide")
st.title("🔱 NARMER SOVEREIGN MATRIX v17.0 Enterprise")
access = st.text_input("رمز الوصول", type="password")
if access != "NARMER-2026": st.stop()
dims = ["الحوكمة والامتثال","سلاسل الإمداد","رأس المال البشري","القوة العسكرية","الدبلوماسية","استقلالية الموارد","المناعة السيبرانية","البنية التحتية الرقمية","الاستقرار الاجتماعي","الابتكار","السيادة المالية"]
inputs = {}
cols = st.columns(3)
for i,d in enumerate(dims):
    with cols[i%3]: inputs[d] = st.slider(d,0,100,75)
if st.button("تقييم"):
    res = requests.post(f"{BACKEND_URL}/api/v1/assess", json={"dimensions":inputs})
    if res.ok:
        data = res.json()
        st.metric("V-Score", f"{data['v_score']:.2f}")
        df = pd.DataFrame(list(inputs.items()), columns=["Dimension","Value"])
        fig = px.line_polar(df, r='Value', theta='Dimension', line_close=True, template="plotly_dark")
        fig.update_traces(fill='toself', line_color='#f4d35e')
        st.plotly_chart(fig, use_container_width=True)
