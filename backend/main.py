import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from the .env file.")

client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class NotesRequest(BaseModel):
    notes: str


@app.get("/")
def home():
    return {"message": "AI Study Assistant backend is running!"}


@app.post("/summarize")
def summarize(request: NotesRequest):
    if not request.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide notes to summarize."
        )

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=(
                "Summarize the following study notes clearly and accurately. "
                "Preserve the important facts and key concepts. "
                "Use simple language and bullet points where helpful.\n\n"
                f"Study notes:\n{request.notes}"
            ),
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="The AI did not return a summary."
            )

        return {"summary": response.text}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI summarization failed. Check the server terminal."
        )
        
class ExplainRequest(BaseModel):
    topic: str


@app.post("/explain")
def explain(request: ExplainRequest):
    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic to explain."
        )

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=(
                "Explain the following topic to a school student "
                "using simple language. Include a clear explanation "
                "and one useful example.\n\n"
                f"Topic: {request.topic}"
            ),
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="The AI did not return an explanation."
            )

        return {"explanation": response.text}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Explanation failed. Check the server terminal."
        )
        
class QuizRequest(BaseModel):
    notes: str


@app.post("/quiz")
def generate_quiz(request: QuizRequest):
    if not request.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide notes to generate a quiz."
        )

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=(
                    "Create a quiz with 5 multiple-choice questions based "
                    "on the following study notes. Give 4 options per "
                    "question and identify the correct answer. Include "
                    "a brief explanation for each answer. Use only "
                    "information supported by the notes.\n\n"
                    f"Study notes:\n{request.notes}"
                ),
            )

            if not response.text:
                raise HTTPException(
                    status_code=502,
                    detail="The AI did not generate a quiz."
                )

            return {"quiz": response.text}

        except HTTPException:
            raise

        except Exception as e:
            print(f"Quiz attempt {attempt + 1} failed:", repr(e))

            if attempt < 2:
                time.sleep(2 * (attempt + 1))
            else:
                raise HTTPException(
                    status_code=502,
                    detail="Quiz generation failed after 3 attempts. Please try again later."
                )
                