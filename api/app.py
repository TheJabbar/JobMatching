from fastapi import FastAPI, Request, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
import joblib
import pandas as pd
from pydantic import BaseModel
import time


# Load model dan vectorizer
RandomForestClassifier = joblib.load("app/model/matching-model.pkl")
vectorizer = joblib.load("app/model/tf-idfvectorizer.pkl")

# Load data mentee untuk scoring
mentee_data = pd.read_csv("app/data/new_mentee.csv")
mentee_data.fillna('', inplace=True)

# Kolom yang akan digabung untuk vectorizer input
text_cols = ['job_position', 'required_tools', 'required_skills', 'required_role_title',
             'mentee_name', 'mentee_title', 'mentee_skill', 'mentee_tools', 'mentee_position']

# FastAPI setup
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key valid
API_KEY = "internship2025"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Request body schema
class RoleRequest(BaseModel):
    job_position: str
    required_tools: str
    required_skills: str
    required_role_title: str

@app.post("/recommend")
async def recommend_mentees(
    request: Request,
    role: RoleRequest,
    api_key: str = Security(api_key_header)
):
    # Start timer
    start_time = time.time()

    # Validasi API Key
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Salin data mentee dan masukkan data request mentor ke kolom input
    df = mentee_data.copy()
    df['job_position'] = role.job_position
    df['required_tools'] = role.required_tools
    df['required_skills'] = role.required_skills
    df['required_role_title'] = role.required_role_title

    # Gabungkan semua kolom teks menjadi satu string
    df['combined_text'] = df[text_cols].agg(' '.join, axis=1)

    # Transform teks dengan vectorizer
    X_input = vectorizer.transform(df['combined_text'])

    # Prediksi probabilitas diterima
    if hasattr(RandomForestClassifier, "predict_proba"):
        proba = RandomForestClassifier.predict_proba(X_input)[:, 1]
    else:
        proba = RandomForestClassifier.predict(X_input)

    # Tambahkan skor ke dataframe
    df['recommendation_score'] = proba

    # Urutkan hasil berdasarkan skor tertinggi
    sorted_recommendations = df.sort_values(by='recommendation_score', ascending=False)

    # Ambil top 5 hasil terbaik
    top_n = sorted_recommendations.head(5)

    # Buat list hasil dengan ranking dan pembulatan skor
    recommendations = []
    for idx, row in top_n.iterrows():
        recommendations.append({
            "rank": len(recommendations) + 1,
            "mentee_name": row['mentee_name'],
            "mentee_title": row['mentee_title'],
            "mentee_skill": row['mentee_skill'],
            "mentee_tools": row['mentee_tools'],
            "mentee_position": row['mentee_position'],
            "score": round(row['recommendation_score'], 4)
        })

    end_time = time.time()  
    elapsed_time = round(end_time - start_time, 3)

    return {
        "status": "success",
        "elapsed_time_seconds": elapsed_time,
        "top_recommendations": recommendations
    }

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Job Matching API is running"}
