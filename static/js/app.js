// SEO Meta Tag Analyzer JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize example URL buttons
    initializeExampleUrls();
    
    // Initialize loading states
    initializeLoadingStates();
    
    // Initialize tooltips if Bootstrap tooltips are available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const urlInput = form.querySelector('input[name="url"]');
            const url = urlInput.value.trim();
            
            // Add protocol if missing
            if (url && !url.match(/^https?:\/\//)) {
                urlInput.value = 'https://' + url;
            }
            
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Initialize example URL buttons
 */
function initializeExampleUrls() {
    const exampleButtons = document.querySelectorAll('.example-url');
    const urlInput = document.getElementById('url');
    
    exampleButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (urlInput) {
                urlInput.value = url;
                urlInput.focus();
                
                // Remove any validation classes
                const form = urlInput.closest('form');
                if (form) {
                    form.classList.remove('was-validated');
                }
                urlInput.classList.remove('is-invalid', 'is-valid');
                
                // Add a subtle animation
                button.classList.add('btn-primary');
                setTimeout(function() {
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-outline-secondary');
                }, 200);
            }
        });
    });
}

/**
 * Initialize loading states for forms
 */
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;
                
                // Set timeout to re-enable button in case of errors
                setTimeout(function() {
                    submitButton.classList.remove('loading');
                    submitButton.disabled = false;
                }, 30000); // 30 seconds timeout
            }
        });
    });
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        }).catch(function(err) {
            console.error('Failed to copy to clipboard:', err);
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

/**
 * Fallback copy to clipboard for older browsers
 */
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('Copied to clipboard!', 'success');
        } else {
            showToast('Failed to copy to clipboard', 'error');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showToast('Copy not supported in this browser', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }
}

/**
 * Smooth scroll to element
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Format URL for display
 */
function formatUrl(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.hostname + urlObj.pathname;
    } catch (e) {
        return url;
    }
}

/**
 * Validate URL format
 */
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

/**
 * Get domain from URL
 */
function getDomain(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.hostname;
    } catch (e) {
        return '';
    }
}

/**
 * Truncate text with ellipsis
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength - 3) + '...';
}

/**
 * Handle image load errors in previews
 */
document.addEventListener('error', function(event) {
    if (event.target.tagName === 'IMG' && event.target.closest('.social-preview')) {
        // Hide the image container if image fails to load
        const imageContainer = event.target.closest('.social-image');
        if (imageContainer) {
            imageContainer.style.display = 'none';
        }
    }
}, true);

/**
 * Add copy functionality to meta data tables
 */
document.addEventListener('click', function(event) {
    if (event.target.closest('td') && event.target.closest('.table')) {
        const cell = event.target.closest('td');
        const text = cell.textContent.trim();
        
        if (text && text !== 'Not found' && event.ctrlKey) {
            copyToClipboard(text);
        }
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K to focus on URL input
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const urlInput = document.getElementById('url');
        if (urlInput) {
            urlInput.focus();
            urlInput.select();
        }
    }
    
    // Escape to clear URL input
    if (event.key === 'Escape') {
        const urlInput = document.getElementById('url');
        if (urlInput && document.activeElement === urlInput) {
            urlInput.value = '';
            urlInput.blur();
        }
    }
});
