import logging
from pathlib import Path

logfile = Path("logs/app.log")
logfile.parent.mkdir(exist_ok=True)

logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def log(msg: str):
    logger.info(msg)
    print(msg)