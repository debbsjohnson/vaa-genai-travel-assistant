import logging
from travel_assistant.core.logging import setup_logging


def test_logging_setup(tmp_path):
    """Test logging creates files and captures messages"""
    logs_dir = tmp_path / "logs"

    # override log path
    import travel_assistant.core.logging as log_module

    log_module.logs_dir = logs_dir  # set the global variable

    log_module.setup_logging()
    logger = logging.getLogger("test")
    logger.info("Test message")

    log_file = logs_dir / "app.log"
    assert log_file.exists()
    assert "Test message" in log_file.read_text()
