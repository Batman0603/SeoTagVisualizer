// SEO Meta Tag Analyzer JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize example URL buttons
    initializeExampleUrls();
    
    // Initialize loading states
    initializeLoadingStates();
    
    // Initialize theme toggle
    initializeThemeToggle();
    
    // Initialize animations
    initializeAnimations();
    
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
                
                // Enhanced animation with ripple effect
                const originalText = button.textContent;
                button.style.transform = 'scale(0.95)';
                button.classList.add('btn-primary');
                button.classList.remove('btn-outline-primary');
                
                setTimeout(function() {
                    button.style.transform = 'scale(1)';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-outline-primary');
                }, 150);
                
                // Show feedback
                showToast('URL loaded: ' + button.textContent, 'success');
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
                const spinner = submitButton.querySelector('.spinner-border');
                if (spinner) {
                    spinner.classList.remove('d-none');
                    submitButton.classList.add('loading');
                    submitButton.disabled = true;
                }
                
                // Set timeout to re-enable button in case of errors
                setTimeout(function() {
                    if (spinner) {
                        spinner.classList.add('d-none');
                        submitButton.classList.remove('loading');
                        submitButton.disabled = false;
                    }
                }, 30000); // 30 seconds timeout
            }
        });
    });
}

/**
 * Initialize and manage theme switching
 */
function initializeTheme() {
    // Check for saved theme preference or default to 'dark'
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const htmlElement = document.documentElement;
    
    // Apply the theme
    htmlElement.setAttribute('data-bs-theme', savedTheme);
    
    // Update toggle button appearance
    updateThemeToggleButton(savedTheme);
}

/**
 * Initialize theme toggle functionality
 */
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const htmlElement = document.documentElement;
            const currentTheme = htmlElement.getAttribute('data-bs-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Apply new theme
            htmlElement.setAttribute('data-bs-theme', newTheme);
            
            // Save preference
            localStorage.setItem('theme', newTheme);
            
            // Update button appearance
            updateThemeToggleButton(newTheme);
            
            // Add transition effect
            document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
            setTimeout(() => {
                document.body.style.transition = '';
            }, 300);
        });
    }
}

/**
 * Update theme toggle button appearance
 */
function updateThemeToggleButton(theme) {
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (themeIcon && themeText) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
            themeText.textContent = 'Light Mode';
        } else {
            themeIcon.className = 'fas fa-moon';
            themeText.textContent = 'Dark Mode';
        }
    }
}

/**
 * Initialize animations and enhanced interactions
 */
function initializeAnimations() {
    // Add fade-in animation to cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards and feature elements
    const animatedElements = document.querySelectorAll('.card, .feature-card, .hero-section');
    animatedElements.forEach(function(element) {
        observer.observe(element);
    });
    
    // Enhanced button interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(button) {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
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
 * Show enhanced toast notification
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
    
    // Icon mapping for different toast types
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    // Create toast element with enhanced styling
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 fade-in" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center">
                    <i class="${icons[type] || icons.info} me-2"></i>
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
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: type === 'error' ? 5000 : 3000 // Error messages stay longer
        });
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

// Enhanced keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K to focus on URL input
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const urlInput = document.getElementById('url');
        if (urlInput) {
            urlInput.focus();
            urlInput.select();
            showToast('Ready to analyze! Paste your URL here.', 'info');
        }
    }
    
    // Ctrl/Cmd + T to toggle theme
    if ((event.ctrlKey || event.metaKey) && event.key === 't') {
        event.preventDefault();
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.click();
        }
    }
    
    // Escape to clear URL input
    if (event.key === 'Escape') {
        const urlInput = document.getElementById('url');
        if (urlInput && document.activeElement === urlInput) {
            urlInput.value = '';
            urlInput.blur();
            showToast('Input cleared', 'info');
        }
    }
    
    // Enter to submit form when URL input is focused
    if (event.key === 'Enter') {
        const urlInput = document.getElementById('url');
        if (urlInput && document.activeElement === urlInput && urlInput.value.trim()) {
            const form = urlInput.closest('form');
            if (form) {
                form.requestSubmit();
            }
        }
    }
});

// Add enhanced scroll effects
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('shadow-lg');
            navbar.style.backgroundColor = 'rgba(13, 110, 253, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.classList.remove('shadow-lg');
            navbar.style.backgroundColor = '';
            navbar.style.backdropFilter = '';
        }
    }
});

// Add performance optimization for smooth animations
document.addEventListener('DOMContentLoaded', function() {
    // Preload critical CSS variables
    const computedStyle = getComputedStyle(document.documentElement);
    const primaryColor = computedStyle.getPropertyValue('--primary-color');
    
    // Add will-change property for animated elements
    const animatedElements = document.querySelectorAll('.card, .btn, .form-card');
    animatedElements.forEach(function(element) {
        element.style.willChange = 'transform, box-shadow';
    });
});
