document.addEventListener('DOMContentLoaded', () => {
    const prizeDisplay = document.getElementById('prize-display');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const mysteryBox = document.querySelector('.mystery-box');
    const rollingText = document.createElement("p");

    // Get prize from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let prize = urlParams.get('prize');

    console.log("Prize fetched from URL:", prize); // Debugging

    // Show rolling effect
    rollingText.innerHTML = "🎲 Rolling the dice...";
    rollingText.style.color = "#ffffff"; 
    rollingText.style.fontSize = "18px"; 
    rollingText.style.fontWeight = "bold";
    rollingText.style.textAlign = "center";
    document.body.appendChild(rollingText);

    // Simulate a rolling effect before revealing the prize
    setTimeout(() => {
        rollingText.remove(); // Remove rolling text
        loadingSpinner.style.display = 'none'; // Hide loading animation
        mysteryBox.classList.add('open'); // Show the box opening effect

        if (prize) {
            prizeDisplay.innerHTML = `<strong>${decodeURIComponent(prize)}</strong>`;
            console.log("Prize displayed successfully.");
        } else {
            prizeDisplay.innerHTML = `<span style="color: red; font-weight: bold;">No prize found</span>`;
            console.error("No prize found in URL parameters.");
        }
    }, 3000); // Wait 3 seconds before revealing prize
}); 