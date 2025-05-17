import os
import logging

# Logging setup at the very top
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import instaloader

from utils import ig_login, load_user_list, wait_before_next_check
from stories import download_stories_for_user

def main():
    """Main entry point for the IG2TG story downloader."""
    load_dotenv(override=True)
    username = os.getenv("IG_USERNAME")
    password = os.getenv("IG_PASSWORD")
    session = os.getenv("IGSESSIONID")
    csrftoken = os.getenv("IGCSRFTOKEN")

    instance = instaloader.Instaloader()
    instance.compress_json = False
    instance.dirname_pattern = os.path.join("stories", "{target}")

    instance = ig_login(instance, username, password, session, csrftoken)
    if not instance:
        logger.error("Login failed. Exiting.")
        return

    users = load_user_list("user_list.txt")
    if not users:
        logger.info("No users found in user_list.txt. Please add at least one username and restart the script.")
        return

    while True:
        for target_user in users:
            logger.info(f"Checking stories for user: {target_user}")
            try:
                download_stories_for_user(target_user, instance)
            except Exception as e:
                logger.error(f"Error processing user '{target_user}': {e}", exc_info=True)
        wait_before_next_check(86400)  # Wait 1 day

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user. Exiting gracefully.")