// Translate button logic
document.getElementById("translateBtn").addEventListener("click", async () => {
    const text = document.getElementById("inputText").value.trim();
    if (!text) return;

    const res = await fetch("/translate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    const data = await res.json();

    document.getElementById("result").style.display = "block";
    document.getElementById("jpOutput").innerText = data.japanese;
    document.getElementById("romajiOutput").innerText = data.pronunciation;
	document.getElementById("grammarOutput").innerText = data.grammar;

    // Save pronunciation for speaking
    window.currentPronunciation = data.pronunciation;
});

// --- Speech synthesis for pronunciation ---
document.getElementById("speakBtn")
    .addEventListener("click", () => {
        const utter = new SpeechSynthesisUtterance(window.currentPronunciation);
        utter.lang = "ja-JP";  // ✔ Correct japanese voice
        speechSynthesis.speak(utter);
    });

