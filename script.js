document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    console.log("Token:", token);

    const prize = urlParams.get("prize");
    console.log("Prize:", prize);

    const prizeDisplay = document.getElementById('prize-display');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const mysteryBox = document.querySelector('.mystery-box');
    const rollingText = document.createElement("p");

    if (!token) {
        alert("No token provided!");
        return;
    }

    // Get used tokens from localStorage
    let usedTokens = JSON.parse(localStorage.getItem("usedTokens")) || [];

    if (usedTokens.includes(token)) {
        // Token already used, show "already-clicked" div and hide "winner"
        document.getElementById("winner").style.display = "none";
        document.getElementById("already-clicked").style.display = "block";
        document.getElementById("already-clicked").textContent = "Oops, frens! You already hit the jackpot once, no double dipping! ";
    } else {
        // Store token in localStorage
        usedTokens.push(token);
        localStorage.setItem("usedTokens", JSON.stringify(usedTokens));

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
    }
});