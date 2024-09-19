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
    response_column = 'Judul Pelatihan'  # Column to return response from
    additional_columns = ['Durasi Pelatihan', 'Jenjang', 'Deskripsi Pelatihan']  # List additional columns to display
    
    def chatbot_response(user_input, knowledge_base, search_column, response_column, additional_columns):
        user_input = user_input.lower()
        matches = []
        
        for index, row in knowledge_base.iterrows():
            search_text = str(row.get(search_column, '')).lower()
            if user_input in search_text:
                response_info = {response_column: row.get(response_column, 'No Response Available')}
                for col in additional_columns:
                    response_info[col] = row.get(col, 'No Data Available')
                matches.append(response_info)
        
        return matches if matches else [{"message": "Sorry, I don't have an answer for that."}]

    user_input = st.text_input("Topik apa yang kamu mau pelajari:")
    if user_input:
        responses = chatbot_response(user_input, df, search_column, response_column, additional_columns)
        if responses:
            # Convert the list of dictionaries to a DataFrame
            results_df = pd.DataFrame(responses)
            st.write("Kamu bisa pilih course ini:")
            st.table(results_df)  # Display the DataFrame as a table
        else:
            st.write(responses[0]['message'])
else:
    st.warning("Data could not be loaded. Please check the file and try again.")
