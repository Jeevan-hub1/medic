from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "patient"
    state: Optional[str] = None
    district: Optional[str] = None

class UserCreate(UserBase):
    password: str
    aadhaar_hash: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Doctor Schemas
class DoctorBase(BaseModel):
    specialty: str
    license_no: str
    hospital: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    rating: float = 4.5
    available: bool = True
    languages: str = "English, Hindi"

class DoctorCreate(DoctorBase):
    user_id: int

class Doctor(DoctorBase):
    id: int
    user_id: int
    user: User

    class Config:
        from_attributes = True

# Appointment Schemas
class AppointmentBase(BaseModel):
    doctor_id: int
    datetime: str
    type: str = "online"  # online, offline
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    patient_id: int
    status: str
    
    class Config:
        from_attributes = True

# Health Report Schemas
class HealthReportBase(BaseModel):
    file_path: str
    analysis_json: str

class HealthReport(HealthReportBase):
    id: int
    user_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    session_id: int

class ChatMessageBase(BaseModel):
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    title: str
    body: str

class Notification(NotificationBase):
    id: int
    user_id: int
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Prescription Schemas
class PrescriptionBase(BaseModel):
    appointment_id: int
    medicines_json: str

class Prescription(PrescriptionBase):
    id: int
    issued_at: datetime

    class Config:
        from_attributes = True
