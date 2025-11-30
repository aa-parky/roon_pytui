"""Main entry point for the Roon PyTUI application."""

import logging
import sys
from pathlib import Path

from .ui.app import RoonTUI


def setup_logging() -> None:
    """Set up logging configuration."""
    log_dir = Path.home() / ".config" / "roon-pytui"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "roon-pytui.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stderr),
        ],
    )


def main() -> None:
    """Main entry point."""
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting Roon PyTUI")

    try:
        app = RoonTUI()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.exception(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
