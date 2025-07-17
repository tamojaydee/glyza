// Pancake Cinema Workflows - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize task interactions
    initializeTaskInteractions();
    
    // Initialize theme customizations
    initializeThemeFeatures();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize animations and visual effects
 */
function initializeAnimations() {
    // Add floating animation to pancake icons
    const pancakeIcons = document.querySelectorAll('img[alt*="Pancake"], img[src*="pancake"]');
    pancakeIcons.forEach(icon => {
        icon.classList.add('floating-pancake');
    });
    
    // Add entrance animations to cards
    const cards = document.querySelectorAll('.cinema-card, .task-card, .stats-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize form validations and enhancements
 */
function initializeFormValidations() {
    // Enhanced password validation
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            validatePasswordStrength(this);
        });
    });
    
    // Real-time form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showFormErrors(this);
            }
        });
    });
    
    // Auto-save for textarea inputs (draft functionality)
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const saveKey = `draft_${textarea.name}_${Date.now()}`;
        
        // Load saved draft
        const savedDraft = localStorage.getItem(saveKey);
        if (savedDraft && !textarea.value) {
            textarea.value = savedDraft;
            showDraftNotification(textarea);
        }
        
        // Save draft on input
        textarea.addEventListener('input', debounce(function() {
            localStorage.setItem(saveKey, this.value);
        }, 1000));
        
        // Clear draft on successful form submission
        textarea.closest('form').addEventListener('submit', function() {
            localStorage.removeItem(saveKey);
        });
    });
}

/**
 * Initialize task-specific interactions
 */
function initializeTaskInteractions() {
    // Quick status change
    const statusBadges = document.querySelectorAll('.task-status-badge');
    statusBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            const taskCard = this.closest('.task-card');
            const taskId = getTaskIdFromCard(taskCard);
            if (taskId) {
                showQuickStatusModal(taskId);
            }
        });
    });
    
    // Task completion celebration
    const taskForms = document.querySelectorAll('form[action*="update_task"]');
    taskForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const statusSelect = this.querySelector('select[name="status"]');
            if (statusSelect && statusSelect.value === 'done') {
                showCompletionCelebration();
            }
        });
    });
    
    // Drag and drop for task reordering (visual only)
    initializeDragAndDrop();
}

/**
 * Initialize theme-specific features
 */
function initializeThemeFeatures() {
    // Cinema-style loading animation
    addCinemaLoader();
    
    // Pancake emoji reactions for completed tasks
    addEmojiReactions();
    
    // Dynamic background particles
    addBackgroundEffects();
    
    // Keyboard shortcuts
    initializeKeyboardShortcuts();
}

/**
 * Validate password strength
 */
function validatePasswordStrength(input) {
    const password = input.value;
    const strengthIndicator = getOrCreateStrengthIndicator(input);
    
    let strength = 0;
    let feedback = [];
    
    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');
    
    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('One uppercase letter');
    
    if (/[a-z]/.test(password)) strength++;
    else feedback.push('One lowercase letter');
    
    if (/\d/.test(password)) strength++;
    else feedback.push('One number');
    
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++;
    else feedback.push('One special character');
    
    updateStrengthIndicator(strengthIndicator, strength, feedback);
}

/**
 * Get or create password strength indicator
 */
function getOrCreateStrengthIndicator(input) {
    let indicator = input.parentNode.querySelector('.password-strength');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'password-strength mt-2';
        input.parentNode.appendChild(indicator);
    }
    return indicator;
}

/**
 * Update password strength indicator
 */
function updateStrengthIndicator(indicator, strength, feedback) {
    const levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['#e74c3c', '#e67e22', '#f39c12', '#27ae60', '#2ecc71'];
    
    const level = Math.min(strength, 4);
    const percentage = (strength / 5) * 100;
    
    indicator.innerHTML = `
        <div class="progress" style="height: 5px;">
            <div class="progress-bar" style="width: ${percentage}%; background-color: ${colors[level]}"></div>
        </div>
        <small class="text-muted">
            Strength: <span style="color: ${colors[level]}">${levels[level]}</span>
            ${feedback.length > 0 ? `<br>Need: ${feedback.join(', ')}` : ''}
        </small>
    `;
}

/**
 * Validate entire form
 */
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

/**
 * Show form validation errors
 */
function showFormErrors(form) {
    const firstInvalidInput = form.querySelector('.is-invalid');
    if (firstInvalidInput) {
        firstInvalidInput.focus();
        showToast('Please fill in all required fields', 'error');
    }
}

