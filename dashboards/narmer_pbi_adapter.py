import pandas as pd
import requests
import urllib3

# تجاهل تحذيرات SSL في البيئات المحلية
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# عنوان المصفوفة المشفر (الحصن)
URL = "https://localhost/assess"
HEADERS = {"Authorization": "Bearer YOUR_JWT_TOKEN"}

# بيانات تجريبية لمحاكاة الطلب
payload = {
    "dimensions": {
        "Geopolitical_Stability": 85,
        "Economic_Sovereignty": 78,
        "Cyber_Defense": 92,
        "Resource_Management": 88,
        "Social_Cohesion": 80,
        "Historical_Identity": 95
    }
}

try:
    # جلب البيانات من محرك نارمر
    response = requests.post(URL, json=payload, headers=HEADERS, verify=False)
    data = response.json()
    
    # تحويل النتائج إلى جدول لـ Power BI
    df = pd.DataFrame([data])
    print(df)
except Exception as e:
    print(f"Connection Error: {e}")