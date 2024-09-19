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
        # st.write("Raw data snippet:")
        # st.write(data.decode('utf-8')[:500])  # Display a snippet of the raw data

        # Read the CSV content using io.StringIO to convert the string into a file-like object
        df = pd.read_csv(io.StringIO(data.decode('utf-8')), delimiter=';', header=0)
        
        # Log the first few rows of the DataFrame
        # st.write("DataFrame head:")
        # st.write(df.head())
        
        return df
    except Exception as e:
        # Print detailed error messages
        st.error(f"Failed to download or read CSV file: {e}")
        return None

# Streamlit app
st.title("Upskill Cakap Product")

# Initialize df as None
df = None

# Load CSV data
bucket_name = "cakap-product"
file_name = "tvet_course_library.csv"

def chatbot_response(user_input, knowledge_base, search_column, response_column):
    user_input = user_input.lower()
    
    # Iterate over rows and check for the presence of user_input in the search_column
    for index, row in knowledge_base.iterrows():
        # Convert column data to string and lower case
        search_text = str(row.get(search_column, '')).lower()
        
        # Check if user_input is a substring of search_text
        if user_input in search_text:
            # Return the corresponding value from response_column
            return str(row.get(response_column, 'No Response Available'))
    
    # Return a default message if no match is found
    return "Sorry, I don't have an answer for that."

