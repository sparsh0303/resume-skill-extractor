import os
import re
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file_path(upload_folder, filename):
    """Generate a secure file path for uploaded files"""
    filename = secure_filename(filename)
    return os.path.join(upload_folder, filename)

def extract_email(text):
    """Extract email from text using regex"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    """Extract phone number from text using regex"""
    phone_pattern = r'\b(?:\+?\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None

def clean_text(text):
    """Clean extracted text by removing extra whitespace"""
    return ' '.join(text.split())

def is_valid_skill(skill):
    """Basic validation for skill filtering"""
    return bool(skill and len(skill) >= 2 and len(skill) <= 50)
