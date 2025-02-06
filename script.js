const token = urlParams.get("token");
        console.log(token)

        const prize = urlParams.get("prize");

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