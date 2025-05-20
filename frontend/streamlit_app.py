import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

st.set_page_config(page_title="🎥 Anime Recommender", layout="wide")
st.markdown("<h1 style='text-align: center;'>🎌 Anime Recommendation Engine</h1>", unsafe_allow_html=True)
st.markdown("Get suggestions based on your favorite anime! 🔍")

# ------------------- Load Titles & Poster ---------------------
@st.cache_data(show_spinner=False)
def load_valid_anime_titles():
    valid_titles_path = "../data/valid_titles.csv"
    df = pd.read_csv("../data/anime.csv")
    df.dropna(subset=["name", "genre"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    unique_titles = df["name"].unique().tolist()

    if os.path.exists(valid_titles_path):
        valid_df = pd.read_csv(valid_titles_path)
        return sorted(valid_df["name"].tolist()), df

    valid_titles = []
    with st.spinner("🔍 Validating anime titles... This may take a few moments."):
        progress_bar = st.progress(0)
        for i, title in enumerate(unique_titles):
            try:
                r = requests.get(f"http://localhost:8000/recommend/{title}", timeout=3)
                d = r.json()
                if "recommendations" in d and d["recommendations"]:
                    valid_titles.append(title)
            except:
                pass
            progress_bar.progress((i + 1) / len(unique_titles))

        pd.DataFrame(valid_titles, columns=["name"]).to_csv(valid_titles_path, index=False)
        st.success(f"✅ Valid titles saved to {valid_titles_path}.")
    return sorted(valid_titles), df

def fetch_anime_poster(title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            results = response.json().get("data")
            if results:
                return results[0].get("images", {}).get("jpg", {}).get("large_image_url", None)
    except:
        pass
    return None

# ------------------- Sidebar Filters ---------------------
anime_titles, full_df = load_valid_anime_titles()
all_genres = sorted(set(g.strip() for sublist in full_df["genre"].dropna().str.split(", ") for g in sublist))

st.sidebar.header("🔧 Filters")
selected_genre = st.sidebar.selectbox("🎭 Filter by Genre", ["All"] + all_genres)
min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 10.0, 7.0, step=0.1)
min_members = st.sidebar.slider("👥 Minimum Members", 0, 1000000, 10000, step=10000)

# ------------------- Tabs ---------------------
tab1, tab2 = st.tabs(["🎯 Recommend", "🔥 Top Rated"])
results = pd.DataFrame()
top_df = pd.DataFrame()

# ------------------- Tab 1: Recommend ---------------------
with tab1:
    selected_title = st.selectbox("🎯 Select an Anime Title:", anime_titles)
    if st.button("🚀 Recommend"):
        with st.spinner("Fetching recommendations..."):
            try:
                r = requests.get(f"http://localhost:8000/recommend/{selected_title}")
                data = r.json()
                if "recommendations" in data:
                    results = pd.DataFrame(data["recommendations"])
                    results = results[(results["rating"] >= min_rating) & (results["members"] >= min_members)]

                    if selected_genre != "All":
                        results = results[results["genre"].str.contains(selected_genre)]

                    if results.empty:
                        st.warning("No recommendations found for selected filters.")
                    else:
                        st.markdown("### 🧠 Recommendations")
                        for i in range(0, len(results), 2):
                            cols = st.columns(2)
                            for j in range(2):
                                if i + j < len(results):
                                    row = results.iloc[i + j]
                                    with cols[j]:
                                        st.image(fetch_anime_poster(row["name"]) or "", width=160)
                                        st.markdown(f"**{row['name']}**")
                                        st.caption(f"🎭 {row['genre']}")
                                        st.metric("⭐ Rating", round(row["rating"], 2))
                                        st.metric("👥 Members", int(row["members"]))
                else:
                    st.warning(data.get("message", "No recommendations found."))
            except Exception as e:
                st.error(f"Error: {e}")

    # 📊 Genre Bar Chart for Recommendations
    if not results.empty and "genre" in results.columns:
        genre_lists = results["genre"].dropna().str.split(", ")
        genre_flat = [g.strip() for sublist in genre_lists for g in sublist]
        genre_counts = pd.Series(genre_flat).value_counts().reset_index()
        genre_counts.columns = ["Genre", "Count"]

        st.markdown("### 📊 Genre Distribution (Recommendations)")
        fig = px.bar(genre_counts, x="Genre", y="Count", color="Genre")
        st.plotly_chart(fig, use_container_width=True)

# ------------------- Tab 2: Top Rated ---------------------
with tab2:
    if st.button("🔥 Load Top Anime"):
        with st.spinner("Loading top anime..."):
            try:
                r = requests.get("http://localhost:8000/recommend/top?limit=10")
                data = r.json()

                if isinstance(data, dict) and "top" in data:
                    top_df = pd.DataFrame(data["top"])

                    if selected_genre != "All":
                        top_df = top_df[top_df["genre"].str.contains(selected_genre)]

                    st.markdown("### 🏆 Top Rated Anime")
                    for i in range(0, len(top_df), 2):
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(top_df):
                                row = top_df.iloc[i + j]
                                with cols[j]:
                                    st.image(fetch_anime_poster(row["name"]) or "", width=160)
                                    st.markdown(f"**{row['name']}**")
                                    st.caption(f"🎭 {row['genre']}")
                                    st.metric("⭐ Rating", round(row["rating"], 2))
                                    st.metric("👥 Members", int(row["members"]))
                else:
                    st.error("❌ 'top' key missing in backend response.")
                    st.json(data)

            except Exception as e:
                st.error(f"Error loading top anime: {e}")

    # 📊 Genre Bar Chart for Top Rated
    if not top_df.empty and "genre" in top_df.columns:
        genre_lists = top_df["genre"].dropna().str.split(", ")
        genre_flat = [g.strip() for sublist in genre_lists for g in sublist]
        genre_counts = pd.Series(genre_flat).value_counts().reset_index()
        genre_counts.columns = ["Genre", "Count"]

        st.markdown("### 📊 Genre Distribution (Top Rated)")
        fig = px.bar(genre_counts, x="Genre", y="Count", color="Genre")
        st.plotly_chart(fig, use_container_width=True)
