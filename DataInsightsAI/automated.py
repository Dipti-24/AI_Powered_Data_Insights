import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import requests
from config import DEEPSEEK_API_KEY  


# print(DEEPSEEK_API_KEY)
# Define API URL
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Streamlit UI
st.title("🚀 AI-Powered Data Insights")

# File Upload or SQL Connection
option = st.radio("📊 Select Data Source:", ("Upload File", "Connect to SQL Database"))

df = None
if option == "Upload File":
    uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1]
        df = pd.read_csv(uploaded_file) if file_extension == "csv" else pd.read_excel(uploaded_file)

elif option == "Connect to SQL Database":
    db_file = st.text_input("🔗 Enter SQLite database file path:")
    query = st.text_area("📝 Enter SQL query:")
    if st.button("Run Query") and db_file and query:
        try:
            conn = sqlite3.connect(db_file)
            df = pd.read_sql_query(query, conn)
        except Exception as e:
            st.error(f" Error executing query: {e}")
        finally:
            conn.close()

if df is not None:
    st.write("###  Preview of Data:")
    st.write(df.head())

    # Clean Data (Remove Nulls, Handle Duplicates)
    st.write("###  Data Cleaning")
    if st.button("Clean Data"):
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        st.success("✅ Data cleaned successfully!")
        st.write(df.head())

    # Generate Summary
    data_summary = df.describe().to_string()

    # Prepare payload for DeepSeek API
    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": f"Analyze the following dataset and provide insights:\n\n{data_summary}"}
        ],
        "stream": False
    }
    
  
    headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
    }

    # Make API request
    response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)

    # Check response
    if response.status_code == 200:
        insights = response.json()["choices"][0]["message"]["content"]
        st.write("### 🤖 AI-Generated Insights:")
        st.write(insights)

      
    else:
        st.error(f" Error: {response.status_code} - {response.text}")

    # NLP-Based Queries
    st.write("### 💡 Ask AI a Question About Your Data:")
    user_query = st.text_input("Enter your question:")
    
    if user_query:
        query_payload = {
            "model": "mistralai/mistral-small-3.2-24b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": f"Based on this dataset, answer: {user_query}\n\nDataset:\n{df.to_string()}"}
            ],
            "stream": False
        }

        # Make API request
        query_response = requests.post(DEEPSEEK_API_URL, json=query_payload, headers=headers)

        # Check response
        if query_response.status_code == 200:
            response_text = query_response.json()["choices"][0]["message"]["content"]
            st.write("###  AI Response:")
            st.write(response_text)
        else:
            st.error(f" Error: {query_response.status_code} - {query_response.text}")

    # Data Visualization
    st.write("###  Data Visualization:")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        selected_col = st.selectbox(" Select a column to visualize:", numeric_cols)

        # Histogram
        fig, ax = plt.subplots()
        sns.histplot(df[selected_col], kde=True, ax=ax)
        st.pyplot(fig)

        # Correlation Heatmap
        if len(numeric_cols) > 1:
            st.write("###  Correlation Heatmap:")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
            st.pyplot(fig)
    else:
        st.write(" No numeric columns found for visualization.")

