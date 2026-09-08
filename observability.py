"""Observability module providing tracing, JSON logging, and PII redaction."""
import json
import logging
import re
import sys
from typing import Any, Dict
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# OpenTelemetry Tracer setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("fde.chat.pulse.agent")

# PII Scrubbing patterns
EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
TOKEN_REGEX = re.compile(r"(AIza[0-9A-Za-z-_]{35}|ghp_[0-9A-Za-z]{36})")


class JsonFormatter(logging.Formatter):
    """Formats logs into structured JSON payloads."""
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "intent"):
            log_obj["agent_intent"] = getattr(record, "intent")
        if hasattr(record, "outcome"):
            log_obj["actual_outcome"] = getattr(record, "outcome")
        if hasattr(record, "context"):
            log_obj["metadata"] = getattr(record, "context")
        return json.dumps(log_obj)


def setup_logger(name: str = "agent_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger


logger = setup_logger()


def scrub_pii(text: str) -> str:
    """Removes emails and API tokens prior to logging or storage."""
    scrubbed = EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
    scrubbed = TOKEN_REGEX.sub("[REDACTED_TOKEN]", scrubbed)
    return scrubbed
