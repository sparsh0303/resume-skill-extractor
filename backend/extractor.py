import pdfplumber
from utils import extract_email, extract_phone, clean_text

COMMON_SKILLS = {
    'python', 'java', 'javascript', 'c++', 'sql', 'react', 'node.js', 'docker',
    'kubernetes', 'aws', 'azure', 'git', 'agile', 'scrum', 'machine learning',
    'data analysis', 'html', 'css', 'angular', 'vue.js', 'mongodb', 'postgresql'
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""
    return text

def extract_name(text):
    """
    Basic name extraction - assumes name is in the first few lines
    In a production environment, you'd want to use NER (Named Entity Recognition)
    """
    lines = text.split('\n')
    for line in lines[:3]:  # Check first 3 lines
        # Remove common resume header words
        line = line.lower().replace('resume', '').replace('cv', '').strip()
        if line and len(line.split()) <= 4:  # Most names are 1-4 words
            return line.title()
    return None

def extract_skills(text):
    """Extract skills from text by matching against COMMON_SKILLS"""
    skills = []
    text_lower = text.lower()
    
    for skill in COMMON_SKILLS:
        if skill in text_lower:
            skills.append(skill)
    
    return list(set(skills))  # Remove duplicates

def extract_experience(text):
    """
    Basic experience extraction - looks for sections that might contain work experience
    In a production environment, you'd want to use more sophisticated NLP techniques
    """
    text_lower = text.lower()
    experience_section = ""
    
    # Common section headers for experience
    headers = ['experience', 'work experience', 'employment history', 'work history']
    
    for header in headers:
        if header in text_lower:
            # Find the section after the header
            start_idx = text_lower.find(header)
            next_section = float('inf')
            
            # Look for the next section header (education, skills, etc.)
            for next_header in ['education', 'skills', 'projects', 'certifications']:
                idx = text_lower.find(next_header, start_idx + len(header))
                if idx != -1 and idx < next_section:
                    next_section = idx
            
            if next_section != float('inf'):
                experience_section = text[start_idx:next_section].strip()
            else:
                experience_section = text[start_idx:].strip()
            
            break
    
    return clean_text(experience_section) if experience_section else None

def extract_resume_data(file_path):
    """Main function to extract all resume data"""
    text = extract_text_from_pdf(file_path)
    if not text:
        return None
        
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': ','.join(extract_skills(text)),
        'experience': extract_experience(text)
    }
