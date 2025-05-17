import instaloader
from urllib3 import exceptions
from retrying import retry
import requests
import os

def download_stories_for_user(target_user, instance):
    if not target_user:
        print("You need to enter a username.")
        return

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