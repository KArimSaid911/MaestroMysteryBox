// URL Parameter Handling
function getUrlParameters() {
    // Get everything after the # symbol
    const params = window.location.hash.substring(1);
    const urlParams = new URLSearchParams(params);
    return {
        token: urlParams.get('t'),
        prize: urlParams.get('prize'),
        error: urlParams.get('error')
    };
}

// Route Handler
function handleRoute() {
    const params = getUrlParameters();
    const mysteryBox = document.querySelector('.mystery-box');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const prizeMessage = document.getElementById('prizeMessage');
    const finalClaimBtn = document.getElementById('finalClaimBtn');

    // Hide all sections initially
    loading.style.display = 'none';
    result.style.display = 'none';
    mysteryBox.style.display = 'block';

    if (params.error === 'already-claimed') {
        mysteryBox.style.display = 'none';
        result.style.display = 'block';
        prizeMessage.textContent = "Oops! You've already claimed a prize. No double dipping! 🎰";
        return;
    }

    if (params.prize && params.token) {
        // Show prize result directly
        mysteryBox.style.display = 'none';
        result.style.display = 'block';
        prizeMessage.textContent = `🎉 Congratulations! You've won: ${decodeURIComponent(params.prize)}`;
        finalClaimBtn.style.display = 'block';
        return;
    }

    if (params.token) {
        // Add click handler for mystery box
        mysteryBox.addEventListener('click', handleMysteryBoxClick);
    } else {
        // No valid parameters, show error
        mysteryBox.style.display = 'none';
        result.style.display = 'block';
        prizeMessage.textContent = "Invalid or expired mystery box link! 😔";
    }
}

// Mystery Box Click Handler
function handleMysteryBoxClick() {
    const mysteryBox = document.querySelector('.mystery-box');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    // Disable further clicks
    mysteryBox.style.pointerEvents = 'none';
    mysteryBox.style.display = 'none';
    
    // Show loading animation
    loading.style.display = 'block';
    
    // Animate loading messages
    const messages = loading.querySelectorAll('.loading-text');
    const progressBar = loading.querySelector('.progress-bar');
    let currentMessage = 0;
    
    messages.forEach((msg, index) => {
        setTimeout(() => {
            messages[Math.max(0, index - 1)].style.opacity = '0';
            msg.style.opacity = '1';
            msg.style.transform = 'translateY(0)';
            progressBar.style.width = `${(index + 1) * 33.33}%`;
            
            if (index === messages.length - 1) {
                setTimeout(() => {
                    loading.style.display = 'none';
                    result.style.display = 'block';
                    result.style.opacity = '1';
                    result.style.transform = 'translateY(0)';
                }, 1000);
            }
        }, index * 1000);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', handleRoute);

// Listen for hash changes
window.addEventListener('hashchange', handleRoute);