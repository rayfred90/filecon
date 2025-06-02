import os
import json
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import tempfile
import uuid
from werkzeug.utils import secure_filename

# Document processors
from processors.pdf_processor import PDFProcessor
from processors.doc_processor import DocProcessor
from processors.excel_processor import ExcelProcessor
from processors.ppt_processor import PPTProcessor
from processors.ebook_processor import EbookProcessor
from processors.text_processor import TextProcessor

# Text splitter
from text_splitter import TextSplitterService

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 
    'ppt', 'pptx', 'epub', 'mobi', 'txt', 'md',
    'js', 'ts', 'py', 'java', 'cpp', 'html', 'css', 
    'json', 'xml', 'yaml', 'sql', 'php', 'go', 'rust'
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize processors
processors = {
    'pdf': PDFProcessor(),
    'doc': DocProcessor(),
    'docx': DocProcessor(),
    'xls': ExcelProcessor(),
    'xlsx': ExcelProcessor(),
    'csv': ExcelProcessor(),
    'ppt': PPTProcessor(),
    'pptx': PPTProcessor(),
    'epub': EbookProcessor(),
    'mobi': EbookProcessor(),
    'txt': TextProcessor(),
    'md': TextProcessor(),
    'js': TextProcessor(),
    'ts': TextProcessor(),
    'py': TextProcessor(),
    'java': TextProcessor(),
    'cpp': TextProcessor(),
    'html': TextProcessor(),
    'css': TextProcessor(),
    'json': TextProcessor(),
    'xml': TextProcessor(),
    'yaml': TextProcessor(),
    'sql': TextProcessor(),
    'php': TextProcessor(),
    'go': TextProcessor(),
    'rust': TextProcessor()
}

text_splitter_service = TextSplitterService()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        stored_filename = f"{file_id}.{file_extension}"
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
        file.save(filepath)
        
        return jsonify({
            'file_id': file_id,
            'filename': filename,
            'file_type': file_extension,
            'message': 'File uploaded successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/convert', methods=['POST'])
def convert_file():
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        output_format = data.get('output_format', 'md')  # 'md' or 'json'
        
        if not file_id:
            return jsonify({'error': 'No file_id provided'}), 400
        
        # Find the uploaded file
        uploaded_file = None
        file_extension = None
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith(file_id):
                uploaded_file = filename
                file_extension = filename.rsplit('.', 1)[1].lower()
                break
        
        if not uploaded_file:
            return jsonify({'error': 'File not found'}), 404
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file)
        
        # Process file based on extension
        processor = processors.get(file_extension)
        if not processor:
            return jsonify({'error': f'No processor found for {file_extension}'}), 400
        
        # Convert to text/structured data
        content = processor.process(filepath)
        
        # Format output
        if output_format == 'json':
            output_content = json.dumps(content, indent=2, ensure_ascii=False)
            output_filename = f"{file_id}.json"
        else:  # markdown
            if isinstance(content, dict):
                output_content = processor.to_markdown(content)
            else:
                output_content = str(content)
            output_filename = f"{file_id}.md"
        
        # Save converted file
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        return jsonify({
            'file_id': file_id,
            'output_format': output_format,
            'content_preview': output_content[:500] + '...' if len(output_content) > 500 else output_content,
            'content_length': len(output_content),
            'message': 'File converted successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/split', methods=['POST'])
def split_text():
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        splitter_params = data.get('splitter_params', {})
        output_format = data.get('output_format', 'md')
        
        if not file_id:
            return jsonify({'error': 'No file_id provided'}), 400
        
        # Find the converted file
        converted_filename = f"{file_id}.{output_format}"
        converted_path = os.path.join(app.config['OUTPUT_FOLDER'], converted_filename)
        
        if not os.path.exists(converted_path):
            return jsonify({'error': 'Converted file not found. Please convert first.'}), 404
        
        # Read converted content
        with open(converted_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split text
        chunks = text_splitter_service.split_text(content, splitter_params)
        
        # Create split output
        split_filename = f"{file_id}_split.{output_format}"
        split_path = os.path.join(app.config['OUTPUT_FOLDER'], split_filename)
        
        if output_format == 'json':
            split_content = json.dumps({
                'chunks': chunks,
                'chunk_count': len(chunks),
                'splitter_params': splitter_params
            }, indent=2, ensure_ascii=False)
        else:  # markdown
            split_content = f"# Split Document\n\n**Chunk Count:** {len(chunks)}\n\n**Splitter Parameters:** {json.dumps(splitter_params, indent=2)}\n\n---\n\n"
            for i, chunk in enumerate(chunks, 1):
                split_content += f"## Chunk {i}\n\n{chunk}\n\n---\n\n"
        
        with open(split_path, 'w', encoding='utf-8') as f:
            f.write(split_content)
        
        return jsonify({
            'file_id': file_id,
            'chunk_count': len(chunks),
            'splitter_params': splitter_params,
            'preview': chunks[:3] if len(chunks) > 3 else chunks,
            'message': 'Text split successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<file_id>/<file_type>')
def download_file(file_id, file_type):
    try:
        if file_type == 'original':
            # Find original converted file
            for ext in ['md', 'json']:
                filename = f"{file_id}.{ext}"
                filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
                if os.path.exists(filepath):
                    return send_file(filepath, as_attachment=True, download_name=filename)
        
        elif file_type == 'split':
            # Find split file
            for ext in ['md', 'json']:
                filename = f"{file_id}_split.{ext}"
                filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
                if os.path.exists(filepath):
                    return send_file(filepath, as_attachment=True, download_name=filename)
        
        return jsonify({'error': 'File not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Document converter API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