/**
 * Show draft notification
 */
function showDraftNotification(textarea) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show mt-2';
    notification.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>
        Draft restored! Your previous content has been recovered.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    textarea.parentNode.appendChild(notification);
}

/**
 * Get task ID from task card
 */
function getTaskIdFromCard(card) {
    const editButton = card.querySelector('[data-bs-target*="editTask"]');
    if (editButton) {
        const target = editButton.getAttribute('data-bs-target');
        const match = target.match(/editTask(\d+)/);
        return match ? match[1] : null;
    }
    return null;
}

/**
 * Show quick status change modal
 */
function showQuickStatusModal(taskId) {
    // This would implement a quick status change modal
    console.log(`Quick status change for task ${taskId}`);
}

/**
 * Show completion celebration
 */
function showCompletionCelebration() {
    // Create celebratory animation
    const celebration = document.createElement('div');
    celebration.className = 'completion-celebration';
    celebration.innerHTML = '🎉 🥞 🎬';
    celebration.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        z-index: 9999;
        animation: celebrate 2s ease-out forwards;
    `;
    
    document.body.appendChild(celebration);
    
    setTimeout(() => {
        celebration.remove();
    }, 2000);
}

/**
 * Initialize drag and drop functionality
 */
function initializeDragAndDrop() {
    const taskCards = document.querySelectorAll('.task-card');
    
    taskCards.forEach(card => {
        card.draggable = true;
        
        card.addEventListener('dragstart', function(e) {
            this.style.opacity = '0.5';
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', this.outerHTML);
        });
        
        card.addEventListener('dragend', function() {
            this.style.opacity = '1';
        });
        
        card.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });
        
        card.addEventListener('drop', function(e) {
            e.preventDefault();
            // Visual feedback only - would need backend implementation for persistence
            showToast('Drag and drop reordering is visual only', 'info');
        });
    });
}

/**
 * Add cinema-style loading animation
 */
function addCinemaLoader() {
    // Add loading states to forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalContent = this.innerHTML;
            this.innerHTML = '<i class="fas fa-film fa-spin me-2"></i>Loading...';
            this.disabled = true;
            
            // Re-enable after form submission attempt
            setTimeout(() => {
                this.innerHTML = originalContent;
                this.disabled = false;
            }, 2000);
        });
    });
}

/**
 * Add emoji reactions for completed tasks
 */
function addEmojiReactions() {
    const doneCards = document.querySelectorAll('.task-card.status-done');
    doneCards.forEach(card => {
        if (!card.querySelector('.completion-emoji')) {
            const emoji = document.createElement('span');
            emoji.className = 'completion-emoji';
            emoji.innerHTML = '🎬🥞';
            emoji.style.cssText = 'position: absolute; top: 10px; right: 10px; font-size: 1.2rem;';
            card.style.position = 'relative';
            card.appendChild(emoji);
        }
    });
}

/**
 * Add subtle background effects
 */
function addBackgroundEffects() {
    // Create floating pancake particles
    const particleContainer = document.createElement('div');
    particleContainer.className = 'background-particles';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    
    for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.innerHTML = '🥞';
        particle.style.cssText = `
            position: absolute;
            font-size: 2rem;
            opacity: 0.1;
            animation: float-particle ${15 + Math.random() * 10}s infinite linear;
            left: ${Math.random() * 100}%;
            animation-delay: ${Math.random() * 15}s;
        `;
        particleContainer.appendChild(particle);
    }
    
    document.body.appendChild(particleContainer);
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + / to show shortcuts help
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            showKeyboardShortcuts();
        }
        
        // Ctrl/Cmd + N to add new task
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            const addTaskButton = document.querySelector('[data-bs-target="#addTaskForm"]');
            if (addTaskButton) {
                addTaskButton.click();
            }
        }
    });
}

/**
 * Show keyboard shortcuts modal
 */
function showKeyboardShortcuts() {
    showToast('Keyboard Shortcuts: Ctrl+N (New Task), Ctrl+/ (This Help)', 'info');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Debounce utility function
 */
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

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes celebrate {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }
        50% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.2);
        }
        100% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(1) translateY(-50px);
        }
    }
    
    @keyframes float-particle {
        from {
            transform: translateY(100vh) rotate(0deg);
        }
        to {
            transform: translateY(-100px) rotate(360deg);
        }
    }
    
    .fade-in-up {
        animation: fade-in-up 0.6s ease-out forwards;
    }
    
    .completion-emoji {
        animation: bounce 1s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
`;
document.head.appendChild(style);
