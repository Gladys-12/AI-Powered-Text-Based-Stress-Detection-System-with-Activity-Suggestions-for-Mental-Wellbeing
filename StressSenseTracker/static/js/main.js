// Main JavaScript file for StressSense application

// Global utility functions
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'primary'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Form validation utilities
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateUsername(username) {
    return username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
}

// Text processing utilities
function getTextStats(text) {
    const words = text.trim().split(/\s+/).filter(word => word.length > 0);
    return {
        characters: text.length,
        words: words.length,
        sentences: text.split(/[.!?]+/).filter(s => s.trim().length > 0).length
    };
}

// Emotion-related utilities
function getEmotionIcon(emotion) {
    const icons = {
        'happy': 'fas fa-smile-beam',
        'sad': 'fas fa-sad-tear',
        'angry': 'fas fa-angry',
        'anxious': 'fas fa-meh-blank',
        'stressed': 'fas fa-tired',
        'neutral': 'fas fa-meh'
    };
    return icons[emotion] || icons['neutral'];
}

function getEmotionColor(emotion) {
    const colors = {
        'happy': '#7CB342',
        'sad': '#1E88E5',
        'angry': '#E53935',
        'anxious': '#FB8C00',
        'stressed': '#8E24AA',
        'neutral': '#607D8B'
    };
    return colors[emotion] || colors['neutral'];
}

// Animation utilities
function fadeInElements(selector, delay = 100) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * delay);
    });
}

// Local storage utilities
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

function getFromLocalStorage(key, defaultValue = null) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : defaultValue;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return defaultValue;
    }
}

// Theme utilities
function initializeTheme() {
    const savedTheme = getFromLocalStorage('theme', 'light');
    document.body.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.body.setAttribute('data-theme', newTheme);
    saveToLocalStorage('theme', newTheme);
    
    showToast(`Switched to ${newTheme} theme`, 'success');
}

// Form enhancement utilities
function enhanceForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;
    
    // Add real-time validation
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearFieldError(this);
        });
    });
    
    // Enhanced form submission
    form.addEventListener('submit', function(e) {
        if (!validateForm(form)) {
            e.preventDefault();
        }
    });
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const name = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Specific field validations
    if (value && type === 'email' && !validateEmail(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
    }
    
    if (value && name === 'password' && !validatePassword(value)) {
        isValid = false;
        errorMessage = 'Password must be at least 6 characters long';
    }
    
    if (value && name === 'username' && !validateUsername(value)) {
        isValid = false;
        errorMessage = 'Username must be at least 3 characters and contain only letters, numbers, and underscores';
    }
    
    // Show/hide error
    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function validateForm(form) {
    const fields = form.querySelectorAll('input, textarea');
    let isValid = true;
    
    fields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Character counter utility
function initializeCharacterCounter(textareaSelector, countSelector, maxLength = null) {
    const textarea = document.querySelector(textareaSelector);
    const counter = document.querySelector(countSelector);
    
    if (!textarea || !counter) return;
    
    function updateCounter() {
        const length = textarea.value.length;
        counter.textContent = length;
        
        if (maxLength) {
            counter.textContent += ` / ${maxLength}`;
            
            if (length > maxLength) {
                counter.classList.add('text-danger');
                counter.classList.remove('text-success');
            } else if (length > maxLength * 0.8) {
                counter.classList.add('text-warning');
                counter.classList.remove('text-success', 'text-danger');
            } else {
                counter.classList.add('text-success');
                counter.classList.remove('text-warning', 'text-danger');
            }
        }
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter(); // Initialize
}

// Auto-resize textarea utility
function initializeAutoResize(textareaSelector) {
    const textarea = document.querySelector(textareaSelector);
    if (!textarea) return;
    
    function resize() {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }
    
    textarea.addEventListener('input', resize);
    resize(); // Initialize
}

// Smooth scroll utility
function smoothScrollTo(element, offset = 0) {
    const elementPosition = element.offsetTop - offset;
    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });
}

// Loading state management
function setLoadingState(element, isLoading, originalText = null) {
    if (isLoading) {
        element.dataset.originalText = originalText || element.textContent;
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        element.disabled = true;
    } else {
        element.innerHTML = element.dataset.originalText || originalText;
        element.disabled = false;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Enhance forms
    enhanceForm('form');
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                smoothScrollTo(target, 100);
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add fade-in animation to cards
    fadeInElements('.card, .auth-card, .tip-card, .activity-item', 150);
    
    // Initialize auto-resize for textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        initializeAutoResize(`#${textarea.id}`);
    });
    
    console.log('StressSense app initialized successfully!');
});

// Error handling
window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    showToast('An unexpected error occurred. Please try again.', 'error');
});

// Handle network errors
window.addEventListener('offline', function() {
    showToast('You are currently offline. Some features may not work.', 'warning');
});

window.addEventListener('online', function() {
    showToast('Connection restored!', 'success');
});

// Export utilities for use in other scripts
window.StressSenseUtils = {
    showToast,
    validateEmail,
    validatePassword,
    validateUsername,
    getTextStats,
    getEmotionIcon,
    getEmotionColor,
    fadeInElements,
    saveToLocalStorage,
    getFromLocalStorage,
    toggleTheme,
    setLoadingState,
    smoothScrollTo
};
