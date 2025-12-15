// Fun E-commerce JavaScript

// Update cart count on page load
document.addEventListener('DOMContentLoaded', function () {
    updateCartCount();

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.5s ease';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
});

// Update cart count
function updateCartCount() {
    // This would be updated via AJAX in a real implementation
    // For now, we'll use a simple approach
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        // You can fetch this from the server or local storage
        cartCount.textContent = '0';
    }
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Add to cart animation
function addToCartAnimation(button) {
    button.style.transform = 'scale(0.9)';
    setTimeout(() => {
        button.style.transform = 'scale(1)';
    }, 200);
}

// Slide out animation for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(-100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
