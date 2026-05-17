@"
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import uuid
from app.core.engine import NarmerEngine
from app.services.ai_advisor import AISovereignAdvisor

router = APIRouter()

# تعريف نموذج الطلب
class AssessmentRequest(BaseModel):
    dimensions: dict[str, float]

# أوزان افتراضية للمحرك (يمكن تعديلها حسب التكوين)
DEFAULT_WEIGHTS = {
    "product_quality": 0.25,
    "operational_efficiency": 0.25,
    "market_risk": 0.25,
    "financial_stability": 0.25
}

@router.post("/assess")
async def assess(request: AssessmentRequest):
    # 1. حساب v_score باستخدام المحرك
    engine = NarmerEngine(DEFAULT_WEIGHTS)
    v_score = engine.calculate_v_score(request.dimensions)

    # 2. محاكاة مونت كارلو (بسيطة)
    simulations = 1000
    noise = np.random.normal(0, 2.0, simulations)
    simulated_scores = np.clip(v_score + noise, 0.0, 100.0)
    monte_carlo = {
        "mean": float(np.mean(simulated_scores)),
        "ci_95": [float(np.percentile(simulated_scores, 2.5)), float(np.percentile(simulated_scores, 97.5))],
        "risk": float(np.std(simulated_scores) / 100.0)
    }

    # 3. معرف تدقيق فريد
    audit_id = str(uuid.uuid4())

    # 4. استدعاء الذكاء الاصطناعي للحصول على توصية
    try:
        advisor = AISovereignAdvisor()
        ai_advice = advisor.generate_advice(v_score)
    except Exception as e:
        ai_advice = f"تعذر توليد توصية ذكية: {str(e)}"

    return {
        "v_score": v_score,
        "monte_carlo": monte_carlo,
        "audit_id": audit_id,
        "ai_advice": ai_advice,
        "advisor_version": "Jais-Sovereign-v1"
    }
"@ | Out-File -FilePath "C:\Users\ip\narmer_enterprise\backend\app\api\endpoints\score.py" -Encoding utf8