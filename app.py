from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from dotenv import load_dotenv
import openai
import requests
import os
import io
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# List of supported file extensions
SUPPORTED_EXTENSIONS = [
    '.c', '.cs', '.cpp', '.doc', '.docx', '.html', '.java', 
    '.json', '.md', '.pdf', '.php', '.pptx', '.py', 
    '.rb', '.tex', '.txt', '.css', '.js', '.sh', '.ts'
]


async def upload_file_to_openai(file: UploadFile):
    try:
        # Check if the file has a filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="File has no filename.")
        
        # Get the file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # Check if the file extension is supported
        if not file_extension or file_extension not in SUPPORTED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file extension: {file_extension}. Supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}")
        
        # Read the file's content
        file_content = await file.read()
        
        # Upload the file to OpenAI for 'user_data' purpose
        uploaded_file = openai.File.create(
            file=io.BytesIO(file_content),
            purpose='user_data'
        )
        return uploaded_file['id']
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Failed to upload file to OpenAI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file to OpenAI: {str(e)}")


@app.post('/add_file_to_vector_store')
async def add_file_to_vector_store(vector_store_id: str = Form(...), file: UploadFile = File(...)):
    try:
        # Upload the file to OpenAI and get the file_id
        file_id = await upload_file_to_openai(file)
        
        # Add the uploaded file to the vector store manually with requests
        url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}/files"
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        data = {
            "file_id": file_id
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code != 200:
            logger.error(f"Error updating vector store: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        return response.json()
    
    except openai.error.InvalidRequestError as e:
        logger.error(f"Invalid request to OpenAI: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid request to OpenAI: {str(e)}")
    except Exception as e:
        logger.error(f"Error updating vector store: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating vector store: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
    
    