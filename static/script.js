/**
 * Healthcare Symptom Checker - Frontend JavaScript
 * Handles form submission, API calls, and UI updates
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const symptomForm = document.getElementById('symptomForm');
const symptomsTextarea = document.getElementById('symptoms');
const charCount = document.getElementById('charCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingContainer = document.getElementById('loadingContainer');
const resultsSection = document.getElementById('resultsSection');
const errorContainer = document.getElementById('errorContainer');
const analysisResults = document.getElementById('analysisResults');
const disclaimerText = document.getElementById('disclaimerText');
const emergencyAlert = document.getElementById('emergencyAlert');
const modelName = document.getElementById('modelName');
const tokensUsed = document.getElementById('tokensUsed');
const errorMessage = document.getElementById('errorMessage');
const newCheckBtn = document.getElementById('newCheckBtn');
const retryBtn = document.getElementById('retryBtn');

// State
let currentSymptoms = '';

// ===== Event Listeners =====

// Character counter
symptomsTextarea.addEventListener('input', (e) => {
    const length = e.target.value.length;
    charCount.textContent = length;
    
    // Visual feedback when approaching limit
    if (length > 900) {
        charCount.style.color = 'var(--danger-color)';
    } else if (length > 700) {
        charCount.style.color = 'var(--warning-color)';
    } else {
        charCount.style.color = 'var(--text-muted)';
    }
});

// Form submission
symptomForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const symptoms = symptomsTextarea.value.trim();
    
    // Validation
    if (!symptoms) {
        showError('Please describe your symptoms.');
        return;
    }
    
    if (symptoms.length < 10) {
        showError('Please provide a more detailed description (at least 10 characters).');
        return;
    }
    
    currentSymptoms = symptoms;
    await analyzeSymptoms(symptoms);
});

// New check button
newCheckBtn.addEventListener('click', () => {
    resetForm();
    symptomsTextarea.focus();
});

// Retry button
retryBtn.addEventListener('click', () => {
    if (currentSymptoms) {
        analyzeSymptoms(currentSymptoms);
    } else {
        hideError();
        symptomsTextarea.focus();
    }
});

// ===== Core Functions =====

/**
 * Analyze symptoms by calling the backend API
 */
async function analyzeSymptoms(symptoms) {
    try {
        // Show loading state
        showLoading();
        
        // Call API
        const response = await fetch(`${API_BASE_URL}/check-symptoms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symptoms }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze symptoms');
        }
        
        if (!data.success) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        // Show results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while analyzing your symptoms. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Display analysis results
 */
function displayResults(data) {
    // Hide other sections
    errorContainer.style.display = 'none';
    
    // Check for emergency keywords in the analysis
    const emergencyKeywords = ['emergency', 'immediately', '911', 'urgent care', 'hospital', 'serious'];
    const hasEmergency = emergencyKeywords.some(keyword => 
        data.analysis.toLowerCase().includes(keyword)
    );
    
    // Show/hide emergency alert
    if (hasEmergency) {
        emergencyAlert.style.display = 'flex';
    } else {
        emergencyAlert.style.display = 'none';
    }
    
    // Format and display analysis
    analysisResults.innerHTML = formatAnalysis(data.analysis);
    
    // Display disclaimer
    disclaimerText.textContent = data.disclaimer;
    
    // Display metadata
    if (data.metadata) {
        modelName.textContent = data.metadata.model || 'AI Model';
        tokensUsed.textContent = data.metadata.tokens_used || '0';
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Format analysis text for better display
 */
function formatAnalysis(text) {
    // Convert markdown-style formatting to HTML
    let formatted = text
        // Headers
        .replace(/^### (.*$)/gim, '<h4>$1</h4>')
        .replace(/^## (.*$)/gim, '<h3>$1</h3>')
        .replace(/^# (.*$)/gim, '<h2>$1</h2>')
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Lists
        .replace(/^\d+\.\s+(.*$)/gim, '<li>$1</li>')
        .replace(/^-\s+(.*$)/gim, '<li>$1</li>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    // Wrap in paragraphs if not already
    if (!formatted.startsWith('<')) {
        formatted = '<p>' + formatted + '</p>';
    }
    
    // Wrap lists
    formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    return formatted;
}

/**
 * Show loading state
 */
function showLoading() {
    loadingContainer.style.display = 'block';
    resultsSection.style.display = 'none';
    errorContainer.style.display = 'none';
    analyzeBtn.disabled = true;
    
    // Scroll to loading
    loadingContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingContainer.style.display = 'none';
    analyzeBtn.disabled = false;
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
    resultsSection.style.display = 'none';
    loadingContainer.style.display = 'none';
    
    // Scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Hide error message
 */
function hideError() {
    errorContainer.style.display = 'none';
}

/**
 * Reset form to initial state
 */
function resetForm() {
    symptomsTextarea.value = '';
    charCount.textContent = '0';
    charCount.style.color = 'var(--text-muted)';
    currentSymptoms = '';
    
    // Hide all result sections
    resultsSection.style.display = 'none';
    errorContainer.style.display = 'none';
    loadingContainer.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== Initialization =====

// Focus on textarea when page loads
document.addEventListener('DOMContentLoaded', () => {
    symptomsTextarea.focus();
});
