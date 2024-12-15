import os
from dotenv import load_dotenv
import openai
import streamlit as st
from maps_api import get_recommendations_from_google_maps, geocode_location
import pandas as pd
import base64

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 设置页面配置
st.set_page_config(
    page_title="MoodGPT: Your Mood-Based Activity Chatbot",
    page_icon="💬",
    layout="wide"
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are MoodGPT, a friendly and empathetic assistant. Engage in natural conversation, "
                "respond kindly to user emotions. After about 3 user messages, proactively suggest local "
                "relaxing spots based on the user's location. Avoid repetitive apologies. Keep responses warm and helpful."
            )
        },
        {
            "role": "assistant",
            "content": "Hi there! I’m MoodGPT AI assistant, my name is Yuki Asuna. How are you feeling today?"
        }
    ]
    st.session_state["user_message_count"] = 0
    st.session_state["recommended_places"] = []
    st.session_state["location"] = "New York"
    st.session_state["location_coords"] = None

# 生成 OpenAI 响应
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

# 自定义 CSS
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

# 页面标题
st.title("MoodGPT: Your Mood-Based Activity Chatbot")

# 显示图片（通过 Base64 编码方式嵌入图片）
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = "static/star.jpg"  # 图片路径
image_base64 = image_to_base64(image_path)

# 使用 Base64 编码的图片
st.markdown(
    f"""
    <div>
        <img src="data:image/jpeg;base64,{image_base64}" alt="Mood-GPT" class="custom-image">
    </div>
    """,
    unsafe_allow_html=True,
)

# 设置用户位置
st.write("**Set Your Location** (e.g., 'New York', 'San Francisco', or '40.7128,-74.0060'):")
location_input = st.text_input("Your location:", value=st.session_state["location"])
if location_input.strip() != st.session_state["location"]:
    st.session_state["location"] = location_input.strip()
    st.session_state["recommended_places"] = []

# 地理编码用户位置
coords = None
if "," in st.session_state["location"]:
    coords = tuple(map(float, st.session_state["location"].split(",")))
else:
    coords = geocode_location(st.session_state["location"])

if coords is None:
    coords = (40.7128, -74.0060)  # 默认值
st.session_state["location_coords"] = coords

# 页面布局
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

    # 聊天输入框
    user_input = st.text_input("Type your message here...")
    if st.button("Send"):
        user_msg = user_input.strip()
        if user_msg:
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            st.session_state["user_message_count"] += 1
            response = generate_response(st.session_state["messages"])
            st.session_state["messages"].append({"role": "assistant", "content": response})

            # 自动推荐
            if st.session_state["user_message_count"] >= 3 and not st.session_state["recommended_places"]:
                keyword = "yoga"
                lat, lng = st.session_state["location_coords"]
                location_str = f"{lat},{lng}"
                places = get_recommendations_from_google_maps(keyword=keyword, location=location_str, radius=2000)
                if places:
                    rec_text = "Here are some relaxing spots around your location:\n\n"
                    for p in places:
                        google_map_link = f"https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lng']}"
                        rec_text += f"- [{p['name']}]({google_map_link}) - {p['address']}\n"
                    st.session_state["messages"].append({"role": "assistant", "content": rec_text})
                    st.session_state["recommended_places"] = places

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
            google_map_link = f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lng']}"
            st.markdown(f"- **[{place['name']}]({google_map_link})**: {place['address']}")
    else:
        lat, lng = st.session_state["location_coords"]
        map_data["lat"].append(lat)
        map_data["lon"].append(lng)
        st.write("No recommendations yet. After a few messages, suggestions will appear here.")

    if map_data["lat"] and map_data["lon"]:
        df = pd.DataFrame(map_data)
        st.map(df, zoom=13)
