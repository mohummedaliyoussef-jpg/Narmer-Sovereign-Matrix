# استخدام نسخة بايثون خفيفة ومستقرة لبيئة سريعة
FROM python:3.11-slim

# منع بايثون من كتابة ملفات الـ pyc وضمان خروج المخرجات فوراً للـ logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# تثبيت الحزم الأساسية للعرض الرسومي والاتصال
RUN pip install --no-cache-dir streamlit requests plotly pandas

# نسخ كود الواجهة الأمامية بالكامل
COPY . /app

# فتح المنفذ الافتراضي لـ Streamlit
EXPOSE 8501

# إقلاع واجهة العرض مع تعطيل حماية الـ CORS لضمان مرونة العبور عبر البروكسي
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]