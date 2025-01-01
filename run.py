import requests
import time
import logging
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("node_sync_monitor.log"),
        logging.StreamHandler()
    ]
)

# Configuration
LOCAL_RPC_URL = os.getenv("LOCAL_RPC_URL", "http://localhost:8899")  # Your node's RPC URL
REFERENCE_RPC_URL = os.getenv("REFERENCE_RPC_URL", "https://api.mainnet-beta.solana.com")  # Reference node RPC URL
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")     # Telegram bot token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")         # Telegram chat ID
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 10))    # Interval to check sync status (seconds)
SYNC_THRESHOLD = int(os.getenv("SYNC_THRESHOLD", 100))   # Threshold for out-of-sync detection (slots)

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in the environment.")

def send_telegram_message(message):
    """
    Send a message to the specified Telegram chat.
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logging.info("Telegram notification sent successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to send Telegram message: {e}")

def get_slot(rpc_url):
    """
    Fetch the current slot from the given RPC URL using the 'getSlot' method.
    """
    try:
        response = requests.post(
            rpc_url,
            json={"jsonrpc": "2.0", "id": 1, "method": "getSlot"},
            timeout=5
        )
        response.raise_for_status()
        return response.json().get("result")
    except requests.RequestException as e:
        logging.error(f"Error fetching slot from {rpc_url}: {e}")
        return None

def check_sync_status():
    """
    Check if the node is in sync with the reference node and notify if out of sync.
    """
    local_slot = get_slot(LOCAL_RPC_URL)
    reference_slot = get_slot(REFERENCE_RPC_URL)

    if local_slot is None or reference_slot is None:
        logging.warning("Unable to fetch slot data. Skipping sync check.")
        return

    slot_difference = reference_slot - local_slot
    logging.info(f"Local slot: {local_slot}, Reference slot: {reference_slot}, Difference: {slot_difference}")

    if slot_difference > SYNC_THRESHOLD:
        message = (
            f"⚠️ Node is out of sync!\n"
            f"Local slot: {local_slot}\n"
            f"Reference slot: {reference_slot}\n"
            f"Difference: {slot_difference} slots"
        )
        logging.warning(message)
        send_telegram_message(message)
    else:
        logging.info("Node is in sync.")

def main():
    """
    Main loop to periodically check sync status.
    """
    while True:
        try:
            check_sync_status()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user.")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
