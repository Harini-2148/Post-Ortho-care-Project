import pyodbc
import os
import openai
import json
from dotenv import load_dotenv
import sqlite3

# ✅ Load environment variables
load_dotenv(override=True)

# ✅ Azure SQL Connection Details
server = os.getenv('SQL_SERVER')
database = "darden_poc"
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
driver = "{ODBC Driver 17 for SQL Server}"

# ✅ OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')  
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')  
deployment_name = os.getenv('AZURE_OPENAI_DEPLOYED_MODEL_NAME')  

# ✅ Validate required OpenAI variables
if not all([openai.api_base, openai.api_key, deployment_name]):
    raise ValueError("❌ Missing Azure OpenAI configuration. Check environment variables!")

# ✅ Connect to Azure SQL Database
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Establish database connection
conn = sqlite3.connect('darden_poc.db')
cursor = conn.cursor()

# Fetch chunk data for all rows
fetch_query = """
SELECT did, chunk_1, chunk_2, chunk_3, chunk_4, chunk_5, 
       chunk_6, chunk_7, chunk_8, chunk_9, chunk_10, 
       chunk_11, chunk_12 
FROM ksdev1.tmp_stg
"""
cursor.execute(fetch_query)
rows = cursor.fetchall()

# Function to generate embeddings
def generate_embedding(text):
    """Generate embedding for the input text using Azure OpenAI."""
    if text is None:
        return None  # Use None for empty chunks

    try:
        response = openai.Embedding.create(
            input=[text],  # Must be a list
            deployment_id=deployment_name  # Correct parameter for Azure
        )
        # Extract embedding vector
        embedding = response.data[0].embedding  # Correct extraction
        return json.dumps(embedding)  # Convert to JSON for SQL storage
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None  # Use None in case of error

# Update query to store embeddings
update_query = """
UPDATE ksdev1.tmp_stg
SET 
    embedding_1 = ?, embedding_2 = ?, embedding_3 = ?, embedding_4 = ?, embedding_5 = ?,
    embedding_6 = ?, embedding_7 = ?, embedding_8 = ?, embedding_9 = ?, embedding_10 = ?,
    embedding_11 = ?, embedding_12 = ?
WHERE did = ?
"""

# Process each row and generate embeddings
for row in rows:
    doc_id = row[0]  # Extract document ID
    chunks = row[1:13]  # Extract chunk_1 to chunk_12

    # Generate embeddings for all chunks
    embeddings = [generate_embedding(chunk) for chunk in chunks]

    # Debug: Check generated embeddings
    print(f"Embeddings for doc_id {doc_id}: {str(embeddings[0])[:50]}...")
    print(f"Type of first embedding: {type(embeddings[0])}")  # Should be <class 'str'> 

    # Update embeddings in the database
    try:
        cursor.execute(update_query, (*embeddings, doc_id))
    except Exception as e:
        print(f"Error inserting embeddings for doc_id {doc_id}: {e}")
        continue

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Embeddings successfully generated and updated in the database!")
