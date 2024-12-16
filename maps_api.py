import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_location(address):
    """
    使用 Google Geocoding API 将地址转换为 (lat, lng) 坐标。
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    if data.get("status") == "OK" and len(data.get("results", [])) > 0:
        location = data["results"][0]["geometry"]["location"]
        return (location["lat"], location["lng"])
    return None

def get_recommendations_from_google_maps(keyword="yoga", location="40.7128,-74.0060", radius=1500):
    """
    使用Google Places API根据关键词和位置获得附近的场所推荐。
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": GOOGLE_MAPS_API_KEY,
        "location": location,
        "radius": radius,
        "keyword": keyword
    }
    response = requests.get(url, params=params)
    data = response.json()
    recommendations = []
    if data.get("results"):
        for place in data["results"][:5]:
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "No address found")
            geometry = place.get("geometry", {})
            loc = geometry.get("location", {})
            lat = loc.get("lat")
            lng = loc.get("lng")
            recommendations.append({
                "name": name,
                "address": address,
                "lat": lat,
                "lng": lng
            })
    return recommendations
