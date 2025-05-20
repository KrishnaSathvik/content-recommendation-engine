
# 🎌 Anime Recommendation Engine

A content-based anime recommender built with FastAPI (backend) and Streamlit (frontend). It uses genre-based TF-IDF similarity and shows poster cards with filters.

---

## 🔧 Tech Stack
- Python 3.10+
- FastAPI
- Streamlit
- Scikit-learn
- Pandas
- Plotly
- Jikan API

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/content-recommendation-engine.git
cd content-recommendation-engine
```

### 2️⃣ Install Python Virtual Environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3️⃣ Backend Setup (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -c "from recommender import train_model; train_model()"  # Train the model
uvicorn app:app --reload --port 8000
```

### 4️⃣ Frontend Setup (Streamlit)
Open a new terminal:

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
content-recommendation-engine/
├── backend/
│   ├── app.py
│   ├── recommender.py
│   ├── models/
│   │   └── anime_model.pkl
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── data/
│   ├── anime.csv
│   └── valid_titles.csv
├── .gitignore
├── README.md
```

---

## 🎯 Features

- 🎥 Recommends anime based on genre similarity (TF-IDF + Cosine)
- 🎭 Filter by genre, rating, and member count
- 🏆 View top-rated anime across all genres
- 📊 Genre distribution bar chart for each recommendation set
- 🖼 Posters fetched from Jikan API (MyAnimeList)
- 🧠 Grid layout cards for clean, visual display

---

## 🧪 Example API Endpoints

| Method | Endpoint                          | Description                         |
|--------|-----------------------------------|-------------------------------------|
| GET    | `/recommend/{title}`              | Recommend anime based on title     |
| GET    | `/recommend/top?limit=10`         | Get top-rated anime list           |

---

## 📦 Requirements

### `backend/requirements.txt`
```txt
fastapi
uvicorn
pandas
scikit-learn
joblib
```

### `frontend/requirements.txt`
```txt
streamlit
pandas
requests
plotly
```

---

## 📌 Notes
- Requires `anime.csv` dataset (place in `data/` folder)
- Automatically caches valid anime titles to `valid_titles.csv`
- Handles errors gracefully and shows fallback if posters are missing

---

## 📄 License
MIT
