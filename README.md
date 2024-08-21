# OpenAI Vector Store File Upload

This is a test script to upload files into OpenAI’s vector database. My low-code platform, n8n, doesn’t currently support this functionality directly, so I’m using this script as middleware to bridge the gap and ensure my AI assistants can operate seamlessly.

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Endpoints](#endpoints)
5. [Supported File Types](#supported-file-types)
6. [Learnings](#learnings)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

This repository contains a FastAPI application that allows for file uploads to OpenAI's vector database. It acts as middleware to handle file uploads and batch creation, bridging the gap for platforms like n8n that currently lack this direct functionality.

## Setup

### Prerequisites
- Python 3.7+
- A valid OpenAI API key
- `pip` installed

### Installation

1. Clone the repository:
    ```sh
    git clone [https://github.com/wukimidaire/vector_file_upload_api/](https://github.com/wukimidaire/vector_file_upload_api/)
    ```

2. Navigate to the project directory:
    ```sh
    cd your-repo-name
    ```
   
3. Create a virtual environment:
    ```sh
    python -m venv env
    ```

4. Activate the virtual environment:

    - On Windows:
    ```sh
    .\env\Scripts\activate
    ```
    - On macOS/Linux:
    ```sh
    source env/bin/activate
    ```

5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Create a `.env` file based on the `.env.example` and add your OpenAI API key:
    ```sh
    cp .env.example .env
    ```
    Add your API key to the `.env` file:
    ```
    OPENAI_API_KEY=your-openai-api-key
    ```

## Usage

Run the FastAPI application using Uvicorn:
```sh
uvicorn app:app --reload
The API will be available at http://127.0.0.1:8000.

Endpoints
POST /add_file_to_vector_store_batch
Upload a file and create a vector store file batch.

Request Parameters:

vector_store_id (form): The ID of the vector store.
file (form): The file to be uploaded.
Example Request:

curl -X POST "http://127.0.0.1:8000/add_file_to_vector_store_batch" -F "vector_store_id=your vector store id" -F "file=@path/to/your/file"
Supported File Types
The following file extensions are supported for upload:

.c, .cs, .cpp, .doc, .docx, .html, .java
.json, .md, .pdf, .php, .pptx, .py
.rb, .tex, .txt, .css, .js, .sh, .ts
Learnings
Throughout the development of this script, we encountered several challenges and resolved them as follows:

Invalid purpose Parameter: Initially, the wrong purpose ('vector-store') was used for file uploads. It was corrected to 'user_data'.
Error Handling: Implemented correct error handling for various exceptions, including incorrect API calls and unsupported file types.
Supported File Types: Incorporated comprehensive validation for file extensions based on OpenAI's supported file types.
Beta Header Requirement: Included necessary headers (OpenAI-Beta) to access specific OpenAI API functionalities.
Creating File Batches: Adapted the code to support creating file batches using the correct API endpoints and parameters.
Contributing
Contributions are welcome! Please create an issue or submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
