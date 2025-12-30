"""
Robust Google Gemini API Client

Provides error handling, retry logic, and logging for Gemini API calls.
"""

import time
import logging
from typing import Optional, Dict, Any, List

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from .config import GeminiConfig

logger = logging.getLogger(__name__)


# Custom Exception Classes
class GeminiError(Exception):
    """Base exception for all Gemini-related errors."""
    pass


class GeminiAuthError(GeminiError):
    """Authentication failed - invalid API key."""
    pass


class GeminiQuotaError(GeminiError):
    """Quota exceeded - rate limit or usage limit reached."""
    pass


class GeminiNetworkError(GeminiError):
    """Network or timeout error - may be transient."""
    pass


class GeminiClient:
    """
    Robust client for Google Gemini API.

    Features:
    - Automatic retry on network errors
    - Proper exception classification
    - Request/response logging
    - Health check functionality
    """

    def __init__(self, config: GeminiConfig):
        """
        Initialize Gemini client.

        Args:
            config: GeminiConfig instance with API settings
        """
        self.config = config

        # Configure the Gemini API
        genai.configure(api_key=config.api_key)

        # Initialize the model
        try:
            self.model = genai.GenerativeModel(config.model)
            logger.info(f"✅ Gemini client initialized with model: {config.model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini model: {e}")
            raise GeminiError(f"Failed to initialize Gemini model '{config.model}': {str(e)}")

    def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a response from Gemini API.

        Args:
            prompt: The user's input prompt
            system_instruction: Optional system instruction for the model
            context: Optional context dict (may include request_id, user_id, etc.)

        Returns:
            Generated response text

        Raises:
            GeminiAuthError: If API key is invalid
            GeminiQuotaError: If quota is exceeded
            GeminiNetworkError: If network/timeout error occurs
            GeminiError: For other errors
        """
        context = context or {}
        request_id = context.get("request_id", "unknown")

        # Log the request
        logger.debug(
            f"Gemini request started",
            extra={
                "request_id": request_id,
                "prompt_length": len(prompt),
                "model": self.config.model,
                "has_system_instruction": system_instruction is not None,
            }
        )

        start_time = time.time()
        attempt = 0

        while attempt <= self.config.max_retries:
            attempt += 1

            try:
                # Generate content
                if system_instruction:
                    # Create a new model instance with system instruction
                    model_with_instruction = genai.GenerativeModel(
                        self.config.model,
                        system_instruction=system_instruction
                    )
                    response = model_with_instruction.generate_content(prompt)
                else:
                    response = self.model.generate_content(prompt)

                # Extract text from response
                response_text = response.text

                # Log success
                duration = time.time() - start_time
                logger.info(
                    f"Gemini response received",
                    extra={
                        "request_id": request_id,
                        "response_length": len(response_text),
                        "duration": f"{duration:.2f}s",
                        "model": self.config.model,
                        "attempt": attempt,
                    }
                )

                return response_text

            except google_exceptions.Unauthenticated as e:
                # Authentication error - don't retry
                logger.error(
                    f"Gemini API authentication failed",
                    extra={
                        "request_id": request_id,
                        "error_type": "authentication",
                        "attempt": attempt,
                        "will_retry": False,
                    },
                    exc_info=True
                )
                raise GeminiAuthError(
                    f"Invalid Gemini API key. Please verify your API key is correct. "
                    f"Get a new key from https://makersuite.google.com/app/apikey"
                ) from e

            except google_exceptions.ResourceExhausted as e:
                # Quota exceeded - don't retry
                logger.error(
                    f"Gemini API quota exceeded",
                    extra={
                        "request_id": request_id,
                        "error_type": "quota_exceeded",
                        "attempt": attempt,
                        "will_retry": False,
                    },
                    exc_info=True
                )
                raise GeminiQuotaError(
                    f"Gemini API quota exceeded. Please check your usage limits or try again later."
                ) from e

            except (google_exceptions.DeadlineExceeded, google_exceptions.ServiceUnavailable) as e:
                # Network/timeout error - retry if attempts remain
                will_retry = attempt < self.config.max_retries

                logger.warning(
                    f"Gemini API network error (attempt {attempt}/{self.config.max_retries})",
                    extra={
                        "request_id": request_id,
                        "error_type": "network",
                        "attempt": attempt,
                        "will_retry": will_retry,
                    }
                )

                if will_retry:
                    # Wait before retrying
                    delay = self.config.retry_delay * attempt  # Exponential backoff
                    logger.debug(f"Retrying in {delay}s...")
                    time.sleep(delay)
                    continue  # Retry
                else:
                    # Out of retries
                    logger.error(
                        f"Gemini API network error - max retries exceeded",
                        extra={"request_id": request_id},
                        exc_info=True
                    )
                    raise GeminiNetworkError(
                        f"Network error communicating with Gemini API. "
                        f"The service may be temporarily unavailable. Please try again later."
                    ) from e

            except google_exceptions.NotFound as e:
                # Model not found - don't retry
                logger.error(
                    f"Gemini model not found",
                    extra={
                        "request_id": request_id,
                        "model": self.config.model,
                        "error_type": "model_not_found",
                        "attempt": attempt,
                    },
                    exc_info=True
                )
                raise GeminiError(
                    f"The Gemini model '{self.config.model}' is not available. "
                    f"Please check the model name in your configuration."
                ) from e

            except Exception as e:
                # Unexpected error - log and raise
                logger.error(
                    f"Unexpected Gemini API error",
                    extra={
                        "request_id": request_id,
                        "error_type": "unknown",
                        "error_class": type(e).__name__,
                        "attempt": attempt,
                    },
                    exc_info=True
                )
                raise GeminiError(
                    f"An unexpected error occurred while calling Gemini API: {str(e)}"
                ) from e

        # Should never reach here, but just in case
        raise GeminiNetworkError("Max retries exceeded")

    def health_check(self) -> Dict[str, Any]:
        """
        Check Gemini API health.

        Sends a trivial prompt to verify API connectivity.

        Returns:
            Dict with health status:
            {
                "service": "gemini",
                "status": "healthy" | "unhealthy",
                "model": str,
                "timestamp": float,
                "response_length": int,  # if healthy
                "error": str,  # if unhealthy
                "message": str,  # if unhealthy
            }
        """
        timestamp = time.time()

        logger.info("Running Gemini health check...")

        try:
            # Send trivial prompt
            response = self.generate_response(
                prompt="Hello from SalaatFlow health check. Respond with 'OK'.",
                context={"request_id": "health-check"}
            )

            logger.info("✅ Gemini health check passed")

            return {
                "service": "gemini",
                "status": "healthy",
                "model": self.config.model,
                "timestamp": timestamp,
                "response_length": len(response),
            }

        except GeminiAuthError as e:
            logger.error(f"❌ Gemini health check failed: authentication error")
            return {
                "service": "gemini",
                "status": "unhealthy",
                "error": "authentication_failed",
                "message": str(e),
                "timestamp": timestamp,
            }

        except GeminiQuotaError as e:
            logger.error(f"❌ Gemini health check failed: quota exceeded")
            return {
                "service": "gemini",
                "status": "unhealthy",
                "error": "quota_exceeded",
                "message": str(e),
                "timestamp": timestamp,
            }

        except GeminiNetworkError as e:
            logger.error(f"❌ Gemini health check failed: network error")
            return {
                "service": "gemini",
                "status": "unhealthy",
                "error": "network_error",
                "message": str(e),
                "timestamp": timestamp,
            }

        except GeminiError as e:
            logger.error(f"❌ Gemini health check failed: {e}")
            return {
                "service": "gemini",
                "status": "unhealthy",
                "error": "gemini_error",
                "message": str(e),
                "timestamp": timestamp,
            }

        except Exception as e:
            logger.error(f"❌ Gemini health check failed: unexpected error", exc_info=True)
            return {
                "service": "gemini",
                "status": "unhealthy",
                "error": "unknown_error",
                "message": f"Unexpected error: {str(e)}",
                "timestamp": timestamp,
            }


if __name__ == "__main__":
    """Test the Gemini client."""
    import sys
    import os

    print("🧪 Testing Gemini Client...")
    print("=" * 60)

    try:
        # Load config
        from .config import GeminiConfig

        config = GeminiConfig.from_env()
        print(f"✅ Config loaded: model={config.model}")

        # Create client
        client = GeminiClient(config)
        print(f"✅ Client initialized")

        # Health check
        print("\n📊 Running health check...")
        health = client.health_check()

        if health["status"] == "healthy":
            print(f"✅ Health check PASSED")
            print(f"   Model: {health['model']}")
            print(f"   Response length: {health['response_length']} chars")
        else:
            print(f"❌ Health check FAILED")
            print(f"   Error: {health.get('error')}")
            print(f"   Message: {health.get('message')}")
            sys.exit(1)

        # Test simple generation
        print("\n💬 Testing simple generation...")
        response = client.generate_response(
            "Say 'Hello from SalaatFlow!' in one sentence.",
            context={"request_id": "test-001"}
        )
        print(f"✅ Response received:")
        print(f"   {response[:100]}...")

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Test failed:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
