import os
from dotenv import load_dotenv
import openai
import streamlit as st
from maps_api import get_recommendations_from_google_maps, geocode_location
import pandas as pd

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="MoodGPT: Your Mood-Based Activity Chatbot", page_icon="💬", layout="wide")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are MoodGPT, a friendly and empathetic assistant. Engage in natural conversation, respond kindly to user emotions. "
                "After about 3 user messages, proactively suggest local relaxing spots based on the user's location. "
                "Avoid repetitive apologies. Keep responses warm and helpful."
            )
        },
        {
            "role": "assistant",
            "content": "Hi there! I’m MoodGPT. How are you feeling today?"
        }
    ]
    st.session_state["user_message_count"] = 0
    st.session_state["recommended_places"] = []
    st.session_state["location"] = "New York"  # 用户可修改
    st.session_state["location_coords"] = None  # 保存地理坐标

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

# 自定义CSS，让UI更科技感
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
h1, h2, h3 {
    font-weight: 600;
}
input[type=text] {
    border-radius: 5px;
    border: 1px solid #ccc;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("MoodGPT: Your Mood-Based Activity Chatbot")

# 顶部位置设置
st.write("**Set Your Location** (e.g., 'New York', 'San Francisco', or '40.7128,-74.0060'):")
location_input = st.text_input("Your location:", value=st.session_state["location"])
if location_input.strip() != st.session_state["location"]:
    st.session_state["location"] = location_input.strip()
    st.session_state["recommended_places"] = []  # 位置变了后清空已推荐地点

# 地理编码用户位置
coords = None
if "," in st.session_state["location"]:
    # 认为是 "lat,lng" 格式
    coords = tuple(map(float, st.session_state["location"].split(",")))
else:
    # 认为是地名
    coords = geocode_location(st.session_state["location"])

if coords is None:
    # 地理编码失败或未给出正确坐标，默认纽约
    coords = (40.7128, -74.0060)
st.session_state["location_coords"] = coords

left_col, right_col = st.columns([1,1])

with left_col:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.markdown(
                f"""
                <div class='assistant-msg'>
                    <img src='https://raw.githubusercontent.com/hpdts/lambda-assets/master/bot_icon.png' class='assistant-avatar'>
                    <div class='assistant-bubble'><strong>MoodGPT:</strong><br>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
        elif msg["role"] == "user":
            st.markdown(
                f"""
                <div class='user-msg'>
                    <img src='https://raw.githubusercontent.com/hpdts/lambda-assets/master/user_icon.png' class='user-avatar'>
                    <div class='user-bubble'><strong>You:</strong><br>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.text_input("Type your message here...")

    col_buttons = st.columns([1,1])
    with col_buttons[0]:
        send_button = st.button("Send")
    with col_buttons[1]:
        clear_button = st.button("Clear Chat")

    if send_button:
        user_msg = user_input.strip()
        if user_msg:
            # 加入用户消息
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            st.session_state["user_message_count"] += 1
            # 生成AI回复
            response = generate_response(st.session_state["messages"])
            st.session_state["messages"].append({"role": "assistant", "content": response})

            # 自动推荐逻辑
            if st.session_state["user_message_count"] >= 3 and not st.session_state["recommended_places"]:
                # 假定关键字yoga，可根据需求改为根据用户对话内容选择关键字
                keyword = "yoga"
                lat, lng = st.session_state["location_coords"]
                location_str = f"{lat},{lng}"
                places = get_recommendations_from_google_maps(keyword=keyword, location=location_str, radius=2000)
                if places:
                    rec_text = "It seems you might enjoy some relaxing spots around your location:\n\n"
                    for p in places:
                        google_map_link = f"https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lng']}"
                        rec_text += f"- [{p['name']}]({google_map_link}) - {p['address']}\n"
                    st.session_state["messages"].append({"role": "assistant", "content": rec_text})
                    st.session_state["recommended_places"] = places

    if clear_button:
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
    # 构建地图数据
    map_data = {
        "lat": [],
        "lon": []
    }

    # 如果有推荐地点，加入到地图数据中
    if st.session_state["recommended_places"]:
        for place in st.session_state["recommended_places"]:
            if place["lat"] and place["lng"]:
                map_data["lat"].append(place["lat"])
                map_data["lon"].append(place["lng"])
        # 显示推荐列表
        for p in st.session_state["recommended_places"]:
            google_map_link = f"https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lng']}"
            st.markdown(f"- **[{p['name']}]({google_map_link})**: {p['address']}")
    else:
        # 没有推荐就只显示用户位置
        lat, lng = st.session_state["location_coords"]
        map_data["lat"].append(lat)
        map_data["lon"].append(lng)
        st.write("No recommendations yet. After a few messages, suggestions will appear here.")

    # 显示地图
    if map_data["lat"] and map_data["lon"]:
        df = pd.DataFrame(map_data)
        st.map(df, zoom=13)
