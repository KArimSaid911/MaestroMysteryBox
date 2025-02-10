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


