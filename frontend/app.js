const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadProgress = document.getElementById('uploadProgress');
const progressBar = uploadProgress.querySelector('.progress');
const skillFilter = document.getElementById('skillFilter');
const filterButton = document.getElementById('filterButton');
const resultsContainer = document.getElementById('resultsContainer');
const resumeCardTemplate = document.getElementById('resumeCardTemplate');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
filterButton.addEventListener('click', handleFilter);
skillFilter.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleFilter();
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadResumes();
});

// File Upload Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = '#2C3E50';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = '#4A90E2';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

async function handleFile(file) {
    if (!file.type.includes('pdf')) {
        alert('Please upload a PDF file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        uploadProgress.hidden = false;
        progressBar.style.width = '50%';

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        progressBar.style.width = '100%';
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const data = await response.json();
        setTimeout(() => {
            uploadProgress.hidden = true;
            progressBar.style.width = '0';
            loadResumes();
        }, 500);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to upload file');
        uploadProgress.hidden = true;
        progressBar.style.width = '0';
    }
}

// Resume Loading and Filtering
async function loadResumes(skill = '') {
    try {
        const url = skill
            ? `${API_BASE_URL}/filter?skill=${encodeURIComponent(skill)}`
            : `${API_BASE_URL}/results`;

        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch resumes');

        const data = await response.json();
        displayResumes(data.resumes);

    } catch (error) {
        console.error('Error:', error);
        resultsContainer.innerHTML = '<p class="error">Failed to load resumes</p>';
    }
}

function handleFilter() {
    const skill = skillFilter.value.trim();
    loadResumes(skill);
}

function displayResumes(resumes) {
    resultsContainer.innerHTML = '';

    if (!resumes || resumes.length === 0) {
        resultsContainer.innerHTML = '<p>No resumes found</p>';
        return;
    }

    resumes.forEach(resume => {
        const card = createResumeCard(resume);
        resultsContainer.appendChild(card);
    });
}

function createResumeCard(resume) {
    const card = resumeCardTemplate.content.cloneNode(true);
    
    // Fill in the card details
    card.querySelector('.resume-name').textContent = resume.name || 'Unnamed';
    card.querySelector('.resume-date').textContent = new Date(resume.uploaded_at).toLocaleDateString();
    
    const emailSpan = card.querySelector('.email');
    const phoneSpan = card.querySelector('.phone');
    emailSpan.textContent = resume.email || 'No email';
    phoneSpan.textContent = resume.phone || 'No phone';

    const skillsList = card.querySelector('.skills-list');
    if (resume.skills && resume.skills.length > 0) {
        resume.skills.forEach(skill => {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill;
            skillsList.appendChild(skillTag);
        });
    } else {
        skillsList.innerHTML = '<span>No skills found</span>';
    }

    card.querySelector('.experience-text').textContent = resume.experience || 'No experience listed';

    return card;
}

// Helper Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
