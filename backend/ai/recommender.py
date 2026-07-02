def match_specialty_from_symptoms(symptoms_text: str) -> str:
    """
    Predict medical specialty based on symptom text
    """
    text = symptoms_text.lower()
    
    # Simple mapping keywords
    mappings = {
        "gynecology": ["period", "menstrual", "pregnant", "pregnancy", "gyne", "ovary", "uterus", "pcos", "pcod"],
        "psychiatry": ["depressed", "anxiety", "mental", "stress", "sleep", "hallucination", "mood", "psych"],
        "pulmonogy": ["lung", "breathing", "cough", "chest pain", "asthma", "breath", "oxygen"],
        "orthopedics": ["bone", "fracture", "joint", "muscle", "back pain", "knee", "spine"],
        "pediatrics": ["child", "baby", "infant", "vaccine", "growth", "pediatric"],
        "oncology": ["cancer", "tumor", "chemo", "growth", "biopsy", "lump"]
    }
    
    for specialty, keywords in mappings.items():
        if any(keyword in text for keyword in keywords):
            return specialty.capitalize()
            
    # Default fallback
    return "General Medicine"

def get_diet_recommendations_by_phase(phase: str) -> dict:
    """
    Provide recommendations for diet based on menstrual phase
    """
    phase_data = {
        "menstrual": {
            "focus": "Iron & hydration",
            "foods": "Spinach, lentils, dark chocolate, ginger tea, beetroot",
            "avoid": "Cold foods, high sodium, excess caffeine"
        },
        "follicular": {
            "focus": "Energy & light fresh produce",
            "foods": "Sprouted salads, citrus fruits, broccoli, lean protein, nuts",
            "avoid": "Heavy fatty foods, processed sugars"
        },
        "ovulation": {
            "focus": "Anti-inflammatory & estrogen support",
            "foods": "Flaxseeds, berries, leafy greens, quinoa, almonds",
            "avoid": "High glycemic index foods, deep-fried dishes"
        },
        "luteal": {
            "focus": "Magnesium & complex carbs",
            "foods": "Sweet potatoes, bananas, oats, walnuts, herbal infusions",
            "avoid": "Refined sugars, carbonated drinks, excess caffeine"
        }
    }
    
    return phase_data.get(phase.lower(), {
        "focus": "Balanced nutrition",
        "foods": "Seasonal fruits, vegetables, whole grains, dairy products",
        "avoid": "Junk foods, processed snacks"
    })
