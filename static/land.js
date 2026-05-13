 // Navbar scroll effect
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            });
        });
        
        // Animate elements on scroll
        function animateOnScroll() {
            const elements = document.querySelectorAll('.feature-card, .step-card, .testimonial-card');
            
            elements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const elementVisible = 150;
                
                if (elementTop < window.innerHeight - elementVisible) {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }
            });
        }
        
        // Set initial state for animation
        document.querySelectorAll('.feature-card, .step-card, .testimonial-card').forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        });
        
        // Trigger animation on load and scroll
        window.addEventListener('load', animateOnScroll);
        window.addEventListener('scroll', animateOnScroll);
        
        // Robot screen text animation
        const screenText = document.querySelector('.screen-text');
        const texts = ["Hello!", "Ready!", "Fun!", "Learn!", "Play!"];
        let currentTextIndex = 0;
        
        function changeRobotText() {
            screenText.style.opacity = '0';
            setTimeout(() => {
                currentTextIndex = (currentTextIndex + 1) % texts.length;
                screenText.textContent = texts[currentTextIndex];
                screenText.style.opacity = '1';
            }, 300);
        }
        
        // Change text every 3 seconds
        setInterval(changeRobotText, 3000);