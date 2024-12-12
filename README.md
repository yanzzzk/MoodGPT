# MoodGPT: Your Personalized Mood-based Chatbot

MoodGPT is an interactive chatbot designed to help users unwind by understanding their mood and recommending tailored activities. The application supports multi-turn conversations, saves chat history, and provides real-time suggestions for restaurants, movies, or other leisure activities based on user input.

---

## Features

### Multi-turn Conversation
- Continuous back-and-forth interaction between the user and the chatbot.
- Chat history is displayed dynamically, preserving context for intelligent responses.

### Real-time Recommendations
- Based on user input, the chatbot suggests:
  - Restaurants
  - Movie theaters
  - Other relaxing activities (e.g., yoga, spa, nature walks).
- Recommendations are presented in a clean, interactive list.

### Interactive User Interface
- Designed with **Streamlit** for a sleek and user-friendly experience.
- Welcomes users with an introductory message.
- Displays conversation history and allows users to restart sessions.

### Context-aware AI
- Powered by **OpenAI GPT models** for empathetic and intelligent responses.
- Adapts dynamically to the user’s mood and conversation flow.

---

## Installation Guide

### Prerequisites
1. **Python 3.9 or later** (Recommended: Python 3.10 or 3.12).
2. **Streamlit** (For creating the user interface).
3. **OpenAI API Key** (Required for chatbot functionality).

### Step-by-step Setup

#### Step 1: Clone the Repository
```bash
git clone https://github.com/your-repository/moodgpt.git
cd moodgpt
```

#### Step 2: Set Up a Virtual Environment
```bash
python3 -m venv moodgpt-env
source moodgpt-env/bin/activate  # macOS/Linux
moodgpt-env\Scripts\activate   # Windows
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure the OpenAI API Key
1. Create a `.env` file in the project directory.
2. Add your OpenAI API key in the following format:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

#### Step 5: Run the Application
```bash
streamlit run app.py
```

---

## Usage

### Welcome Message
Upon launching, the chatbot greets the user and asks about their mood.

### Start Chatting
- Enter your mood or feelings in the text input field.
- Press **Send** to start the conversation.

### Get Personalized Recommendations
- During the conversation, click **Get Recommendations** to receive suggestions for relaxing activities.

### Restart Session
- Use the **Clear Chat** button to reset the conversation and start fresh.

---

## Code Overview

### `app.py`
- The main application script responsible for:
  - Setting up the **Streamlit** interface.
  - Managing multi-turn conversations.
  - Fetching responses from OpenAI GPT models.
  - Displaying recommendations.

#### Key Components:
1. **Session State Management**:
   - Stores user inputs and chatbot responses persistently during the session.
2. **Chat History**:
   - Displays all prior messages for context-aware interactions.
3. **Recommendation Engine**:
   - Provides a list of activities tailored to the user’s mood.

### `test.py`
- A test script to validate the API integration and basic functionality of the chatbot.

### `requirements.txt`
- Lists all the dependencies required to run the project, including:
  - `openai`
  - `streamlit`
  - `python-dotenv`

---

## Advanced Features

### Conversation Context
The chatbot uses conversation history to provide:
- Personalized responses.
- Follow-up questions such as:
  - “Do you feel stressed?”
  - “Would you like a distraction or some advice?”

### Recommendation Logic
- Leverages a predefined list of relaxing activities.
- Randomized to ensure fresh suggestions.

---

## File Structure
```
moodgpt/
├── app.py               # Main application file
├── requirements.txt     # Required Python dependencies
├── .env                 # API Key (user-created)
├── README.md            # Project documentation
├── moodgpt-env/         # Virtual environment (user-created)
└── __pycache__/         # Cached Python files (auto-generated)
```

---

## Sample Output

### Welcome Message:
```
Hi there! I’m MoodGPT, your mood-based assistant. How are you feeling today?
```

### User Input:
```
I feel a bit stressed after work.
```

### Chatbot Reply:
```
I’m sorry to hear that. Would you like to talk about it or get some recommendations to unwind?
```

### Recommendations:
1. Nearby yoga classes
2. Walks in nature
3. Top-rated restaurants
4. Current movie screenings

---

## Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
**Author**: Yan Li  
**Email**: yan61@illinois.edu  
**GitHub**: [yanzzzk](https://github.com/yanzzzk)

Feel free to raise issues or contribute to the project! 🎉

