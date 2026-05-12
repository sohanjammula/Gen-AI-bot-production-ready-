import os
from dotenv import load_dotenv
import google.generativeai as genai          # <-- correct import
from utils.logger import get_logger

load_dotenv()
logger = get_logger()


class GeminiService:
    """
    Thin wrapper around Google Gemini (Generative AI) that:
    * reads the API key from the .env file
    * creates a GenerativeModel instance
    * returns plain‑text responses
    """

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """Initialise the GenAI client and pick a model."""
        try:
            # Configure the library once (global state)
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

            # The GenerativeModel object is what you use to call generate_content
            self.model = genai.GenerativeModel(model_name)
            self.model_name = model_name
            logger.info("Gemini client initialized")
        except Exception as exc:                # pragma: no‑cover
            logger.error(f"Initialization error: {exc}")
            raise

    def generate_response(self, prompt: str) -> str:
        """Send *prompt* to Gemini and return the text answer."""
        try:
            response = self.model.generate_content(prompt)
            # response.text may be None if Gemini didn’t return any text
            return response.text if getattr(response, "text", None) else "No response generated."
        except Exception as exc:                # pragma: no‑cover
            logger.error(f"Gemini API Error: {exc}")
            return "⚠️ Sorry, I'm having trouble right now."
