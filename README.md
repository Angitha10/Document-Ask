# Document-Ask

This repository contains a Flask web application that allows users to upload PDF documents, extract text from them, generate preview images, and engage in a chat-like interface for asking questions about the content of the PDF. The application utilizes the PyMuPDF library for PDF processing and the Hugging Face Transformers library for question-answering.

## Interface

![Document-Ask Chat Interface](screenshots/interface_screenshot.png)

## Features
- Upload PDF documents.
- Extract text from PDFs and store it for further processing.
- Generate preview images for all pages in the PDF.
- Implement a chat interface for users to ask questions about the PDF content.
- Use a pre-trained question-answering model from Hugging Face to provide answers based on the extracted text.

## Setup Instructions

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Installation Steps

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Angitha10/Document-Ask.git
2. Navigate to the project directory:
    ```bash
    cd Document-Ask
3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
6. Run the Flask application:
    ```bash
    python app.py
7. Open your web browser and go to http://127.0.0.1:5000/ to access the application.

## Usage
1. Upload a PDF document using the provided interface.
2. The application will extract text from the PDF and generate preview images for each page.
3. Access the chat interface by navigating to the /process/<filename> route.
4. Ask questions about the PDF content in the chat interface.
5. The application will utilize a pre-trained question-answering model to provide answers based on the extracted text.
### Acknowledgments
- This project uses the Flask web framework, PyMuPDF for PDF processing, and Hugging Face Transformers for question-answering.

Feel free to contribute, report issues, or suggest improvements!