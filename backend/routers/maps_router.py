import os
import requests
from fastapi import APIRouter, Query, Depends
import models
import auth

router = APIRouter(
    prefix="/maps",
    tags=["maps"]
)

# Set a mock list of Indian PHCs/Hospitals as fallback if key is missing
MOCK_HOSPITALS = [
    {"name": "MediSahayak Primary Health Centre (PHC)", "lat_offset": 0.005, "lng_offset": 0.003, "rating": 4.6, "address": "Sector 3, Local Area Clinic"},
    {"name": "Apollo Clinic Rural Outreach", "lat_offset": -0.007, "lng_offset": 0.009, "rating": 4.4, "address": "Main Bazar Cross Road"},
    {"name": "Government Community Health Centre", "lat_offset": 0.012, "lng_offset": -0.008, "rating": 4.1, "address": "Opposite Railway Station"},
    {"name": "Red Cross Rural Hospital", "lat_offset": -0.002, "lng_offset": -0.005, "rating": 4.5, "address": "National Highway 4, near Toll Plaza"},
    {"name": "Amrit Medical Hall and Clinic", "lat_offset": 0.009, "lng_offset": 0.011, "rating": 4.2, "address": "Market complex, Ground floor"}
]

@router.get("/hospitals")
def get_nearby_hospitals(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    current_user: models.User = Depends(auth.get_current_user)
):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        # Generate mock hospitals relative to current coordinates for demo
        hospitals = []
        for index, item in enumerate(MOCK_HOSPITALS):
            hospitals.append({
                "id": f"mock_hospital_{index}",
                "name": item["name"],
                "lat": lat + item["lat_offset"],
                "lng": lng + item["lng_offset"],
                "rating": item["rating"],
                "address": item["address"]
            })
        return {"hospitals": hospitals, "source": "simulated_local_database"}
        
    # Real Google Places search
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={api_key}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        results = data.get("results", [])
        
        hospitals = []
        for r in results:
            loc = r.get("geometry", {}).get("location", {})
            hospitals.append({
                "id": r.get("place_id"),
                "name": r.get("name"),
                "lat": loc.get("lat"),
                "lng": loc.get("lng"),
                "rating": r.get("rating", 4.2),
                "address": r.get("vicinity")
            })
        return {"hospitals": hospitals, "source": "google_places_api"}
    except Exception:
        # Fallback if connection fails
        hospitals = []
        for index, item in enumerate(MOCK_HOSPITALS):
            hospitals.append({
                "id": f"mock_hospital_{index}",
                "name": item["name"],
                "lat": lat + item["lat_offset"],
                "lng": lng + item["lng_offset"],
                "rating": item["rating"],
                "address": item["address"]
            })
        return {"hospitals": hospitals, "source": "simulated_local_database_fallback"}
