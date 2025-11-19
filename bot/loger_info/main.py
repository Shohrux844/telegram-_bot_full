import logging
from dotenv import load_dotenv
from utils.settings import ENV_PATH

load_dotenv(ENV_PATH)

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
