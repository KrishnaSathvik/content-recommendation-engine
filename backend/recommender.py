import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Base directory resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "anime.csv")
MODEL_PATH = os.path.join(BASE_DIR, "backend", "models", "anime_model.pkl")

def load_anime_data():
    df = pd.read_csv(CSV_PATH)
    df.dropna(subset=["genre", "name"], inplace=True)
    df = df.sort_values(by="members", ascending=False).head(1000).reset_index(drop=True)
    return df

def train_model():
    df = load_anime_data()

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["genre"])

    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    joblib.dump((df, similarity_matrix), MODEL_PATH)
    print(f"✅ Model trained and saved to {MODEL_PATH}")

def get_recommendations(title, top_n=5):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained. Please run train_model() first.")

    df, similarity_matrix = joblib.load(MODEL_PATH)

    if title not in df["name"].values:
        return []

    index = df[df["name"] == title].index[0]
    sim_scores = list(enumerate(similarity_matrix[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    similar_indices = [i for i, _ in sim_scores[1:top_n + 1]]
    return df.iloc[similar_indices][["name", "genre", "rating", "members"]].to_dict(orient="records")
