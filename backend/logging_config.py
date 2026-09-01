import logging
import json
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }

        # Masking sensitive data if it happens to be in the message
        if "API_KEY" in log_record["message"]:
            log_record["message"] = "MASKED SENSITIVE DATA"

        return json.dumps(log_record)

def setup_logging(env: str):
    logger = logging.getLogger()

    if env == "prod":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    # Remove existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)
