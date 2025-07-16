// Main JavaScript for MathGenius Uganda

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeNavigation();
    initializeTopicTabs();
    initializeTestimonialSlider();
    initializeScrollAnimations();
    initializeMobileMenu();
    initializeProgressTracking();
    initializeAnimations();
    
    // Load user progress if available
    loadUserProgress();
});

// Navigation functionality
function initializeNavigation() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Smooth scrolling for anchor links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    const offsetTop = target.offsetTop - 70; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Topic tabs functionality
function initializeTopicTabs() {
    const topicTabs = document.querySelectorAll('.topic-tab');
    const topicContents = document.querySelectorAll('.topic-content');
    
    topicTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            
            // Remove active class from all tabs and contents
            topicTabs.forEach(t => t.classList.remove('active'));
            topicContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(target).classList.add('active');
            
            // Animate the content change
            const activeContent = document.getElementById(target);
            activeContent.style.opacity = '0';
            activeContent.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                activeContent.style.opacity = '1';
                activeContent.style.transform = 'translateY(0)';
                activeContent.style.transition = 'all 0.3s ease';
            }, 100);
        });
    });
}

// Testimonial slider functionality
function initializeTestimonialSlider() {
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    const testimonialDots = document.querySelectorAll('.testimonial-dot');
    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds
    
    // Show specific slide
    function showSlide(index) {
        testimonialCards.forEach((card, i) => {
            card.classList.toggle('active', i === index);
        });
        
        testimonialDots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    
    // Next slide
    function nextSlide() {
        currentSlide = (currentSlide + 1) % testimonialCards.length;
        showSlide(currentSlide);
    }
    
    // Add click events to dots
    testimonialDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
        });
    });
    
    // Auto-advance slides
    setInterval(nextSlide, slideInterval);
}

// Scroll animations
function initializeScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-aos]');
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animationType = element.getAttribute('data-aos');
                const delay = element.getAttribute('data-aos-delay') || 0;
                
                setTimeout(() => {
                    element.classList.add('animate-' + animationType);
                }, delay);
                
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => observer.observe(el));
    
    // Add fade-in animation to elements as they come into view
    const fadeElements = document.querySelectorAll('.feature-card, .topic-card, .practice-card');
    
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    fadeElements.forEach(el => fadeObserver.observe(el));
}

// Mobile menu functionality
function initializeMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.classList.toggle('nav-open');
        });
        
        // Close menu when clicking on nav links
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('nav-open');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!hamburger.contains(event.target) && !navMenu.contains(event.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('nav-open');
            }
        });
    }
}

// Progress tracking functionality
function initializeProgressTracking() {
    // Simulate progress for demo purposes
    const progressBars = document.querySelectorAll('.progress-fill');
    
    // Load saved progress or use random values for demo
    progressBars.forEach((bar, index) => {
        const savedProgress = localStorage.getItem(`progress-${index}`) || Math.floor(Math.random() * 100);
        updateProgressBar(bar, savedProgress);
    });
}

function updateProgressBar(progressBar, percentage) {
    progressBar.style.width = percentage + '%';
    
    // Update the corresponding text
    const topicCard = progressBar.closest('.topic-card');
    if (topicCard) {
        const progressText = topicCard.querySelector('.topic-progress span');
        if (progressText) {
            const totalQuestions = progressText.textContent.split('/')[1].split(' ')[0];
            const answeredQuestions = Math.floor((percentage / 100) * parseInt(totalQuestions));
            progressText.textContent = `${answeredQuestions}/${totalQuestions} questions`;
        }
    }
}

