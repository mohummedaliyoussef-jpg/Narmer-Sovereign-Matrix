import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import urllib3
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# تعطيل تحذيرات SSL الخاصة بالشهادات المحلية لتأمين قنوات الاتصال الداخلية بنقاء
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# دالة مساعدة لضبط وتصحيح النصوص العربية في الرسوم البيانية لـ Plotly
def ar_text(text):
    return get_display(reshape(text))

# 1. تهيئة إعدادات الصفحة وهوية المنصة السيادية المطور
st.set_page_config(
    page_title="🔱 NARMER v56.0 – Ultimate Sovereign Engine",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة مخصصة بالـ CSS لتنسيق النصوص العربية والمحاذاة والـ Dark Theme
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: rtl; }
    .stMarkdown, .stText, .stTitle, h1, h2, h3, h4, h5, h6, p { text-align: right; direction: rtl; }
    div.stButton > button:first-child { background-color: #d4af37; color: black; font-weight: bold; width: 100%; border-radius: 8px; border: none; }
    div.stButton > button:first-child:hover { background-color: #bfa030; color: white; }
    .metric-box { padding: 20px; background-color: #1e1e1e; border-radius: 10px; border-right: 5px solid #d4af37; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. العناوين المركزية للوحة التحكم الشاملة
st.title("🔱 مصفوفة نارمر v56.0 – الإمبراطور النهائي")
st.subheader("🏛️ مركز قيادة منصة عـصـام السيادية | ASAAS Sovereign Engine")
st.write("**المستخدم الحالي:** admin | **الدور:** مدير سيادي معتمد (JWT Secured)")
st.markdown("---")

# 3. القائمة الجانبية (Sidebar) لحقن المتغيرات الـ 17 ومحاكاة الصدمات
st.sidebar.header("🎛️ غرفة التحكم بالمدخلات")

st.sidebar.markdown("### 📊 تقييم الأبعاد الـ 17 الحالية:")

with st.sidebar.expander("🏛️ أبعاد الحوكمة والأمن الأساسي", expanded=True):
    gov = st.sidebar.slider("الحوكمة والامتثال", 0.0, 100.0, 75.0, step=5.0)
    supply = st.sidebar.slider("سلاسل الإمداد", 0.0, 100.0, 60.0, step=5.0)
    food = st.sidebar.slider("الأمن الغذائي", 0.0, 100.0, 70.0, step=5.0)
    env = st.sidebar.slider("الاستدامة البيئية", 0.0, 100.0, 65.0, step=5.0)
    health = st.sidebar.slider("الأمن الصحي", 0.0, 100.0, 80.0, step=5.0)

with st.sidebar.expander("🛡️ القوة العسكرية والسيادة التكنولوجية", expanded=False):
    military = st.sidebar.slider("القوة العسكرية", 0.0, 100.0, 90.0, step=5.0)
    space = st.sidebar.slider("السيادة الفضائية", 0.0, 100.0, 55.0, step=5.0)
    cyber = st.sidebar.slider("المناعة السيبرانية", 0.0, 100.0, 85.0, step=5.0)
    ai = st.sidebar.slider("سيادة الذكاء الاصطناعي", 0.0, 100.0, 70.0, step=5.0)
    digital = st.sidebar.slider("البنية التحتية الرقمية", 0.0, 100.0, 75.0, step=5.0)

with st.sidebar.expander("💰 رأس المال والقدرات الناعمة", expanded=False):
    human = st.sidebar.slider("رأس المال البشري", 0.0, 100.0, 70.0, step=5.0)
    innovation = st.sidebar.slider("الابتكار", 0.0, 100.0, 65.0, step=5.0)
    financial = st.sidebar.slider("السيادة المالية", 0.0, 100.0, 70.0, step=5.0)
    diplomacy = st.sidebar.slider("الدبلوماسية", 0.0, 100.0, 80.0, step=5.0)
    energy = st.sidebar.slider("استقلالية الطاقة", 0.0, 100.0, 75.0, step=5.0)
    social = st.sidebar.slider("الاستقرار الاجتماعي", 0.0, 100.0, 85.0, step=5.0)
    soft = st.sidebar.slider("القوة الناعمة", 0.0, 100.0, 75.0, step=5.0)

st.sidebar.markdown("---")

# 4. محاكي "ماذا لو" التفاعلي (What-If Simulation Engine) لحقن الصدمات
st.subheader("🔮 محاكي السيناريوهات والصدمات التكيفي (What-If Simulator)")

scenarios_pool = {
    "بدون تهديد (الوضع الطبيعي)": "🟢 المنظومة تعمل في بيئة مستقرة تكتيكياً ومحمية بالكامل.",
    "هجوم سيبراني منسق على البنية التحتية 🚨": "سقوط مفاجئ في [المناعة السيبرانية] و [البنية التحتية الرقمية] بمقدار 40 درجة.",
    "إغلاق ممر لوجستي بحري حرجي 🌊": "انهيار [سلاسل الإمداد] بمقدار 50 درجة مع تهديد مباشر لـ [الأمن الغذائي].",
    "أزمة مالية وعقوبات اقتصادية دولية 💰": "تراجع [السيادة المالية] بمقدار 35 درجة وضربة موازية لـ [الابتكار].",
    "صراع عسكري حدودي مفاجئ ⚔️": "استنفار [القوة العسكرية] للقصوى، مع هبوط اضطراري في [الاستقرار الاجتماعي]."
}

selected_scenario = st.selectbox("🚨 اختر سيناريو الصدمة الطارئة لحقنه في محرك نارمر:", list(scenarios_pool.keys()))
st.info(f"**التحليل المسبق للصدمة:** {scenarios_pool[selected_scenario]}")

# الاستجابة الحية لتغيير قيم السلايدرز تلقائياً بناء على نوع الصدمة المحقونة
if selected_scenario == "هجوم سيبراني منسق على البنية التحتية 🚨":
    cyber = max(0.0, cyber - 40.0)
    digital = max(0.0, digital - 40.0)
elif selected_scenario == "إغلاق ممر لوجستي بحري حرجي 🌊":
    supply = max(0.0, supply - 50.0)
    food = max(0.0, food - 30.0)
elif selected_scenario == "أزمة مالية وعقوبات اقتصادية دولية 💰":
    financial = max(0.0, financial - 35.0)
    innovation = max(0.0, innovation - 20.0)
elif selected_scenario == "صراع عسكري حدودي مفاجئ ⚔️":
    military = min(100.0, military + 10.0)
    social = max(0.0, social - 30.0)

st.markdown("---")
trigger_assessment = st.button("⚙️ إطلاق معالجة محاكاة السيناريو السيادي (Execute)")

# العناوين والمسارات الموحدة داخل حاويات الدوكر عبر البوابة الأمنية
BACKEND_TOKEN_URL = "http://web:8000/token"
BACKEND_ASSESS_URL = "http://web:8000/assess/"

# 5. منطق المعالجة وعرض المخرجات عند الضغط على زر التنفيذ
if trigger_assessment:
    with st.spinner("⏳ جاري استدعاء مصفوفة نارمر v56.0 وحساب الأوزان التكيفية..."):
        try:
            # أولاً: توليد العبور الصامت والتسجيل عبر الـ JWT لمفتاح المسؤول المأمون
            token_response = requests.post(
                BACKEND_TOKEN_URL, 
                data={"username": "admin", "password": "admin123"}, 
                verify=False, 
                timeout=5
            )
            
            if token_response.status_code == 200:
                access_token = token_response.json()["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                
                # ثانياً: تجهيز حمولة الـ 17 بعداً الكاملة لإرسالها لنواة المحرك
                payload_data = {
                    "الحوكمة والامتثال": gov, "سلاسل الإمداد": supply, "الأمن الغذائي": food,
                    "الاستدامة البيئية": env, "الأمن الصحي": health, "القوة العسكرية": military,
                    "رأس المال البشري": human, "الابتكار": innovation, "السيادة الفضائية": space,
                    "المناعة السيبرانية": cyber, "السيادة المالية": financial, "الدبلوماسية": diplomacy,
                    "سيادة الذكاء الاصطناعي": ai, "البنية التحتية الرقمية": digital, "استقلالية الطاقة": energy,
                    "الاستقرار الاجتماعي": social, "القوة الناعمة": soft,
                    "سيناريو طارئ": selected_scenario
                }

                # استدعاء نقطة المعالجة المركزية المحمية
                response = requests.post(BACKEND_ASSESS_URL, json=payload_data, headers=headers, verify=False, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    v_score = result["v_score"]
                    resilience = result["resilience"]
                    anomalies = result["anomalies_count"]
                    weakest = result["weakest_dimension"]
                    processed_dims = result["dimensions_processed"]

                    # --- تخطيط الواجهة: المؤشرات السريعة الأربعة ---
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    col_m1.metric(label="📊 V-Score الشامل", value=f"{v_score}%")
                    col_m2.metric(label="🛡️ معامل المرونة الوطنية", value=f"{resilience}%")
                    col_m3.metric(label="⚠️ مؤشرات الشذوذ (Z-Score)", value=anomalies)
                    col_m4.metric(label="📉 أضعف بعد استراتيجي", value=weakest)

                    st.markdown("---")

                    # --- تخطيط صف العداد والرادارات الرسومية ---
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.markdown("### 🛡️ مؤشر الحصانة السيادية الإجمالي")
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=v_score,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': ar_text(f"أضعف بعد: {weakest}"), 'font': {'size': 14}},
                            gauge={
                                'axis': {'range': [None, 100], 'tickwidth': 1},
                                'bar': {'color': "#d4af37"}, # ذهبي سيادي
                                'bgcolor': "#222222",
                                'steps': [
                                    {'range': [0, 50], 'color': '#8b0000'}, # أحمر خطر
                                    {'range': [50, 75], 'color': '#e5a93b'}, # أصفر حذر
                                    {'range': [75, 100], 'color': '#006400'} # أخضر آمن
                                ],
                            }
                        ))
                        fig_gauge.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig_gauge, use_container_width=True)

                    with col2:
                        st.markdown("### 📊 تحليل انتشار القوة في مصفوفة نارمر")
                        # تحويل قيم الأبعاد المعالجة إلى رسم بياني شريطي مبهج للمقارنة السريعة
                        df_dims = pd.DataFrame({
                            'البُعد الاستراتيجي': [ar_text(k) for k in processed_dims.keys()],
                            'المستوى الحالي': list(processed_dims.values())
                        }).sort_values(by='المستوى الحالي', ascending=True)

                        fig_bars = go.Figure(data=[go.Bar(
                            x=df_dims['المستوى الحالي'],
                            y=df_dims['البُعد الاستراتيجي'],
                            orientation='h',
                            marker=dict(color=df_dims['المستوى الحالي'], colorscale='Viridis')
                        )])
                        fig_bars.update_layout(
                            margin=dict(l=20, r=20, t=10, b=10),
                            height=320,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_bars, use_container_width=True)

                    st.markdown("---")

                    # --- صف التوصيات والقرارات الاستراتيجية للمستشار الذكي ---
                    st.subheader("🧠 مركز التوجيه الاستراتيجي اللحظي لمصفوفة نارمر:")
                    for rec in result["strategic_recommendations"]:
                        st.success(rec)

                else:
                    st.error("❌ فشل المحرك المركزي في معالجة الحسابات الرياضية المتقدمة للمصفوفة.")
            else:
                st.error("❌ فشل بوابة التفتيش والولوج المشفر (JWT Auth Fail). تواصل مع مركز الحوكمة.")
        
        except Exception as e:
            st.error(f"🚨 خطأ في الاتصال بالشبكة السيادية الداخلية للحاويات: {str(e)}")
else:
    st.markdown("""
    <div class='metric-box'>
        <h3>👋 مرحباً بك في مركز العمليات المركزي المدمج (v56.0)</h3>
        <p>تم دمج لوحة القيادة بنجاح مع النواة الأمنية المشفرة. قم بضبط وتحريك قيم الأبعاد الـ 17 من اللوحة الجانبية، أو قم باختيار إحدى الصدمات والتهديدات الطارئة من <b>محاكي ماذا لو</b>، ثم اضغط على زر <b>إطلاق المعالجة</b> لتفعيل القوة الحسابية للمحرك السيادي فوراً.</p>
    </div>
    """, unsafe_allow_html=True)