from dotenv import load_dotenv
import openai
import streamlit as st
from maps_api import get_recommendations_from_google_maps

# 加载 .env 文件
load_dotenv()

# 从环境变量中读取 API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 初始化聊天历史
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

# Streamlit 页面标题
st.title("Mood-based Chatbot")
st.subheader("Chat with me, and I'll recommend a relaxing activity!")

# 显示聊天历史
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Chatbot:** {message['content']}")

# 用户输入
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip():
        # 保存用户输入到聊天历史
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        try:
            # 调用 OpenAI API 获取回复
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 或 "gpt-4"
                messages=st.session_state.messages
            )

            # 保存 ChatGPT 的回复到聊天历史
            chatbot_reply = response.choices[0].message["content"]
            st.session_state.messages.append({"role": "assistant", "content": chatbot_reply})

        except Exception as e:
            st.error(f"Error: {str(e)}")

        # 清空输入框
        st.experimental_rerun()

# 添加推荐按钮
if st.button("Recommend an Activity"):
    try:
        # 根据聊天上下文生成推荐
        recommendation_prompt = st.session_state.messages + [
            {"role": "user", "content": "Based on our conversation, recommend a relaxing activity, such as a restaurant, movie theater, or other entertainment options."}
        ]
        recommendation_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或 "gpt-4"
            messages=recommendation_prompt
        )
        recommendation = recommendation_response.choices[0].message["content"]
        st.write(f"**Chatbot Recommendation:** {recommendation}")

    except Exception as e:
        st.error(f"Error: {str(e)}")
