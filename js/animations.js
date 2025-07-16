// Advanced animations and interactive effects for MathGenius Uganda

// Animation utilities and interactive effects
class AnimationManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupIntersectionObserver();
        this.setupMathSymbolAnimations();
        this.setupParticleEffects();
        this.setupHoverAnimations();
        this.setupScrollAnimations();
    }
    
    // Intersection Observer for scroll-triggered animations
    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements with animation classes
        document.querySelectorAll('.fade-in, .slide-up, .scale-in, .bounce-in').forEach(el => {
            observer.observe(el);
        });
    }
    
    // Floating math symbols animation
    setupMathSymbolAnimations() {
        const symbols = ['π', '∑', '∆', '∫', '√', '∞', '≈', '±', '×', '÷', '=', '+', '-'];
        const heroSection = document.querySelector('.hero');
        
        if (!heroSection) return;
        
        // Create floating math symbols
        for (let i = 0; i < 15; i++) {
            const symbol = document.createElement('div');
            symbol.className = 'floating-symbol';
            symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            symbol.style.cssText = `
                position: absolute;
                font-size: ${Math.random() * 20 + 15}px;
                opacity: ${Math.random() * 0.3 + 0.1};
                color: var(--primary-color);
                pointer-events: none;
                z-index: 1;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float ${Math.random() * 10 + 15}s infinite linear;
            `;
            heroSection.appendChild(symbol);
        }
    }
    
    // Particle effects for success animations
    setupParticleEffects() {
        // Create particle container if it doesn't exist
        if (!document.getElementById('particles')) {
            const particleContainer = document.createElement('div');
            particleContainer.id = 'particles';
            particleContainer.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
            `;
            document.body.appendChild(particleContainer);
        }
    }
    
    // Enhanced hover animations
    setupHoverAnimations() {
        // Feature cards hover effect
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px) scale(1.02)';
                card.style.boxShadow = '0 20px 40px rgba(0,0,0,0.1)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
            });
        });
        
        // Topic cards interactive effects
        document.querySelectorAll('.topic-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                const icon = card.querySelector('.topic-icon');
                if (icon) {
                    icon.style.transform = 'rotate(10deg) scale(1.1)';
                }
            });
            
            card.addEventListener('mouseleave', () => {
                const icon = card.querySelector('.topic-icon');
                if (icon) {
                    icon.style.transform = 'rotate(0deg) scale(1)';
                }
            });
        });
        
        // Button hover effects
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-2px)';
            });
            
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translateY(0)';
            });
        });
    }
    
    // Scroll-triggered animations
    setupScrollAnimations() {
        // Navbar background animation
        const navbar = document.querySelector('.navbar');
        let lastScrollY = window.scrollY;
        
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
                navbar.style.backdropFilter = 'blur(10px)';
            } else {
                navbar.style.backgroundColor = 'transparent';
                navbar.style.backdropFilter = 'none';
            }
            
            // Hide/show navbar on scroll direction
            if (currentScrollY > lastScrollY && currentScrollY > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        });
        
        // Parallax effect for hero section
        const hero = document.querySelector('.hero');
        if (hero) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const parallax = scrolled * 0.5;
                hero.style.transform = `translateY(${parallax}px)`;
            });
        }
    }
    
    // Trigger success particle explosion
    triggerSuccessAnimation(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        this.createParticleExplosion(centerX, centerY, '#4CAF50');
    }
    
    // Trigger error shake animation
    triggerErrorAnimation(element) {
        element.classList.add('shake');
        setTimeout(() => {
            element.classList.remove('shake');
        }, 600);
    }
    
    // Create particle explosion effect
    createParticleExplosion(x, y, color = '#FFD700') {
        const particleCount = 20;
        const particles = [];
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 6px;
                height: 6px;
                background: ${color};
                border-radius: 50%;
                pointer-events: none;
                z-index: 10000;
                left: ${x}px;
                top: ${y}px;
            `;
            
            document.getElementById('particles').appendChild(particle);
            particles.push(particle);
            
            // Animate particle
            const angle = (Math.PI * 2 * i) / particleCount;
            const velocity = Math.random() * 100 + 50;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;
            
            let posX = x;
            let posY = y;
            let opacity = 1;
            
            const animate = () => {
                posX += vx * 0.02;
                posY += vy * 0.02 + 1; // gravity
                opacity -= 0.02;
                
                particle.style.left = posX + 'px';
                particle.style.top = posY + 'px';
                particle.style.opacity = opacity;
                
                if (opacity > 0) {
                    requestAnimationFrame(animate);
                } else {
                    particle.remove();
                }
            };
            
            requestAnimationFrame(animate);
        }
    }
    
    // Number counting animation
    animateNumber(element, start, end, duration = 1000) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }
    
    // Typewriter effect
    typeWriter(element, text, speed = 50) {
        element.textContent = '';
        let i = 0;
        
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }
}

// Initialize animation manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const animationManager = new AnimationManager();
    
    // Make animation manager globally available
    window.animationManager = animationManager;
    
    // Setup keyboard shortcuts for animations
    document.addEventListener('keydown', (e) => {
        // Space bar for random animation
        if (e.code === 'Space' && e.ctrlKey) {
            e.preventDefault();
            const hero = document.querySelector('.hero');
            if (hero) {
                animationManager.triggerSuccessAnimation(hero);
            }
        }
    });
});

// CSS animations that can be triggered via JavaScript
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-20px) rotate(90deg); }
        50% { transform: translateY(-10px) rotate(180deg); }
        75% { transform: translateY(-30px) rotate(270deg); }
        100% { transform: translateY(0px) rotate(360deg); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px var(--primary-color); }
        50% { box-shadow: 0 0 20px var(--primary-color); }
        100% { box-shadow: 0 0 5px var(--primary-color); }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .shake {
        animation: shake 0.6s ease-in-out;
    }
    
    .pulse {
        animation: pulse 1s ease-in-out infinite;
    }
    
    .glow {
        animation: glow 2s ease-in-out infinite;
    }
    
    .floating-symbol {
        will-change: transform;
    }
    
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
        
        .floating-symbol {
            display: none;
        }
    }
`;

document.head.appendChild(style);