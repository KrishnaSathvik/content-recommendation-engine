from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender import get_recommendations
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "../data/anime.csv")


# Allow all origins (good for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Anime Recommendation Engine API is running."}

@app.get("/recommend/top")
def top_anime(limit: int = 10):
    import pandas as pd
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["name", "genre", "rating", "members"])
    df = df[df["rating"] > 0]
    top_df = df.sort_values(by=["rating", "members"], ascending=[False, False]).head(limit)
    return {
        "top": top_df[["name", "genre", "rating", "members"]].to_dict(orient="records")
    }

@app.get("/recommend/{title}")
def recommend(title: str):
    from recommender import get_recommendations
    results = get_recommendations(title)
    if results:
        return {"recommendations": results}
    else:
        return {"message": "Anime not found or no similar recommendations."}

