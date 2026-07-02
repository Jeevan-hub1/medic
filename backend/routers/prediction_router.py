from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import models
import auth
from ai.predictor import predict_disease_from_symptoms

router = APIRouter(
    prefix="/predict",
    tags=["prediction"]
)

class SymptomRequest(BaseModel):
    symptoms: List[str]
    context: Optional[str] = ""

@router.post("/disease")
def get_disease_prediction(
    req: SymptomRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    if not req.symptoms:
        raise HTTPException(status_code=400, detail="Symptoms list cannot be empty")
        
    prediction = predict_disease_from_symptoms(
        symptoms=req.symptoms,
        health_context=req.context
    )
    return prediction
