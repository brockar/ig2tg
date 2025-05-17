import os
import time
from dotenv import load_dotenv
import instaloader

from utils import ig_login
from stories import download_stories_for_user

def main():
    # Load environment variables
    load_dotenv(override=True)
    username = os.getenv("IG_USERNAME")
    password = os.getenv("IG_PASSWORD")
    session = os.getenv("IGSESSIONID")
    csrftoken = os.getenv("IGCSRFTOKEN")

    # Create Instaloader instance
    instance = instaloader.Instaloader()
    instance.compress_json = False
    instance.dirname_pattern = os.path.join("stories", "{target}")

    # Login
    instance = ig_login(instance, username, password, session, csrftoken)
    if not instance:
        print("Login failed. Exiting.")
        return

    while True:
        target_user = input("Enter the Instagram username to download stories (or 'exit' to quit): ").strip()
        if target_user.lower() == "exit":
            print("Exiting.")
            break
        if not target_user:
            print("You need to enter a username.")
            continue

        download_stories_for_user(target_user, instance)
        print("Waiting 60 seconds before next check...")
        print("This is to avoid hitting Instagram's rate limits.")
        time.sleep(60)

if __name__ == "__main__":
    main()