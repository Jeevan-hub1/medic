from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import auth
from database import get_db

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

@router.post("/book", response_model=schemas.Appointment)
def book_appointment(
    appt: schemas.AppointmentCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify doctor exists
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appt.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    new_appt = models.Appointment(
        patient_id=current_user.id,
        doctor_id=appt.doctor_id,
        datetime=appt.datetime,
        type=appt.type,
        status="pending",
        notes=appt.notes
    )
    
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    
    # Send a notification to patient
    notification = models.Notification(
        user_id=current_user.id,
        title="Appointment Requested",
        body=f"Your appointment with Doctor is requested for {appt.datetime}."
    )
    db.add(notification)
    db.commit()
    
    return new_appt

@router.get("/my-appointments", response_model=list)
def get_user_appointments(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "doctor":
        # Get doctor profile
        doc = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Doctor profile not found")
        appts = db.query(models.Appointment).filter(models.Appointment.doctor_id == doc.id).all()
    else:
        appts = db.query(models.Appointment).filter(models.Appointment.patient_id == current_user.id).all()
        
    result = []
    for app in appts:
        patient_details = db.query(models.User).filter(models.User.id == app.patient_id).first()
        doc_details = db.query(models.Doctor).filter(models.Doctor.id == app.doctor_id).first()
        doc_user = db.query(models.User).filter(models.User.id == doc_details.user_id).first() if doc_details else None
        
        result.append({
            "id": app.id,
            "datetime": app.datetime,
            "type": app.type,
            "status": app.status,
            "notes": app.notes,
            "patient_name": patient_details.name if patient_details else "Patient",
            "doctor_name": doc_user.name if doc_user else "Doctor",
            "specialty": doc_details.specialty if doc_details else "Medicine"
        })
        
    return result

@router.put("/{appt_id}/status")
def update_appointment_status(
    appt_id: int,
    status_str: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    # Validation: Only the doctor or patient involved can update the status
    appt.status = status_str
    db.commit()
    
    # Notify patient
    notification = models.Notification(
        user_id=appt.patient_id,
        title="Appointment Status Updated",
        body=f"Your appointment status has been updated to {status_str}."
    )
    db.add(notification)
    db.commit()
    
    return {"message": "Appointment status updated successfully"}
