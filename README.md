# **MoodGPT: Your Personalized Mood-Based Chatbot**

MoodGPT is an AI-powered chatbot designed to understand user emotions and recommend tailored activities. Built with **machine learning**, **reinforcement learning**, and real-time geolocation capabilities, the application helps users unwind by suggesting nearby activities such as cafes, spas, amusement parks, movie theaters, and more.

🚀 **Live Demo**: [MoodGPT - Your Mood AI Assistant](https://moodaiasuna.streamlit.app/)

---

## Demo Video

[Click here to watch the demo video] https://www.youtube.com/watch?v=aoYiTeh3UXA


## **Features**

### **1. Multi-Turn Conversation**
- Continuous and natural back-and-forth interaction with the chatbot.  
- Chat history dynamically displays to preserve context for **intelligent, empathetic responses**.

### **2. Real-Time Personalized Recommendations**
- Based on the user's mood and location, the chatbot suggests:
  - Restaurants and cafes  
  - Movie theaters  
  - Relaxing activities (e.g., yoga studios, spas, nature walks)  
  - Entertainment venues (e.g., amusement parks, anime expos, bars)  
- Recommendations are fetched dynamically via the **Google Places API** and displayed interactively.

### **3. Context-Aware AI with Reinforcement Learning**
- Built using **OpenAI GPT-4** for natural language understanding and mood detection.  
- **Reinforcement Learning (Q-Learning)** improves recommendation accuracy over time based on user feedback.

### **4. Interactive, User-Friendly Interface**
- Built with **Streamlit** for a sleek, intuitive experience.  
- Features include:
  - Live conversation and chat history  
  - A dynamic geolocation-based map showing nearby recommendations  
  - Clear, well-organized interface for seamless navigation  

---

## **Installation Guide**

### **Prerequisites**
1. **Python 3.9 or later** (Recommended: Python 3.10 or 3.12)  
2. **Streamlit** (Web framework)  
3. **OpenAI API Key** (For GPT-powered responses)  
4. **Google Maps API Key** (For real-time geolocation recommendations)  

---

### **Step-by-Step Setup**

#### **1. Clone the Repository**
```bash
git clone https://github.com/your-repository/moodgpt.git
cd moodgpt

2. Set Up a Virtual Environment
bash
Copy code
python3 -m venv moodgpt-env
source moodgpt-env/bin/activate  # macOS/Linux
moodgpt-env\Scripts\activate    # Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure API Keys
Create a .env file in the project root directory.
Add your API keys in the following format:
env
Copy code
OPENAI_API_KEY=sk-your-openai-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
5. Run the Application
bash
Copy code
streamlit run app.py
Usage
Welcome Message
Upon launching, the chatbot greets the user with:
“Hi there! I’m MoodGPT AI assistant, my name is Yuki Asuna. How are you feeling today?”

Start a Conversation
Type your mood or feelings into the text input box (e.g., “I’m feeling tired”).
Press Send to interact with the chatbot.
Receive Personalized Recommendations
After 3-4 interactions, the chatbot proactively recommends activities based on your emotions and location.
A list of suggestions is displayed, and locations appear interactively on a map.
Restart the Chat
Use the Clear Chat button to start a new conversation.
Code Overview
1. app.py
Main script that handles the following:
Streamlit Interface: Renders the chatbot UI and map display.
Chat Logic: Processes user input, manages chat history, and generates GPT-based responses.
Recommendation Engine: Fetches personalized suggestions via the Google Maps API.
2. maps_api.py
Manages all interactions with the Google Maps API:
Geocodes user-provided locations into latitude and longitude.
Fetches nearby places based on activity types and keywords (e.g., cafes, parks, anime expos).
3. utils.py
Implements ML logic:
Emotion Classification: Uses sentiment analysis and predefined keywords to classify moods.
Recommendation Refinement: Incorporates PCA, K-NN, and decision trees to match emotions to relevant activities.
Reinforcement Learning: Updates activity recommendations over time using Q-Learning.
4. data/activities.csv
A curated dataset of 500+ activities, including categories like:
Cafes, spas, parks
Anime expos, amusement parks, bars
Technologies Used
OpenAI GPT-4: For natural language understanding and response generation.
Google Maps API: To fetch geolocation data and real-time activity suggestions.
Streamlit: For building an interactive and user-friendly web interface.
Scikit-Learn: Implemented PCA, K-NN, and decision trees for activity clustering and matching.
Reinforcement Learning: Q-Learning approach to improve activity recommendations based on user interactions.
File Structure
bash
Copy code
moodgpt/
├── app.py               # Main Streamlit application
├── maps_api.py          # Google Maps API logic
├── utils.py             # ML methods: classification and reinforcement learning
├── data/
│   └── activities.csv   # Curated activity dataset
├── requirements.txt     # Dependencies
├── .env                 # API Keys (user-created)
├── static/
│   └── star.jpg         # Background image
└── README.md            # Project documentation
Sample Output
Chatbot Conversation
bash
Copy code
MoodGPT: Hi there! I’m Yuki Asuna. How are you feeling today?  
You: I’m feeling a bit tired.  
MoodGPT: I’m sorry to hear that. Would you like some suggestions to unwind?  
MoodGPT: Here are some relaxing activities nearby:  
1. Bliss Yoga Studio - 123 Main St.  
2. Cloud 9 Spa - 456 Elm St.  
3. Nature Walk Trail - Central Park.  
Interactive Map
Displays real-time activity locations dynamically based on user input and geolocation.
Contributing
We welcome contributions!

Fork the repository.
Create a feature branch:
bash
Copy code
git checkout -b feature-name
Commit your changes:
bash
Copy code
git commit -m "Add feature"
Push to your branch:
bash
Copy code
git push origin feature-name
Open a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
Author: Yan Li
Email: yan61@illinois.edu
GitHub: yanzzzk

Feel free to explore the app or contribute to its growth! 🎉
