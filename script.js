document.addEventListener('DOMContentLoaded', () => {
    const mysteryBox = document.querySelector('.mystery-box');
    const prizeDisplay = document.getElementById('prize-display');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const confettiContainer = document.querySelector('.confetti-container');

    // Get prize and token from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let prize = urlParams.get('prize');
    let token = urlParams.get('t');

    console.log("Extracted Prize:", prize);
    console.log("Extracted Token:", token);

    // Retrieve stored token from local storage
    const storedToken = localStorage.getItem('claimed_prize_token');

    // 🚨 If user already claimed a prize, show "No double dipping" message 🚨
    if (storedToken === token) {
        loadingSpinner.style.display = 'none';
        prizeDisplay.innerHTML = `<span style="color: red; font-weight: bold;">❌ Oops, frens! You already hit the jackpot once, no double dipping! 🎰</span>`;
        console.error("User already claimed the prize!");
        return;
    }

    // Simulate loading and reveal prize
    setTimeout(() => {
        loadingSpinner.style.display = 'none';
        mysteryBox.classList.add('open');

        setTimeout(() => {
            if (prize) {
                prizeDisplay.innerHTML = `<strong>${decodeURIComponent(prize)}</strong>`;
                console.log("Prize displayed successfully.");

                // ✅ Store the token in localStorage to prevent multiple claims
                localStorage.setItem('claimed_prize_token', token);
            } else {
                prizeDisplay.innerHTML = `<span style="color: red; font-weight: bold;">No prize found</span>`;
                console.error("No prize found in URL parameters.");
            }
            createConfetti();

            // Create new confetti every few seconds
            setInterval(createConfetti, 3000);
        }, 1500);
    }, 2000);

    // Confetti effect
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
}); 