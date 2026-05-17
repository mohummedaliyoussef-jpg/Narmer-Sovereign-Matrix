@echo off
echo تشغيل مخطط السيادة العالمي...
start python global_sovereignty_chart.py
timeout /t 3
echo تشغيل لوحة مراقبة الأداء...
start python performance_dashboard.py
echo تم تشغيل جميع المكونات!
pause