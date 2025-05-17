import instaloader
from urllib3 import exceptions
from retrying import retry
import requests
import os
from dotenv import load_dotenv
from utils import ig_login


load_dotenv(override=True)
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")
session = os.getenv("IGSESSIONID")
csrftoken = os.getenv("IGCSRFTOKEN")

instance = instaloader.Instaloader()
instance.compress_json = False

# Set the download directory for stories
instance.dirname_pattern = os.path.join("stories", "{target}")

instance = ig_login(instance, username, password, session, csrftoken)
if not instance:
    print("Login failed. Exiting.")
    exit(1)

target_user = input("Enter any user you want: ")
if not target_user:
    print("You need to enter a username.")
    exit(1)

print("The account you are looking for is being searched in Instagram..")

try:
    profile = instaloader.Profile.from_username(instance.context, target_user)
    try:
        if profile and profile.has_viewable_story:
            print("Account found. Downloading stories.. ")
            for story in instance.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    # Download the story item
                    instance.download_storyitem(item, target_user)
                    story_dir = os.path.join("stories", target_user)
                    # Find the file just downloaded (by date string in filename)
                    date_str = item.date_local.strftime("%Y-%m-%d_%H-%M-%S_UTC")
                    for ext in [".mp4", ".jpg"]:
                        original_name = f"{date_str}{ext}"
                        original_path = os.path.join(story_dir, original_name)
                        if os.path.exists(original_path):
                            new_name = f"{target_user}-{original_name}"
                            new_path = os.path.join(story_dir, new_name)
                            os.rename(original_path, new_path)
                            print(f"Renamed {original_name} to {new_name}")
            print("The download process has been completed.")

            # Delete unwanted files for stories (diferent)
            story_dir = os.path.join("stories", target_user)
            for root, dirs, files in os.walk(story_dir):
                for file in files:
                    if file.endswith((".xz", ".txt", ".json")):
                        os.remove(os.path.join(root, file))
                        print(f"Deleting: {file}")

        elif profile and not profile.has_viewable_story:
            print(
                "There are no viewable story in the account you are looking for."
            )
    except KeyError as e:
        print(f"Error: Missing expected data in Instagram response: {e}")
        print("This may be due to login/session issues or Instagram API changes.")
except exceptions.ConnectTimeoutError:
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=5,
    )
    def make_api_request():
        response = requests.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target_user}"
        )
        response.raise_for_status()
        return response.json()
    try:
        data = make_api_request()
    except Exception as e:
        print(f"Error: {e}")
except instaloader.exceptions.PrivateProfileNotFollowedException:
    print(
        "This is a private account. You need to follow it to access it's stories."
    )
except instaloader.exceptions.ProfileNotExistsException:
    print(
        "The account you are looking for is not exists on instagram. Try another username"
    )
