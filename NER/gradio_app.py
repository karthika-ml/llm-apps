import os
from dotenv import load_dotenv,dotenv_values
import gradio as gr
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import glob
import pandas as pd
import zipfile
from io import BytesIO

load_dotenv()
# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')
# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Function to read all text files in a folder and return their contents as a list
def process_zip_file(filepath):
    documents = []
    with zipfile.ZipFile(filepath, 'r') as z:
        # Iterate through the files in the zip archive
        for file_name in z.namelist():
            if file_name.endswith(".txt"):
                with z.open(file_name) as file:
                    content = file.read().decode('utf-8')  # Decode bytes to string
                    documents.append(content)
    
    # Split the documents into batches of 5
    batches = [documents[i:i + 5] for i in range(0, len(documents), 5)]
    return batches

# @title Populate Needed categories
def category_populate(portal_input):
  # Split the documents into batches of 5
  batches = process_zip_file(portal_input)
  # Initialize an empty DataFrame to store results from all documents
  master_df = pd.DataFrame()
  # Categories to extract
  categories_to_extract = ["person", "address","skill", "organization"]

  # Process each batch of documents
  for batch in batches:
      results = client.recognize_entities(documents=batch)

      # Loop through results of the current batch
      for result in results:
          # Initialize a dictionary for storing extracted data for the current document
          doc_data = {category: pd.NA for category in categories_to_extract}  # Initialize columns with NaN (pd.NA)

          # Loop through recognized entities and fill the appropriate column
          for entity in result.entities:
              category = entity.category.lower()
              if category in categories_to_extract:
                  # If the category already has text, append with a separator (if needed)
                  if pd.isna(doc_data[category]):
                      doc_data[category] = entity.text
                  else:
                      doc_data[category] += "; " + entity.text

          # Convert the dictionary to a DataFrame (single row) and append to the master DataFrame
          doc_df = pd.DataFrame([doc_data])
          master_df = pd.concat([master_df, doc_df], ignore_index=True)
  return master_df

if __name__ == "__main__":
    # Gradio interface setup
    inputs = gr.components.File(label="Upload Zip File", type="filepath")
    outputs = gr.components.Dataframe(label="Extracted Entities", headers=["Filename", "Content"])

    iface = gr.Interface(
        fn=category_populate,
        inputs=inputs,
        outputs=outputs,
        title="Document Processing with Zip File"
    )

    iface.launch()