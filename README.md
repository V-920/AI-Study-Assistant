# AI Study Assistant

An AI-powered study tool that helps students understand and revise their notes.

## Features

- **Summarize:** Generate summaries of study notes.
- **Explain:** Get explanations of concepts.
- **Quiz Generator:** Generate quizzes to test your understanding.
- **Navigation:** Quickly move between sections of the application.

## Tech Stack

- HTML
- CSS
- JavaScript
- Python
- FastAPI
- Google Gemini API

## Setup

### 1. Clone or download this repository

### 2. Install Python dependencies

Open a terminal in the `backend` directory and run:

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

Create a `.env` file inside the `backend` directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own Gemini API key. Never publish your real API key.

### 4. Start the backend

From the `backend` directory, run:

```bash
python -m uvicorn main:app --reload
```

### 5. Open the frontend

Open `index.html` in your browser or use a local development server.

## Note

The backend requires a valid Gemini API key. Users must configure their own key to use the AI features.
