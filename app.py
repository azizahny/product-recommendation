from google.cloud import storage
import pandas as pd
import streamlit as st
import io

def download_csv_from_gcs(bucket_name, file_name):
    try:
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Check if blob exists
        if not blob.exists():
            raise FileNotFoundError(f"The file {file_name} does not exist in bucket {bucket_name}.")
        
        # Download the data from the blob
        data = blob.download_as_string()
        
        # Read the CSV content using io.StringIO to convert the string into a file-like object
        df = pd.read_csv(io.StringIO(data.decode('utf-8')), delimiter=';', header=0)
        
        return df
    except Exception as e:
        # Log detailed error messages
        st.error(f"Failed to download or read CSV file: {e}")
        return None

# Streamlit app
st.title("Upskill Cakap Product")

# Load CSV data
df = download_csv_from_gcs("cakap-product", "tvet_course_library.csv")

# Ensure df is defined before proceeding
if df is not None and not df.empty:
    # Specify the columns for searching and responding
    search_column = 'Topik Utama'   # Column to search for user input
    response_column = 'Okupasi'  # Column to return response from

    def chatbot_response(user_input, knowledge_base, search_column, response_column):
        user_input = user_input.lower()
        matches = []
        
        for index, row in knowledge_base.iterrows():
            search_text = str(row.get(search_column, '')).lower()
            if user_input in search_text:
                matches.append(str(row.get(response_column, 'No Response Available')))
        
        return matches if matches else ["Sorry, I don't have an answer for that."]

    user_input = st.text_input("Ask me anything:")
    if user_input:
        responses = chatbot_response(user_input, df, search_column, response_column)
        if responses:
            st.write("Here are the possible matches:")
            for response in responses:
                st.write(f"- {response}")
else:
    st.warning("Data could not be loaded. Please check the file and try again.")
