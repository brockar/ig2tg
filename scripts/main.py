import os
import time
import logging
from dotenv import load_dotenv
import instaloader

from utils import ig_login
from stories import download_stories_for_user

logger = logging.getLogger(__name__)

def prompt_for_username():
    """Prompt the user for an Instagram username or exit command."""
    return input("Enter the Instagram username to download stories (or 'exit' to quit): ").strip()

def wait_before_next_check(seconds=60):
    """Wait for a specified number of seconds, logging the reason."""
    logger.info(f"Waiting {seconds} seconds before next check to avoid hitting Instagram's rate limits.")
    time.sleep(seconds)

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

    while True:
        target_user = prompt_for_username()
        if target_user.lower() == "exit":
            logger.info("Exiting.")
            break
        if not target_user:
            logger.warning("You need to enter a username.")
            continue

        download_stories_for_user(target_user, instance)
        wait_before_next_check(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()