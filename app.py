from google.cloud import storage
import pandas as pd
import streamlit as st

def download_csv_from_gcs(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_string()
    return pd.read_csv(pd.compat.StringIO(data.decode('utf-8')))

# Streamlit app
st.title("Knowledge Base Chatbot")

# Load CSV data
bucket_name = "cakap-product"
file_name = "tvet_course_library.csv"
df = download_csv_from_gcs(bucket_name, file_name)

st.write("Knowledge Base Data Loaded:")
st.write(df.head())

def chatbot_response(user_input, knowledge_base):
    for index, row in knowledge_base.iterrows():
        if user_input.lower() in row['Study'].lower():
            return row['Okupasi']
    return "Sorry, I don't have an answer for that."

# Streamlit chatbot interface
user_input = st.text_input("Ask me anything:")
if user_input:
    response = chatbot_response(user_input, df)
    st.write(response)
