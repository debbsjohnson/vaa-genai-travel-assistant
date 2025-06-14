import logging
from pathlib import Path


def setup_logging():
    logging.basicConfig(
        filename=Path("logs/app.log"),
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Prevent verbose logging from dependencies
    logging.getLogger("httpx").setLevel(logging.WARNING)
