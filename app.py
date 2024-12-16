import os
from dotenv import load_dotenv
import openai
import streamlit as st
from maps_api import get_recommendations_from_google_maps, geocode_location
from utils import classify_emotion, get_activity_keyword, refine_recommendations
import pandas as pd
import base64

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="MoodGPT: Your Mood-Based Activity Chatbot",
    page_icon="🪷",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are MoodGPT, a friendly and empathetic assistant. Engage in natural conversation, "
                "respond kindly to user emotions. After about 3 user messages, proactively suggest local "
                "relaxing spots or entertainment (anime, theme parks, cafes, etc.) based on the user's location. "
                "Use knowledge from ML: K-NN, PCA, Decision Trees and possibly embeddings to refine recommendations. "
                "Avoid repetitive apologies. Keep responses warm and helpful."
            )
        },
        {
            "role": "assistant",
            "content": "Hi there! I’m MoodGPT AI assistant Yuki Asuna. How are you feeling today?"
        }
    ]
    st.session_state["user_message_count"] = 0
    st.session_state["recommended_places"] = []
    st.session_state["location"] = "New York"
    st.session_state["location_coords"] = None

def generate_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# CSS
st.markdown("""
<style>
body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    background: #f0f2f6;
}
.chat-container {
    padding: 20px;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.user-msg, .assistant-msg {
    display: flex;
    align-items: flex-start;
    margin: 15px 0;
}
.user-avatar, .assistant-avatar {
    width: 40px;
    height: 40px;
    border-radius: 20px;
    margin: 0 10px;
}
.user-avatar {
    order: 2;
}
.user-bubble, .assistant-bubble {
    border-radius: 10px;
    padding: 10px 15px;
    max-width: 80%;
    line-height: 1.5;
    font-size: 15px;
}
.user-bubble {
    background: #DCF8C6;
    margin-left: auto;
}
.assistant-bubble {
    background: #e8ebf0;
    margin-right: auto;
}
.custom-image {
    display: block;
    margin: 0 auto;
    border-radius: 10px;
    max-height: 300px;
    width: 100%;
    object-fit: cover;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
""", unsafe_allow_html=True)

st.title("MoodGPT: Your Mood-Based Activity Chatbot")

# 显示图片
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = "static/star.jpg"
image_base64 = image_to_base64(image_path)
st.markdown(
    f"""
    <div>
        <img src="data:image/jpeg;base64,{image_base64}" alt="Mood-GPT" class="custom-image">
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("**Set Your Location** (e.g., 'New York', 'San Francisco', or '40.7128,-74.0060'):")
location_input = st.text_input("Your location:", value=st.session_state["location"])
if location_input.strip() != st.session_state["location"]:
    st.session_state["location"] = location_input.strip()
    st.session_state["recommended_places"] = []

coords = None
if "," in st.session_state["location"]:
    coords = tuple(map(float, st.session_state["location"].split(",")))
else:
    coords = geocode_location(st.session_state["location"])

if coords is None:
    coords = (40.7128, -74.0060)
st.session_state["location_coords"] = coords

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.markdown(
                f"""
                <div class='assistant-msg'>
                    <img src='https://i.pinimg.com/originals/0b/40/63/0b40633c3c0b2b245a6ba8b30baf7706.png' class='assistant-avatar'>
                    <div class='assistant-bubble'><strong>MoodGPT:</strong><br>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
        elif msg["role"] == "user":
            st.markdown(
                f"""
                <div class='user-msg'>
                    <img src='https://i.pinimg.com/originals/15/ad/b3/15adb3f1eb3a24e692da5b56108edf5d.jpg' class='user-avatar'>
                    <div class='user-bubble'><strong>You:</strong><br>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.text_input("Type your message here...")
    if st.button("Send"):
        user_msg = user_input.strip()
        if user_msg:
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            st.session_state["user_message_count"] += 1

            # 根据用户输入决定活动关键词
            emotion = classify_emotion(user_msg)
            keyword = get_activity_keyword(emotion)

            # 获取推荐
            lat, lng = st.session_state["location_coords"]
            location_str = f"{lat},{lng}"
            places = get_recommendations_from_google_maps(keyword=keyword, location=location_str, radius=2000)
            places = refine_recommendations(places, emotion)

            st.session_state["recommended_places"] = places

            # 生成AI回复
            # 可在此增加深度学习模型的上下文理解增强，在此示例中仍使用OpenAI API
            response = generate_response(st.session_state["messages"])
            st.session_state["messages"].append({"role": "assistant", "content": f"{response}\n\nI've found some {keyword} spots around you! If you're feeling {emotion}, these might be interesting."})

    if st.button("Clear Chat"):
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": "You are MoodGPT..."
            },
            {
                "role": "assistant",
                "content": "Hi there! I’m MoodGPT. How are you feeling today?"
            }
        ]
        st.session_state["user_message_count"] = 0
        st.session_state["recommended_places"] = []

with right_col:
    st.write("**Nearby Recommendations & Map**")
    map_data = {"lat": [], "lon": []}
    if st.session_state["recommended_places"]:
        for place in st.session_state["recommended_places"]:
            map_data["lat"].append(place["lat"])
            map_data["lon"].append(place["lng"])
            st.markdown(f"- **{place['name']}**: {place['address']}")
    else:
        lat, lng = st.session_state["location_coords"]
        map_data["lat"].append(lat)
        map_data["lon"].append(lng)
        st.write("No recommendations yet. After a few messages, suggestions will appear here.")

    if map_data["lat"] and map_data["lon"]:
        df = pd.DataFrame(map_data)
        st.map(df, zoom=13)
