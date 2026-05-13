# 🤖 Production‑Ready GenAI Career Chatbot

A tiny Streamlit app that uses **Google Gemini (Google Gen AI)** to answer career‑related questions.  
The code is split into a clean package (`app/`) and a top‑level `streamlit_app.py` entry point.

## Prerequisites

| Item | Minimum |
|------|----------|
| Python | 3.11 |
| Git | any |
| Google Cloud project with the **Generative Language API** enabled | – |
| (Optional) Billing | required only for paid models (`gemini‑2.0‑flash`, etc.) |

---  

## Setup (local development)

```bash
# 1️⃣ Clone the repo
git clone https://github.com/sohanjammula/Gen-AI-bot-production-ready-.git
cd Gen-AI-bot-production-ready-

# 2️⃣ Create & activate a virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt
pip install -U google-genai   # ensure the latest GenAI SDK

# 4️⃣ Add your Gemini API key
echo GEMINI_API_KEY=YOUR_REAL_KEY > .env   # replace YOUR_REAL_KEY

# Running the chatbot

streamlit run streamlit_app.py

# Changing the model (optional)
class GeminiService:
    def __init__(self, model_name: str = "gemini-2.0-flash"):

