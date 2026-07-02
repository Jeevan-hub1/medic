import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import auth
from database import get_db

router = APIRouter(
    prefix="/video",
    tags=["video"]
)

def generate_random_room_id(length=12):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@router.post("/create-room")
def create_consultation_room(
    appt_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify appointment exists and belongs to user
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    room_id = f"medisahayak-{appt_id}-{generate_random_room_id()}"
    room_url = f"https://meet.jit.si/{room_id}"
    
    # Save the room link in the notes/details or send in notification
    appt.notes = f"{appt.notes or ''}\n[Video Link: {room_url}]"
    db.commit()
    
    # Send a notification to the patient that the doctor created a call
    notification = models.Notification(
        user_id=appt.patient_id,
        title="Video Call Room Ready",
        body=f"Doctor is ready for your consultation. Click here to join the video room: {room_url}"
    )
    db.add(notification)
    db.commit()
    
    return {
        "room_id": room_id,
        "room_url": room_url,
        "appointment_id": appt_id
    }
