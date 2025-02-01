async function askQuestion() {
    const query = document.getElementById("query").value.trim();
    const responseBox = document.getElementById("response");
    if (!query) {
        responseBox.innerText = "Please enter a question.";
        return;
    }
    responseBox.innerText = "Processing...";
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const data = await response.json();
        responseBox.innerText = data.response;
    } catch (error) {
        responseBox.innerText = "Error fetching response. Please try again.";
    }
}
