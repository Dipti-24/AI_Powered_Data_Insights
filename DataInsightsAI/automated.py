import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import requests
import time
import os

from config import DEEPSEEK_API_KEY  # securely stored API key

# ===== Rate Limit Setup =====
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"
COOLDOWN_SECONDS = 60
MAX_DAILY_CALLS = 10

def is_rate_limited():
    current_time = time.time()
    if "last_request_time" not in st.session_state:
        st.session_state.last_request_time = 0
    if "daily_uses" not in st.session_state:
        st.session_state.daily_uses = 0
    elapsed = current_time - st.session_state.last_request_time
    if st.session_state.daily_uses >= MAX_DAILY_CALLS:
        return "quota_exceeded", 0
    elif elapsed < COOLDOWN_SECONDS:
        return "cooldown", int(COOLDOWN_SECONDS - elapsed)
    else:
        st.session_state.last_request_time = current_time
        st.session_state.daily_uses += 1
        return "ok", 0

# ===== UI =====
st.set_page_config(page_title="AI-Powered Data Insights", layout="wide")
st.title("🚀 AI-Powered Data Insights")

if "daily_uses" in st.session_state:
    st.info(f"🧾 Used {st.session_state.daily_uses}/{MAX_DAILY_CALLS} daily quota.")

option = st.radio("📊 Select Data Source:", ("Upload File", "Connect to SQL Database"))
df = None

if option == "Upload File":
    uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1]
        df = pd.read_csv(uploaded_file) if file_extension == "csv" else pd.read_excel(uploaded_file)

elif option == "Connect to SQL Database":
    db_file = st.text_input("🔗 Enter SQLite database path:")
    query = st.text_area("📝 Enter SQL query:")
    if st.button("Run Query") and db_file and query:
        try:
            conn = sqlite3.connect(db_file)
            df = pd.read_sql_query(query, conn)
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            conn.close()

if df is not None:
    st.write("### 👀 Data Preview")
    st.dataframe(df.head())

    st.write("### 🧹 Clean Data")
    if st.button("Clean Data"):
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        st.success("✅ Cleaned!")
        st.dataframe(df.head())

    st.write("### 🤖 AI Insights")
    rate_status, wait_time = is_rate_limited()

    if rate_status == "quota_exceeded":
        st.warning("🚫 Daily quota exceeded. Try tomorrow.")
    elif rate_status == "cooldown":
        st.warning(f"⏳ Wait {wait_time}s before next request.")
    else:
        summary = df.describe().to_string()
        payload = {
            "model": "mistralai/mistral-small-3.2-24b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": f"Analyze the following dataset:\n{summary}"}
            ],
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            insights = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Insights ready!")
            st.write(insights)
        else:
            st.error(f"❌ API Error: {response.status_code}")

    st.write("### 💬 Ask AI a Question:")
    user_q = st.text_input("Your question:")
    if user_q:
        rate_status, wait_time = is_rate_limited()
        if rate_status == "quota_exceeded":
            st.warning("🚫 Daily query limit reached.")
        elif rate_status == "cooldown":
            st.warning(f"⏳ Wait {wait_time}s before next question.")
        else:
            query_payload = {
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are a data analyst."},
                    {"role": "user", "content": f"Based on this dataset, answer: {user_q}\n\n{df.to_string()}"}
                ],
                "stream": False
            }
            query_response = requests.post(DEEPSEEK_API_URL, json=query_payload, headers=headers)
            if query_response.status_code == 200:
                st.write(query_response.json()["choices"][0]["message"]["content"])
            else:
                st.error("❌ Error in response")

    st.write("### 📊 Data Visualization")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        col = st.selectbox("Select column:", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

        if len(numeric_cols) > 1:
            st.write("### 🔥 Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)
    else:
        st.info("No numeric columns found.")
