from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
from transformers import pipeline

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
socketio = SocketIO(app)

# Variable to store the PDF context
pdf_context = ""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global pdf_context

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text from the uploaded PDF and store it in pdf_context
            pdf_context = extract_text_from_pdf(file_path)

            # Generate preview images for all pages in the PDF
            generate_preview_images(file_path)

            return redirect(url_for('process', filename=filename))

    return render_template('upload.html')

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_number, each_page in enumerate(pdf_document, start=1):
            text += each_page.get_text()
    return text

def generate_preview_images(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        for page in pdf_document:
            pix = page.get_pixmap()
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"page-{page.number}.png")
            pix.save(image_path)

@app.route('/process/<filename>')
def process(filename):
    # Display the first page of the PDF and show the original name
    preview_image_path = url_for('static', filename=f'uploads/page-0.png')
    original_name = secure_filename(filename)  # Get the original name in a safe manner

    return render_template('chat.html', filename=filename, preview_image=preview_image_path)
    
@socketio.on('user_message')
def handle_user_message(message):
    
    response = get_response_from_context(message)
    socketio.emit('server_response', response)

def get_response_from_context(user_message):
    global pdf_context

    # Use pipeline for question-answering
    qa_pipeline = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

    # Ask the question to the model
    result = qa_pipeline(question=user_message, context=pdf_context)

    # Get the answer from the model's response
    answer = result['answer']

    return answer

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    socketio.run(app, debug=True)
