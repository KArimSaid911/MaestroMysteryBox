document.addEventListener('DOMContentLoaded', () => {
    const mysteryBox = document.querySelector('.mystery-box');
    const prizeDisplay = document.getElementById('prize-display');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const confettiContainer = document.querySelector('.confetti-container');

    // Get prize from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const prize = urlParams.get('prize');
    const token = urlParams.get('t');

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
            if (prize) {
                prizeDisplay.textContent = decodeURIComponent(prize);
            } else {
                prizeDisplay.textContent = "No prize found";
            }
            createConfetti();
            
            // Create new confetti every few seconds
            setInterval(createConfetti, 3000);
        }, 1500);
    }, 2000);
}); 