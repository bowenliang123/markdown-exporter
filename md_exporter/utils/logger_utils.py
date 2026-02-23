import logging
import os


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Add Dify plugin logger handler if LOAD_FROM_DIFY_PLUGIN is set to "1" in main.py
    if os.environ.get("LOAD_FROM_DIFY_PLUGIN") == "1":
        from dify_plugin.config.logger_format import plugin_logger_handler  # noqa: PLC0415

        logger.addHandler(plugin_logger_handler)

    # Add stdio handler
    stdio_handler = logging.StreamHandler()
    stdio_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdio_handler.setFormatter(stdio_formatter)
    logger.addHandler(stdio_handler)

    return logger
