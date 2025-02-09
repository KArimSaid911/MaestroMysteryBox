document.addEventListener('DOMContentLoaded', async function() {
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const progressBar = document.querySelector('.progress-bar');
    const finalClaimBtn = document.getElementById('finalClaimBtn');
    const prizeMessage = document.getElementById('prizeMessage');

    if (!loadingDiv || !resultDiv || !progressBar || !finalClaimBtn || !prizeMessage) {
        console.error("Some elements are missing from the HTML.");
        return;
    }

    // List of possible prizes
    function getRandomPrize() {
        const prizes = [
            "1 Maestro premium account for 1 month",
            "2 Maestro premium accounts for 1 week",
            "3 Maestro premium accounts for 1 week",
            "4 Maestro premium accounts for 1 week",
            "5 Maestro premium accounts for 1 week",
            "6 Maestro premium accounts for 1 week",
            "7 Maestro premium accounts for 3 days",
            "8 Maestro premium accounts for 3 days",
            "9 Maestro premium accounts for 1 day",
            "10 Maestro premium accounts for 1 day"
        ];
        
        return prizes[Math.floor(Math.random() * prizes.length)];
    }

    async function animateLoading() {
        const messages = document.querySelectorAll('.loading-text');
        let progress = 0;
        const progressIncrement = 100 / (messages.length + 1);

        for (let i = 0; i < messages.length; i++) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            messages[i].style.opacity = '1';
            messages[i].style.transform = 'translateY(0)';
            progress += progressIncrement;
            progressBar.style.width = `${progress}%`;
        }

        await new Promise(resolve => setTimeout(resolve, 1000));
        progress = 100;
        progressBar.style.width = `${progress}%`;
    }

    // Start loading automatically when the page loads
    loadingDiv.style.display = 'block';

    await animateLoading();
    await new Promise(resolve => setTimeout(resolve, 500));

    loadingDiv.style.display = 'none';
    resultDiv.style.display = 'block';
    resultDiv.style.opacity = '1';
    resultDiv.style.transform = 'translateY(0)';

    // Set the prize message dynamically
    const randomPrize = getRandomPrize();
    prizeMessage.innerHTML = `Congratulations! You won ${randomPrize}!`;

    finalClaimBtn.style.display = 'inline-block';

    finalClaimBtn.addEventListener('click', () => {
        window.open('https://t.me/CrypticKimo', '_blank');
    });

});


// Function to claim a token when a user clicks the mystery box
// Function to get token from the URL
// Function to extract token from URL parameters
function getTokenFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");

    if (!token) {
        alert("❌ No token provided! Please use a valid link.");
        return null;
    }
    return token;
}

// Function to check if token is already claimed
async function checkToken(token) {
    try {
        const response = await fetch(`https://maestro-mysterybox-backend.onrender.com/check_token?token=${token}`);
        const data = await response.json();

        if (data.alreadyClaimed) {
            alert(`🎁 You already won: ${data.prize}`);
        } else {
            claimToken(token);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Function to claim the token
async function claimToken(token) {
    try {
        const response = await fetch("https://maestro-mysterybox-backend.onrender.com/claim_token", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token: token })
        });

        const data = await response.json();
        if (data.status === "success") {
            alert(`🎉 Congratulations! You won: ${data.prize}`);
        } else {
            alert(`❌ ${data.error}`);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Main execution: Get token and check it
document.addEventListener("DOMContentLoaded", () => {
    const token = getTokenFromURL();
    if (token) {
        checkToken(token);
    }
});
