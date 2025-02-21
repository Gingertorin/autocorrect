from pydantic import BaseModel
import math
import random
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from input import generate_candidates
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import numpy as np

# Import typo generator (Ensure 'input.py' exists)
try:
    from input import generate_candidates
except ImportError:
    print("Error: 'input.py' not found. Ensure it's in the same directory as 'main.py'.")

app = FastAPI()

# ✅ CORS FIX: Allow frontend (React) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Language Detection Endpoint (Placeholder)
class TextInput(BaseModel):
    text: str

@app.post("/detect_language")
def detect_language(input_data: TextInput):
    return {"detected_language": "en"}

# 📌 Autocorrect Endpoint (Placeholder)
@app.post("/correct_word")
def correct_word(input_data: TextInput):
    return {"corrected_text": input_data.text}

@app.get("/wordcloud/{word}")
def get_wordcloud(word: str):
    typo_candidates = generate_candidates(word)
    
    # Ensure typo data is available
    if not typo_candidates:
        return {"error": "No typos generated"}

    # **🔹 Normalize Probabilities** to prevent oversized words
    max_typo_prob = max(typo_candidates.values(), default=0.1)
    min_typo_prob = min(typo_candidates.values(), default=0.001)

    word_freq = {
        typo: np.interp(prob, [min_typo_prob, max_typo_prob], [10, 80])  # Scale between 10-80
        for typo, prob in typo_candidates.items()
    }

    # Ensure main word is **always** the largest
    word_freq[word] = max(word_freq.values()) * 1.5  # 1.5x the largest typo

    # Generate the word cloud
    wc = WordCloud(
        width=800, height=800, background_color="white", colormap="coolwarm",
        max_font_size=100  # Prevents extreme sizes
    ).generate_from_frequencies(word_freq)

    # Save image to buffer
    img_buffer = io.BytesIO()
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    
    return Response(content=img_buffer.getvalue(), media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
