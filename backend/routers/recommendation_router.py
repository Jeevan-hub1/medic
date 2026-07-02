from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import models
import auth
from database import get_db
from ai.recommender import match_specialty_from_symptoms, get_diet_recommendations_by_phase

router = APIRouter(
    prefix="/recommend",
    tags=["recommendations"]
)

@router.get("/doctors")
def recommend_doctors(
    symptoms: str = Query(..., description="User symptoms text"),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    specialty = match_specialty_from_symptoms(symptoms)
    
    # Query doctors matching the specialty
    doctors = db.query(models.Doctor).filter(
        models.Doctor.specialty == specialty
    ).all()
    
    # If no doctor matches, fallback to general list
    if not doctors:
        doctors = db.query(models.Doctor).limit(5).all()
        
    result = []
    for doc in doctors:
        # Fetch doctor's user details
        user_details = db.query(models.User).filter(models.User.id == doc.user_id).first()
        result.append({
            "id": doc.id,
            "name": user_details.name if user_details else "Doctor",
            "specialty": doc.specialty,
            "hospital": doc.hospital,
            "rating": doc.rating,
            "available": doc.available,
            "languages": doc.languages
        })
        
    return {
        "matched_specialty": specialty,
        "doctors": result
    }

@router.get("/diet")
def recommend_diet(
    phase: str = Query(..., description="Menstrual phase (Menstrual, Follicular, Ovulation, Luteal)"),
    current_user: models.User = Depends(auth.get_current_user)
):
    recs = get_diet_recommendations_by_phase(phase)
    return {
        "phase": phase,
        "recommendations": recs
    }

@router.get("/medicines")
def recommend_medicines(
    symptom: str = Query(..., description="Core symptom"),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Safe general guidelines for OTC medicine suggestions + doctor advice
    meds_db = {
        "fever": ["Paracetamol (500mg/650mg) - Reduces fever and body aches.", "Aspirin/Ibuprofen (Consult doctor before use)"],
        "cold": ["Cetirizine - Controls running nose/sneezing.", "Decongestants (e.g. Pseudoephedrine)"],
        "cough": ["Dextromethorphan (Dry Cough) - Cough suppressant syrup.", "Guaifenesin (Wet Cough) - Expectorant syrup."],
        "pain": ["Ibuprofen - Anti-inflammatory pain relief.", "Diclofenac Gel - For local muscle/joint pain application."]
    }
    
    symptom_lower = symptom.lower()
    matched_meds = []
    for key, val in meds_db.items():
        if key in symptom_lower:
            matched_meds = val
            break
            
    if not matched_meds:
        matched_meds = ["No specific OTC suggestions available. Please consult a qualified pharmacist or physician."]
        
    return {
        "symptom": symptom,
        "otc_suggestions": matched_meds,
        "note": "Disclaimer: This is for educational context. Always verify with a healthcare provider before taking any medicine."
    }
