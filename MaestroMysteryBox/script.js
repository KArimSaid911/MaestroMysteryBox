document.addEventListener('DOMContentLoaded', () => {
    const mysteryBox = document.querySelector('.mystery-box');
    const prizeDisplay = document.getElementById('prize-display');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const confettiContainer = document.querySelector('.confetti-container');

    // Get prize from URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const encodedPrize = urlParams.get('p');
    let prize = "No prize found";
    
    if (encodedPrize) {
        try {
            // Simple URL decoding
            prize = encodedPrize.replace(/_/g, ' ');
        } catch (e) {
            console.error('Error decoding prize:', e);
        }
    }

    // Create confetti
    function createConfetti() {
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.animationDelay = Math.random() * 3 + 's';
            confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 80%, 50%)`;
            confettiContainer.appendChild(confetti);

            // Remove confetti after animation
            confetti.addEventListener('animationend', () => {
                confetti.remove();
            });
        }
    }

    // Simulate loading and reveal prize
    setTimeout(() => {
        loadingSpinner.style.display = 'none';
        mysteryBox.classList.add('open');
        
        setTimeout(() => {
            prizeDisplay.textContent = prize;
            createConfetti();
            
            // Create new confetti every few seconds
            setInterval(createConfetti, 3000);
        }, 1500);
    }, 2000);
}); 