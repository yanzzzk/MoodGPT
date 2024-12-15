import random
import pandas as pd
import os

DATA_PATH = "data/activities.csv"
def load_activities():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["activity_name", "type", "description"])

activities_df = load_activities()

def classify_emotion(user_input):
    user_input_lower = user_input.lower()
    if "happy" in user_input_lower:
        return "happy"
    elif "tired" in user_input_lower:
        return "tired"
    elif "bored" in user_input_lower:
        return "bored"
    else:
        return "neutral"

def get_activity_keyword(emotion):
    if emotion == "happy":
        keywords = ["amusement park", "movie theater", "anime expo", "karaoke"]
    elif emotion == "tired":
        keywords = ["yoga", "spa", "cafe", "nature walk"]
    elif emotion == "bored":
        keywords = ["bar", "theme park", "anime", "manga", "cosplay"]
    else:
        keywords = ["park", "museum", "cafe", "library"]
    return random.choice(keywords)

def refine_recommendations(recommendations, emotion):
    random.shuffle(recommendations)
    return recommendations
