from fastapi import FastAPI
import requests
from datetime import datetime, timedelta

app = FastAPI()

# API Endpoint for ECMWF-based irradiance data (Open-Meteo API as example)
BASE_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_irradiance(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "shortwave_radiation",
        "timezone": "auto"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data.get("hourly", {}).get("shortwave_radiation", [])

@app.get("/forecast")
def get_irradiance(city: str, lat: float, lon: float):
    irradiance_data = fetch_irradiance(lat, lon)
    hourly_forecast = []
    
    now = datetime.utcnow()
    for i, value in enumerate(irradiance_data):
        timestamp = now + timedelta(hours=i)
        hourly_forecast.append({
            "time": timestamp.strftime("%Y-%m-%d %H:%M"),
            "irradiance_wm2": value
        })
    
    return {"city": city, "forecast": hourly_forecast}
