# from dotenv import load_dotenv
# import os
# import openai
# import streamlit as st

# # 加载 .env 文件
# load_dotenv()

# # 从环境变量中读取 API Key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # 初始化聊天历史
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "system", "content": "You are a helpful chatbot that engages in conversations and eventually recommends a relaxing activity, such as a restaurant, movie theater, or other entertainment options."},
#         {"role": "assistant", "content": "Hello! How can I assist you today?"}
#     ]

# # Streamlit 页面标题
# st.title("Mood-based Chatbot")
# st.subheader("Chat with me, and I'll recommend a relaxing activity!")

# # 显示聊天历史
# for message in st.session_state.messages:
#     if message["role"] == "user":
#         st.markdown(f"**You:** {message['content']}")
#     elif message["role"] == "assistant":
#         st.markdown(f"**Chatbot:** {message['content']}")

# # 用户输入
# user_input = st.text_input("Your message:")

# if st.button("Send"):
#     if user_input.strip():
#         # 保存用户输入到聊天历史
#         st.session_state.messages.append({"role": "user", "content": user_input.strip()})

#         try:
#             # 调用 OpenAI API 获取回复
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",  # 或 "gpt-4"
#                 messages=st.session_state.messages
#             )

#             # 保存 ChatGPT 的回复到聊天历史
#             chatbot_reply = response.choices[0].message["content"]
#             st.session_state.messages.append({"role": "assistant", "content": chatbot_reply})

#         except Exception as e:
#             st.error(f"Error: {str(e)}")

#         # 清空输入框
#         st.experimental_rerun()

# # 添加推荐按钮
# if st.button("Recommend an Activity"):
#     try:
#         # 根据聊天上下文生成推荐
#         recommendation_prompt = st.session_state.messages + [
#             {"role": "user", "content": "Based on our conversation, recommend a relaxing activity, such as a restaurant, movie theater, or other entertainment options."}
#         ]
#         recommendation_response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # 或 "gpt-4"
#             messages=recommendation_prompt
#         )
#         recommendation = recommendation_response.choices[0].message["content"]
#         st.write(f"**Chatbot Recommendation:** {recommendation}")

#     except Exception as e:
#         st.error(f"Error: {str(e)}")






from dotenv import load_dotenv
import os
import openai
import streamlit as st

# Load .env file
load_dotenv()

# Read the API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful chatbot that engages in conversations and eventually recommends a relaxing activity, such as a restaurant, movie theater, or other entertainment options."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Streamlit page title
st.title("Mood-based Chatbot")
st.subheader("Chat with me, and I'll recommend a relaxing activity!")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Chatbot:** {message['content']}")

# User input
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input.strip():
        # Save user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        try:
            # Call OpenAI API to get the chatbot's reply
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or "gpt-4"
                messages=st.session_state.messages
            )

            # Save ChatGPT's reply to chat history
            chatbot_reply = response.choices[0].message["content"]
            st.session_state.messages.append({"role": "assistant", "content": chatbot_reply})

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Add a button for activity recommendation
if st.button("Recommend an Activity"):
    try:
        # Generate recommendation based on chat context
        recommendation_prompt = st.session_state.messages + [
            {"role": "user", "content": "Based on our conversation, recommend a relaxing activity, such as a restaurant, movie theater, or other entertainment options."}
        ]
        recommendation_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4"
            messages=recommendation_prompt
        )
        recommendation = recommendation_response.choices[0].message["content"]
        st.write(f"**Chatbot Recommendation:** {recommendation}")

    except Exception as e:
        st.error(f"Error: {str(e)}")

