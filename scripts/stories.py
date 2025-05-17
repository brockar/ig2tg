from urllib3 import exceptions
from retrying import retry
import instaloader
import requests
import os
from utils import ig_login

instance = instaloader.Instaloader()

username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")
session = os.getenv("IGSESSIONID")
csrftoken = os.getenv("IGCSRFTOKEN")

instance.compress_json = False

ig_login(instance, username, password, session, csrftoken)

# target_user = input("Enter any user you want: ")
target_user = 'mnrfich'
print("The account you are looking for is being searched in Instagram's database..")

try:
    profile = instaloader.Profile.from_username(instance.context, target_user)
    try:
        if profile and profile.has_viewable_story:
            print("Account found. Downloading stories.. ")
            for story in instance.get_stories(profile.user):
                for item in story.get_items():
                    instance.download_storyitem(item, ":stories")
            print("The download process has been completed.")

            # Delete unwanted files for stories (diferent)
            for root, dirs, files in os.walk(target_user):
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
