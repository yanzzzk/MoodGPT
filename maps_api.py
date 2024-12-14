import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_recommendations_from_google_maps(keyword="yoga", location="40.7128,-74.0060", radius=1500):
    """
    使用Google Places API根据关键词和位置获得附近的放松场所推荐。
    参数说明：
    keyword: 搜索关键字，比如 'yoga', 'spa', 'restaurant', 'cinema'
    location: 纬度经度字符串 "lat,lng" 格式
    radius: 搜索半径（米）

    返回：
    包含地点信息的列表，每个元素是字典：
    {
      "name": "Place Name",
      "address": "Address",
      "lat": float,
      "lng": float
    }
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
        for place in data["results"][:5]:  # 只取前5个结果
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "No address found")
            geometry = place.get("geometry", {})
            location = geometry.get("location", {})
            lat = location.get("lat")
            lng = location.get("lng")
            recommendations.append({
                "name": name,
                "address": address,
                "lat": lat,
                "lng": lng
            })
    return recommendations
