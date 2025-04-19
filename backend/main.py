import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import db, Resume
from extractor import extract_resume_data
from utils import allowed_file, secure_file_path, is_valid_skill

app = Flask(__name__, static_folder='frontend')
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database
db.init_app(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = secure_file_path(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract data from PDF
        resume_data = extract_resume_data(file_path)
        if not resume_data:
            return jsonify({'error': 'Failed to extract data from PDF'}), 400
        
        # Save to database
        resume = Resume(
            filename=filename,
            **resume_data
        )
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'resume': resume.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    try:
        resumes = Resume.query.order_by(Resume.uploaded_at.desc()).all()
        return jsonify({
            'resumes': [resume.to_dict() for resume in resumes]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/filter', methods=['GET'])
def filter_resumes():
    skill = request.args.get('skill', '').lower()
    
    if not is_valid_skill(skill):
        return jsonify({'error': 'Invalid skill parameter'}), 400
    
    try:
        # Filter resumes where the skills column contains the specified skill
        resumes = Resume.query.filter(Resume.skills.like(f'%{skill}%')).all()
        return jsonify({
            'resumes': [resume.to_dict() for resume in resumes]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
