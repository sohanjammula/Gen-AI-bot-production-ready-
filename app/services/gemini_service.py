import os
import time
import warnings
from typing import Callable

from dotenv import load_dotenv
from google import genai                     # ← correct import for the new SDK
from google.api_core import exceptions as api_exceptions
from utils.logger import get_logger

# Hide the deprecation warning that the old package used to emit
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()
logger = get_logger()


# ----------------------------------------------------------------------
# Helper: exponential back‑off for 429 (quota exhausted)
# ----------------------------------------------------------------------
def _retry_with_backoff(fn: Callable, max_attempts: int = 3) -> any:
    """
    Call *fn*; on a 429 `ResourceExhausted` error retry with exponential back‑off.
    If all attempts fail the exception is re‑raised so the caller can present a
    friendly fallback.
    """
    delay = 1.0          # first retry = 1 s
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except api_exceptions.ResourceExhausted as exc:
            # The server sometimes tells us exactly how long to wait.
            suggested = None
            try:
                import re
                m = re.search(r'"retryDelay"\s*:\s*"(\d+\.?\d*)s"', str(exc))
                if m:
                    suggested = float(m.group(1))
            except Exception:
                pass

            wait = suggested if suggested is not None else delay
            logger.warning(
                f"Gemini quota exhausted – retry {attempt}/{max_attempts} after {wait:.1f}s"
            )
            time.sleep(wait)
            delay *= 2   # exponential growth for the next try
    # If we get here every attempt has failed.
    raise api_exceptions.ResourceExhausted("Quota exhausted after retries")


# ----------------------------------------------------------------------
class GeminiService:
    """
    Thin wrapper around the Google GenAI client.
    * Uses the new `genai.Client` API.
    * Handles 429‑quota errors with back‑off.
    * Returns a short user‑friendly message for any other failure.
    """

    # ---- Choose a model that is available on the free tier ----
    #   - gemini-1.5-flash  (fast, low‑cost, free tier)
    #   - gemini-1.5-pro   (higher quality, also free‑tier)
    #   - gemini-2.0-flash (requires a paid quota; will raise INVALID_ARGUMENT otherwise)
    # ------------------------------------------------------------
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        try:
            # The client reads the API key from the environment variable
            # `GEMINI_API_KEY` (or `GOOGLE_API_KEY`). No `configure()` call needed.
            self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            self.model_name = model_name
            logger.info("Gemini client initialized")
        except Exception as exc:                               # pragma: no‑cover
            logger.error(f"Gemini client init error: {exc}")
            raise

    # --------------------------------------------------------------
    def generate_response(self, prompt: str) -> str:
        """
        Send *prompt* to Gemini and return the plain‑text answer.
        Handles quota‑exhaustion (429) with exponential back‑off,
        and returns a friendly fallback for any other error.
        """

        def _call():
            # The request format is exactly what the SDK expects.
            return self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

        try:
            response = _retry_with_backoff(_call)
            # `.text` may be None if Gemini returned no textual content.
            return response.text if getattr(response, "text", None) else "No response generated."
        except api_exceptions.ResourceExhausted:
            # All retries exhausted → the quota really is out.
            return (
                "⚠️ **Gemini quota exhausted** – please wait a moment or "
                "upgrade your Google Cloud billing plan."
            )
        except api_exceptions.InvalidArgument as exc:
            # This is the branch that produced the 400 error before.
            logger.error(f"Invalid request (model name / payload): {exc}")
            return (
                "⚠️ Bad request – the selected model may not be available for your "
                "current plan. Try a different model (e.g. `gemini-1.5-flash`)."
            )
        except Exception as exc:
            logger.error(f"Unexpected Gemini error: {exc}")
            return "⚠️ Sorry, I'm having trouble right now."
