document.addEventListener("DOMContentLoaded", () => {
    const mysteryBox = document.querySelector('.mystery-box');
    const prizeDisplay = document.getElementById('prize-display');
    const loadingText = document.getElementById('loading-text');
    const loadingBar = document.getElementById('loading-bar');
    const confettiContainer = document.querySelector('.confetti-container');

    // Get prize from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let prize = urlParams.get('prize');

    // Rolling Dice Messages
    const rollingMessages = ["🎲 Rolling the dice...", "🎰 Spinning...", "🎁 Choosing your prize..."];
    
    let messageIndex = 0;

    // Change dice rolling text every 1 second
    const diceRollInterval = setInterval(() => {
        loadingText.innerText = rollingMessages[messageIndex % rollingMessages.length];
        messageIndex++;
    }, 1000);

    // Simulate Loading and Reveal Prize
    setTimeout(() => {
        clearInterval(diceRollInterval); // Stop changing text
        loadingText.style.display = 'none'; // Hide rolling text
        loadingBar.style.display = 'none';  // Hide loading bar

        setTimeout(() => {
            if (prize) {
                prizeDisplay.innerHTML = `<strong>${decodeURIComponent(prize)}</strong>`;
                prizeDisplay.style.opacity = "1"; // Show prize
            } else {
                prizeDisplay.innerHTML = `<span style="color: red; font-weight: bold;">No prize found</span>`;
            }
            createConfetti(); // Show confetti
        }, 1000);
    }, 2500); // Wait for 2.5 seconds before revealing prize

    // Confetti Effect
    function createConfetti() {
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.animationDelay = Math.random() * 3 + 's';
            confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 80%, 50%)`;
            confettiContainer.appendChild(confetti);

            confetti.addEventListener('animationend', () => {
                confetti.remove();
            });
        }
    }
}); 