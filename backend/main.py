from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from database import engine, SessionLocal
import models

# Import routers
from routers import (
    auth_router,
    chat_router,
    report_router,
    prediction_router,
    recommendation_router,
    appointments_router,
    notifications_router,
    video_router,
    maps_router
)

# Initialize DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MediSahayak API",
    description="Backend API for MediSahayak (formerly Sanjeevani) healthcare platform",
    version="1.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(report_router.router)
app.include_router(prediction_router.router)
app.include_router(recommendation_router.router)
app.include_router(appointments_router.router)
app.include_router(notifications_router.router)
app.include_router(video_router.router)
app.include_router(maps_router.router)

# Seed sample data (Doctors and Users) on startup if empty
def seed_data():
    db = SessionLocal()
    try:
        # Check if doctors exist
        count = db.query(models.Doctor).count()
        if count == 0:
            print("Seeding sample doctor users and profiles...")
            # Import auth to hash passwords
            import auth
            hashed_pwd = auth.get_password_hash("doctor123")
            
            # Sample doctors data
            doctors_data = [
                {"name": "Dr. Ananya Sharma", "email": "ananya@medisahayak.com", "specialty": "Gynecology", "hospital": "City Maternity Hospital", "languages": "English, Hindi, Bengali"},
                {"name": "Dr. Rajesh Iyer", "email": "rajesh@medisahayak.com", "specialty": "Pulmonology", "hospital": "Metro Heart and Lung Institute", "languages": "English, Tamil, Telugu"},
                {"name": "Dr. Vikram Seth", "email": "vikram@medisahayak.com", "specialty": "Orthopedics", "hospital": "Apex Bone & Joint Clinic", "languages": "English, Hindi, Punjabi"},
                {"name": "Dr. Priya Sen", "email": "priya@medisahayak.com", "specialty": "Pediatrics", "hospital": "Care Child Clinic", "languages": "English, Hindi, Odia"},
                {"name": "Dr. Amit Roy", "email": "amit@medisahayak.com", "specialty": "Oncology", "hospital": "Regional Cancer Centre", "languages": "English, Bengali, Hindi"},
                {"name": "Dr. Sneha Patil", "email": "sneha@medisahayak.com", "specialty": "Psychiatry", "hospital": "Mind Care Clinic", "languages": "English, Marathi, Gujarati"}
            ]
            
            for doc in doctors_data:
                # 1. Create User account
                user = models.User(
                    name=doc["name"],
                    email=doc["email"],
                    password_hash=hashed_pwd,
                    role="doctor",
                    state="Karnataka",
                    district="Bengaluru"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                
                # 2. Create Doctor profile
                doctor_profile = models.Doctor(
                    user_id=user.id,
                    specialty=doc["specialty"],
                    license_no=f"MCIM-{random_lic_num()}",
                    hospital=doc["hospital"],
                    rating=4.7,
                    available=True,
                    languages=doc["languages"]
                )
                db.add(doctor_profile)
                db.commit()
                
            print("Doctors seeding completed.")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

def random_lic_num():
    import random
    return random.randint(10000, 99999)

@app.on_event("startup")
async def startup_event():
    seed_data()

# Serve the frontend website as static files at /app
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "Sanjeevani Website")
if os.path.exists(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/")
def home():
    return RedirectResponse(url="/app")

@app.get("/api")
def api_status():
    return {"message": "Welcome to MediSahayak Healthcare API", "status": "active", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

from pydantic import BaseModel
class ArtemayaQuery(BaseModel):
    query: str

@app.post("/chat")
def artemaya_chat(req: ArtemayaQuery):
    from ai.chatbot import generate_chat_response
    reply = generate_chat_response(req.query, [])
    return {"response": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
