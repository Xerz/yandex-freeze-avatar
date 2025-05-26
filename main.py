import time
import logging
import sys

from telegram_utils import send_message
from update_avatar_utils import auth_and_update
from utils import get_avatar_id
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

try:
    avatar_id = get_avatar_id()
    send_message("Avatar freeze service started. Monitoring avatar changes...")
    while True:
        try:
            new_avatar_id = get_avatar_id()
            if new_avatar_id != avatar_id:
                send_message("Avatar has changed. Updating...")
                auth_and_update()
                avatar_id = get_avatar_id()
                if avatar_id != new_avatar_id:
                    send_message("Avatar has been successfully updated.")
                    logging.info("Avatar updated successfully.")
                else:
                    send_message("Avatar update failed.")
                    logging.warning("Avatar update failed.")
            time.sleep(6)  # Ждем 6 секунд перед следующей проверкой
        except Exception as e:
            logging.error(f"Error in main loop: {e}", exc_info=True)
            send_message(f"Error occurred: {e}")
            time.sleep(6)
except KeyboardInterrupt:
    logging.info("Service stopped by user.")
    send_message("Avatar freeze service stopped.")
