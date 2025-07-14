import streamlit as st
import requests
import pandas as pd

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Job Matching - Telkom", layout="centered")

# --- Judul dan Header ---
st.markdown("""
    <h1 style='color:#d71920;'>🔍 Job Matching Recommendation</h1>
    <p>Masukkan deskripsi kebutuhan posisi dan sistem akan merekomendasikan 5 mentee terbaik.</p>
""", unsafe_allow_html=True)

# --- Form Input ---
with st.form("job_matching_form"):
    st.subheader("📝 Deskripsi Posisi Pekerjaan")

    job_position = st.text_input("Job Position")
    required_tools = st.text_area("Required Tools (Pisahkan dengan koma)")
    required_skills = st.text_area("Required Skills (Pisahkan dengan koma)")
    required_role_title = st.text_input("Role Title")

    submitted = st.form_submit_button("🔎 Cari Rekomendasi")

# --- Submit Request ---
if submitted:
    if not all([job_position, required_tools, required_skills, required_role_title]):
        st.warning("Mohon lengkapi semua field.")
    else:
        try:
            with st.spinner("Mengirim data ke sistem..."):
                # Endpoint backend
                url = "http://jobmatch_api:8000/recommend"
                headers = {
                    "x-api-key": "internship2025"
                }
                payload = {
                    "job_position": job_position,
                    "required_tools": required_tools,
                    "required_skills": required_skills,
                    "required_role_title": required_role_title
                }

                response = requests.post(url, json=payload, headers=headers)

            # --- Tampilkan Hasil ---
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ {len(data['top_recommendations'])} Rekomendasi ditemukan dalam {data['elapsed_time_seconds']} detik")
                
                # Buat tabel dari hasil
                df = pd.DataFrame(data["top_recommendations"])
                df = df.rename(columns={
                    "rank": "Ranking",
                    "mentee_name": "Nama",
                    "mentee_title": "Judul",
                    "mentee_skill": "Skill",
                    "mentee_tools": "Tools",
                    "mentee_position": "Posisi",
                    "score": "Skor"
                })
                st.dataframe(df.style.highlight_max(axis=0, subset=["Skor"], color="#d71920"))
            else:
                st.error(f"Terjadi kesalahan: {response.text}")
        except Exception as e:
            st.error(f"Gagal menghubungi backend: {e}")