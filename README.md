MoodGPT: Your Personalized Mood-based Chatbot
MoodGPT is an interactive chatbot designed to help users unwind by understanding their mood and recommending activities tailored to their emotions. This application supports multi-turn conversations, saves chat history, and provides real-time recommendations for restaurants, movies, or other leisure activities based on user preferences.

Features
Multi-turn Conversation:

Allows continuous back-and-forth interaction between the user and the chatbot.
Chat history is displayed dynamically, preserving context for intelligent responses.
Real-time Recommendations:

Based on user input, the chatbot suggests:
Restaurants
Movie theaters
Other relaxing activities (e.g., yoga, spa, walks in nature).
Recommendations are presented as a clean, interactive list.
Interactive User Interface:

Designed with Streamlit, offering a sleek and user-friendly experience.
Welcomes users with an introductory message.
Displays conversation history and allows users to restart sessions.
Context-aware AI:

Powered by OpenAI GPT models for intelligent and empathetic responses.
Adapts responses based on the user's mood and conversation flow.
Installation Guide
Prerequisites
Python 3.9 or later (Ensure Python is installed. Recommended: Python 3.10 or 3.12)
Streamlit (For creating the user interface).
OpenAI API Key (Required for chatbot functionality).
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/your-repository/moodgpt.git
cd moodgpt
Step 2: Set Up a Virtual Environment
bash
Copy code
python3 -m venv moodgpt-env
source moodgpt-env/bin/activate  # macOS/Linux
moodgpt-env\Scripts\activate     # Windows
Step 3: Install Dependencies
bash
Copy code
pip install -r requirements.txt
Step 4: Configure the OpenAI API Key
Create a .env file in the project directory.
Add your OpenAI API key in the following format:
env
Copy code
OPENAI_API_KEY=sk-your-openai-api-key
Step 5: Run the Application
bash
Copy code
streamlit run app.py
Usage
Welcome Message:

Upon launching, the chatbot greets the user and asks about their mood.
Start Chatting:

Enter your mood or feelings in the text input field.
Press Send to start the conversation.
Get Personalized Recommendations:

At any time during the conversation, click Get Recommendations to receive suggestions for relaxing activities.
Restart Session:

Use the "Clear Chat" button to reset the conversation and start fresh.
Code Overview
app.py
The main application script responsible for:

Setting up the Streamlit interface.
Handling multi-turn conversations.
Fetching responses from OpenAI GPT models.
Displaying recommendations.
Key Components:
Session State Management:
Stores user inputs and chatbot responses persistently during the session.
Chat History:
Displays all prior messages for context-aware interactions.
Recommendation Engine:
Provides a list of activities tailored to the user's mood.
Technical Details
OpenAI Model Configuration
Uses the GPT-4 API (can be switched to GPT-3.5 for cost-saving).
Implements System Prompts for defining chatbot behavior.
Maintains context for dynamic and intelligent conversations.
Streamlit Features
Dynamic UI:
Displays chat history and input field simultaneously.
Responsive Buttons:
Send, Get Recommendations, and Clear Chat buttons for user interactions.
Advanced Features
Conversation Context
The chatbot uses the conversation history to provide:

Personalized responses.
Follow-up questions like:
“Do you feel stressed?”
“Would you like a distraction or some advice?”
Recommendation Logic
Leverages a predefined list of relaxing activities.
Randomized to keep suggestions fresh.
File Structure
bash
Copy code
moodgpt/
│
├── app.py                     # Main application file
├── requirements.txt           # Required Python dependencies
├── .env                       # API Key (user-created)
├── README.md                  # Project documentation
├── moodgpt-env/               # Virtual environment (user-created)
└── __pycache__/               # Cached Python files (auto-generated)
Sample Output
Welcome Message:

Hi there! I’m MoodGPT, your mood-based assistant. How are you feeling today?

User Input:

I feel a bit stressed after work.

Chatbot Reply:

I’m sorry to hear that. Would you like to talk about it or get some recommendations to unwind?

Recommendations:

Nearby yoga classes
Walks in nature
Top-rated restaurants
Current movie screenings
Contributing
Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
Author: Yan Li
Email: yan61@illinois.edu
GitHub: yanzzzk
Feel free to raise issues or contribute to the project! 🎉