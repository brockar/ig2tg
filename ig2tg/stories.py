import instaloader
from urllib3 import exceptions
from retrying import retry
import requests
import os
import logging
from utils import delete_files_with_specific_extensions

logger = logging.getLogger(__name__)

def download_stories_for_user(target_user, instance):
    if not target_user:
        logger.warning("You need to enter a username.")
        return

    logger.info("The account you are looking for is being searched in Instagram..")

    try:
        profile = instaloader.Profile.from_username(instance.context, target_user)
        try:
            if profile and profile.has_viewable_story:
                logger.info("Account found. Downloading stories.. ")
                for story in instance.get_stories(userids=[profile.userid]):
                    for item in story.get_items():
                        # Download the story item
                        instance.download_storyitem(item, target_user)
                logger.info("The download process has been completed.")

                # Delete unwanted files for stories (diferent)
                story_dir = os.path.join("stories", target_user)
                cleanup_story_files(story_dir)

            elif profile and not profile.has_viewable_story:
                logger.info(
                    "There are no viewable stories in the account you are looking for."
                )
        except KeyError as e:
            logger.exception("Error: Missing expected data in Instagram response")
            logger.error("This may be due to login/session issues or Instagram API changes.")
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
            logger.error(f"Error: {e}")
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        logger.warning(
            "This is a private account. You need to follow it to access its stories."
        )
    except instaloader.exceptions.ProfileNotExistsException:
        logger.warning(
            "The account you are looking for does not exist on Instagram. Try another username."
        )

def cleanup_story_files(story_dir: str):
    delete_files_with_specific_extensions(story_dir, ["xz", "txt", "json"])