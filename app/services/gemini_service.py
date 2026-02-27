import os
from dotenv import load_dotenv
from google import genai
from utils.logger import get_logger

load_dotenv()
logger = get_logger()


class GeminiService:
    def __init__(self, model_name="gemini-2.0-flash"):
        try:
            self.client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )
            self.model_name = model_name
            logger.info("Gemini client initialized")
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text if response.text else "No response generated."
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return "⚠️ Sorry, I'm having trouble right now."