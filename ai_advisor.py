import os
import requests

class AISovereignAdvisor:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY is not set in .env")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate_advice(self, v_score: float) -> str:
        prompt = f"<s>[INST] أنت مستشار استراتيجي في 'مصفوفة نارمر السيادية'. قيمة المخاطرة الحالية {v_score:.2f}% (من 100%). قدم توصية استراتيجية مكونة من 3-4 جمل بالعربية الفصحى، تركز على رؤية الإمارات 2030. [/INST]"
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            return data[0]['generated_text'].strip()
        except Exception as e:
            return f"تعذر الاتصال بمحرك الذكاء الاصطناعي. السبب: {str(e)}"