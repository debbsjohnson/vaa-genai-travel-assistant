import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# define module-level logs_dir that can be overridden
logs_dir = None


def setup_logging():
    global logs_dir

    # if not set, use default location
    if logs_dir is None:
        # use absolute path to project root/logs
        logs_dir = Path(__file__).resolve().parent.parent / "logs"

    # create logs directory with parent directories if needed
    logs_dir.mkdir(exist_ok=True, parents=True)

    # configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # file handler (rotating logs), 5mb per file and keeps 3 for backup
    file_handler = RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    # console handler (for docker/container logs)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # reduce noise from dependencies
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.INFO)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
