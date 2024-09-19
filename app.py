from google.cloud import storage
import pandas as pd
import streamlit as st
import io

def download_csv_from_gcs(bucket_name, file_name):
    # Create a storage client and fetch the bucket
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Download the data from the blob
    data = blob.download_as_string()
    
    # Read the CSV content using io.StringIO to convert the string into a file-like object
    return pd.read_csv(io.StringIO(data.decode('utf-8')))

# Streamlit app
st.title("Knowledge Base Chatbot")

# Initialize df as None or an empty DataFrame
df = None

# Load CSV data
bucket_name = "cakap-product"  # Ensure this bucket exists and is accessible
file_name = "tvet_course_library.csv"  # Ensure this file exists in the bucket

# Add error handling in case the file can't be loaded
try:
    df = download_csv_from_gcs(bucket_name, file_name)
    st.write("Knowledge Base Data Loaded:")
    st.write(df.head())  # Display the first few rows of the data
except Exception as e:
    st.error(f"Error loading data: {e}")

# Ensure df is defined before proceeding
if df is not None:
    # Chatbot response logic
    def chatbot_response(user_input, knowledge_base):
        # Iterate over each row in the DataFrame to find a match for the user's query
        for index, row in knowledge_base.iterrows():
            # If user input matches any value in the 'Study' column, return the corresponding 'Okupasi'
            if user_input.lower() in row['Study'].lower():
                return row['Okupasi']
        return "Sorry, I don't have an answer for that."

    # Streamlit chatbot interface
    user_input = st.text_input("Ask me anything:")
    if user_input:
        # Get response from the chatbot function
        response = chatbot_response(user_input, df)
        st.write(response)
else:
    st.warning("Data could not be loaded. Please check the file and try again.")
