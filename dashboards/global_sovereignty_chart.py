import plotly.express as px
import pandas as pd

# البيانات التي جمعناها اليوم من البنك الدولي
data = {
    'Region': ['Middle East', 'Asia', 'Africa', 'Americas', 'Europe'],
    'V-Score': [88.5, 95.2, 85.0, 98.1, 94.4],
    'Impact Weight': [0.75, 0.20, 0.15, 0.20, 0.20]
}

df = pd.DataFrame(data)

# إنشاء مخطط تفاعلي (Scatter Bubble Chart)
fig = px.scatter(
    df,
    x="Region",
    y="V-Score",
    size="Impact Weight",
    color="Region",
    hover_name="Region",
    size_max=60,
    title="🌐 Global Sovereignty Matrix – Narmer v56.0"
)

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#0e1117',
    plot_bgcolor='#0e1117',
    font=dict(color='#FFD700', size=14),
    title_font=dict(size=22)
)

# عرض المخطط في Plotly Studio (المتصفح الافتراضي)
fig.show()