const input = document.getElementById("input");
const button = document.getElementById("Button");
const confirms = document.getElementById("confirm");
const summary = document.getElementById("summary");

button.addEventListener("click", async function () {
    const notes = input.value;

    if (notes.trim() === "") {
        confirms.innerText = "Please enter your notes first.";
        return;
    }

    confirms.innerText = "Sending notes to the backend...";
    summary.innerText = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                notes: notes
            })
        });

        if (!response.ok) {
            throw new Error("The server returned an error.");
        }

        const data = await response.json();

        summary.innerText = data.summary;
        confirms.innerText = "Notes received successfully!";

    } catch (error) {
        confirms.innerText = "Could not connect to the backend. Check that the server is running.";
        console.error(error);
    }
});

const topicInput = document.getElementById("topic-input");
const explainButton = document.getElementById("explain-button");
const explainStatus = document.getElementById("explain-status");
const explanation = document.getElementById("explanation");

explainButton.addEventListener("click", async function () {
    const topic = topicInput.value.trim();

    if (topic === "") {
        explainStatus.innerText = "Please enter a topic first.";
        return;
    }

    explainStatus.innerText = "Generating explanation...";
    explanation.innerText = "";

    explainButton.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/explain", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ topic: topic })
        });

        if (!response.ok) {
            throw new Error("The server returned an error.");
        }

        const data = await response.json();

        explanation.innerText = data.explanation;
        explainStatus.innerText = "Explanation generated successfully!";

    } catch (error) {
        explainStatus.innerText = "Could not generate the explanation.";
        console.error(error);
    } finally {
        explainButton.disabled = false;
    }
});

const quizInput = document.getElementById("quiz-input");
const quizButton = document.getElementById("quiz-button");
const quizStatus = document.getElementById("quiz-status");
const quizOutput = document.getElementById("quiz-output");

quizButton.addEventListener("click", async function () {
    const notes = quizInput.value.trim();

    if (!notes) {
        quizStatus.textContent = "Please enter your study notes first.";
        quizOutput.textContent = "";
        return;
    }

    quizStatus.textContent = "Generating your quiz...";
    quizOutput.textContent = "";
    quizButton.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/quiz", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ notes: notes })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Quiz generation failed.");
        }

        quizOutput.textContent = data.quiz;
        console.log("Quiz text length:", quizOutput.textContent.length);
        quizStatus.textContent = "Your quiz is ready!";
    } catch (error) {
        quizStatus.textContent = error.message || "Something went wrong.";
    } finally {
        quizButton.disabled = false;
    }
});
