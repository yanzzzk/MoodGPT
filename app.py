import os
from dotenv import load_dotenv
import openai
import streamlit as st
from maps_api import get_recommendations_from_google_maps

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 初始化对话历史和状态
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are MoodGPT, a friendly and empathetic assistant. You should engage in natural, human-like conversation. "
                "Acknowledge the user's emotions, but do not repeat the exact same sentence or apology too many times. Vary your responses. "
                "If the user is sad, provide gentle encouragement and suggest simple self-care or relaxing activities. "
                "If the user is happy, celebrate their happiness and explore their interests. "
                "After the user has sent about 3 messages, proactively suggest some local relaxing places. "
                "Do not be overly repetitive. Keep responses concise and friendly."
            )
        },
        {
            "role": "assistant",
            "content": "Hi there! I’m MoodGPT. How are you feeling today?"
        }
    ]
    st.session_state["user_message_count"] = 0
    st.session_state["recommended_places"] = []  # 用于存储推荐地点

st.set_page_config(page_title="MoodGPT: Your Mood-Based Activity Chatbot", page_icon="💬")

# CSS样式（更圆润，更清晰的UI）
st.markdown("""
<style>
body {
    font-family: "Helvetica", sans-serif;
}
.chat-container {
    padding: 10px;
}
.user-msg, .assistant-msg {
    display: flex;
    align-items: flex-start;
    margin: 10px 0;
}
.user-avatar, .assistant-avatar {
    width: 40px;
    height: 40px;
    border-radius: 20px;
    margin: 0 10px;
}
.user-avatar {
    order: 2; /* 用户头像在右侧 */
}
.user-bubble {
    background: #DCF8C6;
    border-radius: 15px;
    padding: 10px 15px;
    margin-left: auto;
    max-width: 70%;
}
.assistant-bubble {
    background: #F1F0F0;
    border-radius: 15px;
    padding: 10px 15px;
    margin-right: auto;
    max-width: 70%;
}
.input-container {
    display: flex;
    align-items: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("MoodGPT: Your Mood-Based Activity Chatbot")

left_col, right_col = st.columns([2,1])  # 左边对话，右边地图

with left_col:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    # 显示对话
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.markdown(
                f"""
                <div class='assistant-msg'>
                    <img src='https://raw.githubusercontent.com/microsoft/ ConversationalAgent/main/docs/images/bot_icon.png' class='assistant-avatar'>
                    <div class='assistant-bubble'>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
        elif msg["role"] == "user":
            st.markdown(
                f"""
                <div class='user-msg'>
                    <img src='https://raw.githubusercontent.com/microsoft/ ConversationalAgent/main/docs/images/user_icon.png' class='user-avatar'>
                    <div class='user-bubble'>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # 输入框和发送按钮
    user_input = st.text_input("Type your message here...", "")
    send_clicked = st.button("Send")
    clear_clicked = st.button("Clear Chat")

# 在右侧显示地图和推荐地点（如果有）
with right_col:
    st.write("**Suggested Places**")
    if st.session_state["recommended_places"]:
        # 显示地点列表
        for place in st.session_state["recommended_places"]:
            st.write(f"- **{place['name']}**: {place['address']}")

        # 显示地图
        # 从recommended_places中提取lat,lng
        map_data = {
            "lat": [p["lat"] for p in st.session_state["recommended_places"] if p["lat"] and p["lng"]],
            "lon": [p["lng"] for p in st.session_state["recommended_places"] if p["lat"] and p["lng"]]
        }
        if map_data["lat"] and map_data["lon"]:
            import pandas as pd
            df = pd.DataFrame(map_data)
            st.map(df)
    else:
        st.write("No recommendations yet.")

# 处理用户发送逻辑
if send_clicked and user_input.strip():
    st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
    st.session_state["user_message_count"] += 1

    # 自动回复生成函数
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

    # 生成AI回复
    response = generate_response(st.session_state["messages"])
    st.session_state["messages"].append({"role": "assistant", "content": response})

    # 当用户消息数>=3时尝试自动推荐
    if st.session_state["user_message_count"] >= 3 and not st.session_state["recommended_places"]:
        # 示例：固定查询yoga场所
        # 你可以根据用户对话内容动态决定keyword和location
        places = get_recommendations_from_google_maps(keyword="yoga", location="40.7128,-74.0060", radius=2000)
        if places:
            rec_text = "It sounds like you might enjoy some relaxing activities. Here are a few places you could check out nearby:\n"
            for p in places:
                rec_text += f"{p['name']} - {p['address']}\n"
            st.session_state["messages"].append({"role": "assistant", "content": rec_text})
            st.session_state["recommended_places"] = places

    # 用户交互结束后页面自动重绘，无需 experimental_rerun()

# 处理清空对话逻辑
if clear_clicked:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are MoodGPT, a friendly and empathetic assistant..."
            )
        },
        {
            "role": "assistant",
            "content": "Hi there! I’m MoodGPT. How are you feeling today?"
        }
    ]
    st.session_state["user_message_count"] = 0
    st.session_state["recommended_places"] = []
    # 同样无需 experimental_rerun()，按钮点击后脚本自动重跑。
