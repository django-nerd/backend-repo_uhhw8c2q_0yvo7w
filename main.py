import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

app = FastAPI(title="Russo-Ukrainian War Info API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Russo-Ukrainian War Info API"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# --------------------
# Content Endpoints
# --------------------

@app.get("/api/overview")
def get_overview() -> Dict[str, Any]:
    return {
        "title": "Overview",
        "intro": (
            "The Russo-Ukrainian war is an ongoing, large-scale conflict primarily fought on "
            "Ukrainian territory. It began in 2014 following Russia’s annexation of Crimea and "
            "escalated dramatically with the full-scale invasion of Ukraine launched by Russia on "
            "February 24, 2022. The war has resulted in significant military and civilian casualties, "
            "mass displacement, widespread infrastructure damage, and major geopolitical and economic impacts."
        ),
        "key_points": [
            "Origins trace back to 2014 with the annexation of Crimea and fighting in Donbas.",
            "A full-scale invasion began on February 24, 2022, expanding the conflict countrywide.",
            "The war involves conventional warfare, missile strikes, drone usage, and cyber operations.",
            "International responses include sanctions, military aid to Ukraine, and humanitarian assistance.",
            "Negotiations have occurred intermittently but a comprehensive settlement remains unresolved."
        ],
        "disclaimer": (
            "This page provides a concise, neutral overview for general information only. "
            "For up-to-date details, consult multiple credible sources."
        )
    }

@app.get("/api/timeline")
def get_timeline() -> Dict[str, List[Dict[str, str]]]:
    events: List[Dict[str, str]] = [
        {"date": "2014-02", "event": "Russia annexes Crimea following contested referendum."},
        {"date": "2014-04", "event": "Armed conflict begins in Eastern Ukraine (Donbas)."},
        {"date": "2015-02", "event": "Minsk II agreement seeks to reduce fighting; violations continue."},
        {"date": "2021-2022", "event": "Russian troop buildup near Ukraine’s borders raises alarm."},
        {"date": "2022-02-24", "event": "Russia launches full-scale invasion of Ukraine."},
        {"date": "2022-03–04", "event": "Heavy fighting across multiple fronts; large-scale displacement."},
        {"date": "2022-09", "event": "Ukrainian counteroffensives retake significant territory in Kharkiv region."},
        {"date": "2022-11", "event": "Russian forces withdraw from the city of Kherson."},
        {"date": "2023", "event": "Continued fighting; drone and missile strikes; evolving front lines."},
        {"date": "2024", "event": "Ongoing hostilities with periodic escalations and international responses."}
    ]
    return {"events": events}

@app.get("/api/key-facts")
def get_key_facts() -> Dict[str, Any]:
    return {
        "facts": [
            {"label": "Start of Full-Scale Invasion", "value": "Feb 24, 2022"},
            {"label": "Primary Theaters", "value": "Eastern and Southern Ukraine, with strikes nationwide"},
            {"label": "Displacement", "value": "Millions internally displaced and refugees (varies over time)"},
            {"label": "International Response", "value": "Sanctions on Russia; military and humanitarian aid to Ukraine"},
            {"label": "Cyber and Information", "value": "Significant cyber operations and information warfare"}
        ],
        "note": "Data points are high-level and not exhaustive; consult live sources for updates."
    }

@app.get("/api/resources")
def get_resources() -> Dict[str, List[Dict[str, str]]]:
    return {
        "resources": [
            {"name": "United Nations – Situation Reports", "url": "https://www.un.org/en"},
            {"name": "ICRC – Humanitarian Updates", "url": "https://www.icrc.org"},
            {"name": "NATO – Official Statements", "url": "https://www.nato.int"},
            {"name": "EU – Official Statements", "url": "https://europa.eu"},
            {"name": "Ukrainian Government", "url": "https://www.kmu.gov.ua/en"},
            {"name": "Russian Government", "url": "http://government.ru/en/"},
            {"name": "BBC – Explainers and Coverage", "url": "https://www.bbc.com/news"},
            {"name": "Reuters – Live Updates", "url": "https://www.reuters.com/world/europe/"}
        ],
        "disclaimer": "Links are provided for reference. Exercise critical thinking and verify with multiple credible sources."
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
