import os
from dotenv import load_dotenv
import openai
import streamlit as st
from maps_api import get_recommendations_from_google_maps, geocode_location
from feedback import RecommendationRLModel  # Import the Q-table model
from utils import classify_emotion, get_activity_keyword, refine_recommendations
import pandas as pd
import base64

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure Streamlit page
st.set_page_config(
    page_title="MoodGPT: Your Mood-Based Activity Chatbot",
    page_icon="💬💢",
    layout="wide"
)

# Initialize session state for Q-table model and other variables
if "rl_model" not in st.session_state:
    st.session_state["rl_model"] = RecommendationRLModel()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are MoodGPT, a friendly assistant that recommends relaxing activities."},
        {"role": "assistant", "content": "Hi there! I’m MoodGPT. How are you feeling today?"}
    ]
    st.session_state["user_message_count"] = 0
    st.session_state["recommended_places"] = []
    st.session_state["location"] = "New York"
    st.session_state["location_coords"] = None
    st.session_state["feedback"] = []

# Function to generate responses from OpenAI
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

# Custom CSS for avatars and layout
st.markdown("""
<style>
.avatar-img {
    width: 40px;
    height: 40px;
    border-radius: 20px;
    margin-right: 10px;
}
.chat-msg {
    display: flex;
    align-items: flex-start;
    margin: 10px 0;
}
.user-bubble, .assistant-bubble {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 10px;
    font-size: 15px;
}
.user-bubble {
    background-color: #dcf8c6;
    margin-left: auto;
}
.assistant-bubble {
    background-color: #f0f2f6;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# Main app logic
st.title("MoodGPT: Your Mood-Based Activity Chatbot")

# User location input
location_input = st.text_input("Enter your location:", value=st.session_state["location"])
if location_input.strip() != st.session_state["location"]:
    st.session_state["location"] = location_input.strip()
    st.session_state["recommended_places"] = []
    st.session_state["recommended_places"] = []

coords = None
if "," in st.session_state["location"]:
    coords = tuple(map(float, st.session_state["location"].split(",")))
else:
    coords = geocode_location(st.session_state["location"])

if coords:
    st.session_state["location_coords"] = coords
else:
    st.session_state["location_coords"] = (40.7128, -74.0060)  # Default to New York

# Left column: Chat interface
left_col, right_col = st.columns([2, 1])
with left_col:
    # Display chat history
    for idx, msg in enumerate(st.session_state["messages"]):
        if msg["role"] == "assistant":
            st.markdown(
                f"""
                <div class="chat-msg">
                    <img src="https://i.pinimg.com/originals/0b/40/63/0b40633c3c0b2b245a6ba8b30baf7706.png" class="avatar-img">
                    <div class="assistant-bubble">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )
            # Feedback buttons
            col_feedback = st.columns([1, 1])
            with col_feedback[0]:
                if st.button("👍", key=f"thumbs_up_{idx}"):
                    st.session_state["feedback"].append({"message_idx": idx, "feedback": 1})
            with col_feedback[1]:
                if st.button("👎", key=f"thumbs_down_{idx}"):
                    st.session_state["feedback"].append({"message_idx": idx, "feedback": -1})
        elif msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-msg" style="justify-content: flex-end;">
                    <div class="user-bubble">{msg['content']}</div>
                    <img src="https://i.pinimg.com/originals/15/ad/b3/15adb3f1eb3a24e692da5b56108edf5d.jpg" class="avatar-img">
                </div>
                """, unsafe_allow_html=True
            )

    # Chat input field with clearing logic
    user_input_key = f"chat_input_{st.session_state['user_message_count']}"
    user_input = st.text_input("Type your message here:", key=user_input_key)
    send_button = st.button("Send")

    if (send_button or user_input) and user_input.strip():
        user_msg = user_input.strip()
        st.session_state["messages"].append({"role": "user", "content": user_msg})
        st.session_state["user_message_count"] += 1

        # Generate and add chatbot response
        response = generate_response(st.session_state["messages"])
        st.session_state["messages"].append({"role": "assistant", "content": response})

        # Add recommendations if needed
        if st.session_state["user_message_count"] >= 3 and not st.session_state["recommended_places"]:
            places = get_recommendations_from_google_maps("relaxing activities", f"{coords[0]},{coords[1]}", 2000)
            if places:
                rec_msg = "Here are some relaxing spots nearby:\n"
                for place in places:
                    link = f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lng']}"
                    rec_msg += f"- [{place['name']}]({link}) - {place['address']}\n"
                st.session_state["messages"].append({"role": "assistant", "content": rec_msg})
                st.session_state["recommended_places"] = places

        st.rerun()

# Right column: Display recommendations and map
with right_col:
    st.write("### Nearby Recommendations")
    map_data = {"lat": [], "lon": []}
    for place in st.session_state["recommended_places"]:
        link = f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lng']}"
        st.markdown(f"- **[{place['name']}]({link})**: {place['address']}")
        map_data["lat"].append(place["lat"])
        map_data["lon"].append(place["lng"])

    if map_data["lat"] and map_data["lon"]:
        df = pd.DataFrame(map_data)
        st.map(df, zoom=13)

# Save Q-table button
if st.button("Save Q-Table"):
    st.session_state["rl_model"].save_model("q_table.npy")