// Animation helpers
function initializeAnimations() {
    // Floating math symbols animation
    const floatingElements = document.querySelectorAll('.floating-element');
    
    floatingElements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.5}s`;
        element.classList.add('animate-math-float');
    });
    
    // Hero stats counter animation
    animateCounters();
    
    // Parallax effect for hero section
    initializeParallax();
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/\D/g, ''));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = counter.textContent.replace(/\d+/, target);
                clearInterval(timer);
            } else {
                counter.textContent = counter.textContent.replace(/\d+/, Math.floor(current));
            }
        }, 20);
    });
}

function initializeParallax() {
    const heroVisual = document.querySelector('.hero-visual');
    
    if (heroVisual) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroVisual.style.transform = `translateY(${rate}px)`;
        });
    }
}

// User progress management
function loadUserProgress() {
    const userId = localStorage.getItem('userId') || 'demo-user';
    const progress = JSON.parse(localStorage.getItem(`progress-${userId}`)) || {};
    
    // Apply progress to UI elements
    Object.keys(progress).forEach(topicId => {
        const progressBar = document.querySelector(`[data-topic="${topicId}"] .progress-fill`);
        if (progressBar) {
            updateProgressBar(progressBar, progress[topicId]);
        }
    });
}

function saveUserProgress(topicId, percentage) {
    const userId = localStorage.getItem('userId') || 'demo-user';
    const progress = JSON.parse(localStorage.getItem(`progress-${userId}`)) || {};
    
    progress[topicId] = percentage;
    localStorage.setItem(`progress-${userId}`, JSON.stringify(progress));
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

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

// Performance optimization
function optimizePerformance() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Preconnect to external resources
    const preconnectLinks = [
        'https://fonts.googleapis.com',
        'https://cdnjs.cloudflare.com'
    ];
    
    preconnectLinks.forEach(url => {
        const link = document.createElement('link');
        link.rel = 'preconnect';
        link.href = url;
        document.head.appendChild(link);
    });
}

// Initialize performance optimizations
optimizePerformance();

// Math-specific utilities
const MathUtils = {
    // Generate random number within range
    randomInt: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
    
    // Format number with commas
    formatNumber: (num) => num.toLocaleString(),
    
    // Calculate percentage
    calculatePercentage: (part, total) => Math.round((part / total) * 100),
    
    // Shuffle array
    shuffleArray: (array) => {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    },
    
    // Generate math problem
    generateProblem: (type, difficulty = 'easy') => {
        const problems = {
            addition: () => {
                const a = MathUtils.randomInt(1, difficulty === 'easy' ? 100 : 1000);
                const b = MathUtils.randomInt(1, difficulty === 'easy' ? 100 : 1000);
                return {
                    question: `${a} + ${b} = ?`,
                    answer: a + b,
                    type: 'addition'
                };
            },
            subtraction: () => {
                const a = MathUtils.randomInt(10, difficulty === 'easy' ? 100 : 1000);
                const b = MathUtils.randomInt(1, a);
                return {
                    question: `${a} - ${b} = ?`,
                    answer: a - b,
                    type: 'subtraction'
                };
            },
            multiplication: () => {
                const a = MathUtils.randomInt(1, difficulty === 'easy' ? 12 : 25);
                const b = MathUtils.randomInt(1, difficulty === 'easy' ? 12 : 25);
                return {
                    question: `${a} × ${b} = ?`,
                    answer: a * b,
                    type: 'multiplication'
                };
            },
            division: () => {
                const answer = MathUtils.randomInt(1, difficulty === 'easy' ? 12 : 25);
                const divisor = MathUtils.randomInt(2, difficulty === 'easy' ? 12 : 25);
                const dividend = answer * divisor;
                return {
                    question: `${dividend} ÷ ${divisor} = ?`,
                    answer: answer,
                    type: 'division'
                };
            }
        };
        
        return problems[type] ? problems[type]() : problems.addition();
    }
};

// Export utilities for use in other files
window.MathGenius = {
    MathUtils,
    showNotification,
    updateProgressBar,
    saveUserProgress,
    loadUserProgress
};

// Service Worker registration for offline functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden, pause animations
        document.body.classList.add('page-hidden');
    } else {
        // Page is visible, resume animations
        document.body.classList.remove('page-hidden');
    }
});

// Add CSS for mobile menu (since it needs JavaScript state)
const mobileMenuCSS = `
    @media (max-width: 768px) {
        .nav-menu {
            position: fixed;
            top: 70px;
            left: -100%;
            width: 100%;
            height: calc(100vh - 70px);
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            padding-top: 2rem;
            transition: all 0.3s ease;
            z-index: 999;
        }
        
        .nav-menu.active {
            left: 0;
        }
        
        .hamburger.active span:nth-child(1) {
            transform: rotate(-45deg) translate(-5px, 6px);
        }
        
        .hamburger.active span:nth-child(2) {
            opacity: 0;
        }
        
        .hamburger.active span:nth-child(3) {
            transform: rotate(45deg) translate(-5px, -6px);
        }
        
        .nav-open {
            overflow: hidden;
        }
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        z-index: 10000;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .notification-success .notification-content i {
        color: #10b981;
    }
    
    .notification-error .notification-content i {
        color: #ef4444;
    }
    
    .notification-info .notification-content i {
        color: #3b82f6;
    }
    
    .page-hidden * {
        animation-play-state: paused !important;
    }
`;

// Inject the CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = mobileMenuCSS;
document.head.appendChild(styleSheet);