import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging.

    Sets a basic configuration and aligns common server loggers
    with the specified level.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name).setLevel(numeric_level)
