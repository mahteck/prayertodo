"""
Logging configuration for SalaatFlow chatbot.

Provides structured logging with:
- Console output (INFO level)
- File logging (DEBUG level)
- Error file logging (ERROR level)
- Secret filtering to redact sensitive data
"""

import logging
import os
import re
from pathlib import Path
from typing import Optional


class SecretFilter(logging.Filter):
    """Filter to redact sensitive information from logs."""

    # Patterns to match secrets
    SECRET_PATTERNS = [
        # Gemini API keys (AIza...)
        (r'(AIza[a-zA-Z0-9_-]{35})', '[REDACTED_GEMINI_KEY]'),
        # Bearer tokens
        (r'(Bearer\s+)([a-zA-Z0-9_\-\.]+)', r'\1[REDACTED_TOKEN]'),
        # Generic API keys in various formats
        (r'(api[_-]?key["\s:=]+)([a-zA-Z0-9-_]+)', r'\1[REDACTED_KEY]'),
        # Passwords
        (r'(password["\s:=]+)([^\s,}\]]+)', r'\1[REDACTED_PASSWORD]'),
        # Database URLs with credentials
        (r'(postgresql://[^:]+:)([^@]+)(@)', r'\1[REDACTED_DB_PASS]\3'),
        # Authorization headers
        (r'(Authorization["\s:]+)([^\s,}\]]+)', r'\1[REDACTED_AUTH]'),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log record to redact secrets.

        Args:
            record: Log record to filter

        Returns:
            True (always allow the record, just modify it)
        """
        # Redact secrets in the message
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            for pattern, replacement in self.SECRET_PATTERNS:
                record.msg = re.sub(pattern, replacement, record.msg, flags=re.IGNORECASE)

        # Redact secrets in arguments
        if hasattr(record, 'args') and record.args:
            if isinstance(record.args, dict):
                record.args = self._redact_dict(record.args)
            elif isinstance(record.args, (tuple, list)):
                record.args = tuple(self._redact_value(arg) for arg in record.args)

        return True

    def _redact_value(self, value):
        """Redact secrets from a value."""
        if isinstance(value, str):
            result = value
            for pattern, replacement in self.SECRET_PATTERNS:
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
            return result
        elif isinstance(value, dict):
            return self._redact_dict(value)
        elif isinstance(value, (list, tuple)):
            return type(value)(self._redact_value(v) for v in value)
        return value

    def _redact_dict(self, d: dict) -> dict:
        """Redact secrets from dictionary values."""
        redacted = {}
        sensitive_keys = {'api_key', 'apikey', 'token', 'password', 'secret', 'authorization', 'auth'}

        for key, value in d.items():
            # Check if key name indicates sensitive data
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                redacted[key] = '[REDACTED]'
            elif isinstance(value, str):
                redacted[key] = self._redact_value(value)
            elif isinstance(value, dict):
                redacted[key] = self._redact_dict(value)
            elif isinstance(value, (list, tuple)):
                redacted[key] = type(value)(self._redact_value(v) for v in value)
            else:
                redacted[key] = value

        return redacted


def setup_logging(
    log_dir: Optional[str] = None,
    log_level: str = "INFO",
    enable_json: bool = False
) -> None:
    """
    Configure logging for the SalaatFlow application.

    Args:
        log_dir: Directory for log files (default: ./logs)
        log_level: Console logging level (default: INFO)
        enable_json: Enable JSON formatted logs (default: False)
    """
    # Determine log directory
    if log_dir is None:
        log_dir = os.path.join(os.getcwd(), 'logs')

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # File paths
    main_log_file = log_path / 'chatbot.log'
    error_log_file = log_path / 'chatbot_errors.log'

    # Create formatters
    if enable_json:
        # JSON formatter for structured logging
        log_format = '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}'
    else:
        # Standard formatter
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(log_format)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all levels

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler (INFO level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SecretFilter())
    root_logger.addHandler(console_handler)

    # File handler for all logs (DEBUG level)
    file_handler = logging.FileHandler(main_log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(SecretFilter())
    root_logger.addHandler(file_handler)

    # Error file handler (ERROR level only)
    error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(SecretFilter())
    root_logger.addHandler(error_handler)

    # Log initialization message
    logger = logging.getLogger(__name__)
    logger.info("✅ Logging configured successfully")
    logger.info(f"📂 Logs directory: {log_path.absolute()}")
    logger.info(f"📝 Main log: {main_log_file.name}")
    logger.info(f"❌ Error log: {error_log_file.name}")
    logger.debug(f"Console log level: {log_level}")
    logger.debug(f"File log level: DEBUG")
    logger.debug(f"JSON formatting: {enable_json}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Example usage for testing
if __name__ == "__main__":
    setup_logging()

    logger = get_logger(__name__)

    # Test logging
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Test secret filtering
    logger.info("API Key: AIzaSyBa-hcy0emMTYAwu2A_vPeGDznFlDXTjwA")
    logger.info("Bearer token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    logger.info("Password: password=SuperSecret123")
    logger.info("Database: postgresql://user:mypassword@localhost/db")

    print("\n✅ Logging test complete. Check logs/chatbot.log and logs/chatbot_errors.log")
