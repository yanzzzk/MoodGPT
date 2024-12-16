import random
import pandas as pd
import os

# 假设我们在CS 441中学到K-NN、PCA、决策树和深度学习等方法，这里只是简单模拟逻辑，实际需训练模型。
# 在真实场景中，你会有数据集和训练过程，这里我们用简单的规则+随机模拟。

DATA_PATH = "data/activities.csv"

def load_activities():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["activity_name", "type", "description"])

activities_df = load_activities()

def classify_emotion(user_input):
    # 简单情绪分类：实际可用深度学习或Transformer模型提高准确率
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
    # 根据情绪返回不同关键词（可根据PCA/决策树等对活动类型进行优化，这里简化）
    # 示例：在真实场景中可以对activities_df进行聚类(PCA+KNN)或决策树分类找出合适类型
    if emotion == "happy":
        keywords = ["amusement park", "movie theater", "anime expo", "karaoke"]
    elif emotion == "tired":
        keywords = ["yoga", "spa", "cafe", "nature walk"]
    elif emotion == "bored":
        keywords = ["bar", "theme park", "anime", "manga", "cosplay"]
    else:
        keywords = ["park", "museum", "cafe", "library"]

    # 利用PCA和KNN(伪代码)：对activities_df提取特征，将活动type转化为向量降维后匹配相似关键词
    # 这里仅示意，不做实际计算
    # pseudo_pca = PCA(...)
    # pseudo_knn = KNeighborsClassifier(...)
    # pseudo_decision_tree = DecisionTreeClassifier(...)
    # 实际训练代码略，当用户有emotion时，我们假设已训练并选择关键词
    
    return random.choice(keywords)

def refine_recommendations(recommendations, emotion):
    # 根据emotion和活动数据文件，对推荐进行微调
    # 在真实场景中可用决策树或深度学习模型排序，这里简化为随机打分
    # pseudo_decision_scores = ...
    random.shuffle(recommendations)
    return recommendations




# import random
# import pandas as pd
# import os
# from sklearn.decomposition import PCA
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier

# # Path to activities data file
# DATA_PATH = "data/activities.csv"

# # Load activity dataset
# def load_activities():
#     if os.path.exists(DATA_PATH):
#         return pd.read_csv(DATA_PATH)
#     return pd.DataFrame(columns=["activity_name", "type", "description", "features"])

# activities_df = load_activities()

# # Emotion classification based on user input
# def classify_emotion(user_input):
#     """
#     Classify emotion based on user input using simple keyword matching.
#     """
#     user_input_lower = user_input.lower()
#     if "happy" in user_input_lower:
#         return "happy"
#     elif "tired" in user_input_lower:
#         return "tired"
#     elif "bored" in user_input_lower:
#         return "bored"
#     else:
#         return "neutral"

# # Retrieve activity keyword based on emotion
# def get_activity_keyword(emotion):
#     """
#     Returns activity keyword(s) based on classified emotion.
#     """
#     emotion_keywords = {
#         "happy": ["amusement park", "movie theater", "anime expo", "karaoke"],
#         "tired": ["yoga", "spa", "cafe", "nature walk"],
#         "bored": ["bar", "theme park", "anime", "manga", "cosplay"],
#         "neutral": ["park", "museum", "cafe", "library"]
#     }
#     keywords = emotion_keywords.get(emotion, emotion_keywords["neutral"])

#     # Reduce dimensionality of activity types to simulate advanced selection (PCA example)
#     if not activities_df.empty:
#         features = activities_df["type"].str.get_dummies()  # Convert types to one-hot encoding
#         pca = PCA(n_components=2)
#         reduced_features = pca.fit_transform(features)
#         activities_df["pca1"], activities_df["pca2"] = reduced_features[:, 0], reduced_features[:, 1]
#         similar_keywords = activities_df.loc[
#             activities_df["pca1"].abs() < 1.0, "type"
#         ].unique()  # Simulated similarity based on PCA
#         keywords = list(set(keywords) & set(similar_keywords)) or keywords

#     return random.choice(keywords)

# # Refine recommendations using mock ranking
# def refine_recommendations(recommendations, emotion):
#     """
#     Refine and rank recommendations based on emotion and feature scoring.
#     """
#     if activities_df.empty:
#         return recommendations  # Return as is if no activity data

#     if emotion not in ["happy", "tired", "bored"]:
#         return recommendations

#     # Example of ranking with a simple decision tree (trained on random scores)
#     emotion_mapping = {"happy": 1, "tired": 2, "bored": 3}
#     activities_df["emotion_score"] = activities_df["type"].map(
#         lambda x: emotion_mapping.get(emotion, 0)
#     )
#     features = activities_df[["emotion_score"]].values
#     labels = activities_df.index.values

#     clf = DecisionTreeClassifier()
#     clf.fit(features, labels)

#     # Rank recommendations
#     ranked_indices = clf.predict_proba(features)[:, 1].argsort()
#     ranked_recommendations = [recommendations[i] for i in ranked_indices[: len(recommendations)]]

#     return ranked_recommendations

# # Example integration function
# def get_recommendations(user_input):
#     """
#     Integrates emotion classification, activity keyword selection,
#     and recommendation refinement to return final recommendations.
#     """
#     emotion = classify_emotion(user_input)
#     keyword = get_activity_keyword(emotion)

#     # Fetch recommendations based on keyword (mock example)
#     recommendations = activities_df.loc[activities_df["type"] == keyword].to_dict("records")
#     refined_recommendations = refine_recommendations(recommendations, emotion)

#     return refined_recommendations
