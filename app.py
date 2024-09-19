from google.cloud import storage
import pandas as pd
import streamlit as st
import io

def download_csv_from_gcs(bucket_name, file_name):
    try:
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Download the data from the blob
        data = blob.download_as_string()
        
        # Log the first few bytes of data for inspection
        st.write("Raw data snippet:")
        st.write(data.decode('utf-8')[:500])  # Display a snippet of the raw data

        # Read the CSV content using io.StringIO to convert the string into a file-like object
        df = pd.read_csv(io.StringIO(data.decode('utf-8')), delimiter=';', header=0)
        
        # Log the first few rows of the DataFrame
        st.write("DataFrame head:")
        st.write(df.head())
        
        return df
    except Exception as e:
        # Print detailed error messages
        st.error(f"Failed to download or read CSV file: {e}")
        return None

# Streamlit app
st.title("Knowledge Base Chatbot")

# Initialize df as None
df = None

# Load CSV data
bucket_name = "cakap-product"
file_name = "tvet_course_library.csv"

# Add error handling in case the file can't be loaded
try:
    df = download_csv_from_gcs(bucket_name, file_name)
    if df is not None and not df.empty:
        st.write("Knowledge Base Data Loaded:")
        st.write(df.head())  # Display the first few rows of the data
    else:
        st.warning("Data is empty or not loaded properly.")
except Exception as e:
    st.error(f"Error loading data: {e}")

# Ensure df is defined before proceeding
if df is not None and not df.empty:
    def chatbot_response(user_input, knowledge_base):
        user_input = user_input.lower()
        
        for index, row in knowledge_base.iterrows():
            # Convert row values to string and then check
            study_text = str(row.get('Study', '')).lower()
            
            if user_input in study_text:
                return str(row.get('Okupasi', 'No Okupasi Available'))
        
        return "Sorry, I don't have an answer for that."

    user_input = st.text_input("Ask me anything:")
    if user_input:
        response = chatbot_response(user_input, df)
        st.write(response)
else:
    st.warning("Data could not be loaded. Please check the file and try again.")
