import os
import logging
import time
from typing import List, Optional, Any

logger = logging.getLogger(__name__)

def delete_files_with_specific_extensions(folder_path: str, extensions: List[str]) -> None:
    for root_folder, _, files in os.walk(folder_path):
        for file in files:
            file_extension = file.split(".")[-1]
            if file_extension in extensions:
                file_path = os.path.join(root_folder, file)
                try:
                    os.remove(file_path)
                    logger.info(f"{file_path} deleted.")
                except Exception as e:
                    logger.error(f"Error occurred while deleting {file_path}: {e}")

def ig_login(
    instance: Any,
    username: str,
    password: Optional[str],
    session: Optional[str],
    csrftoken: Optional[str]
) -> Optional[Any]:
    """
    Attempt to login to Instagram using credentials or session cookies.
    Returns the logged-in instance or False if login fails.
    """
    if not password and (not session or not csrftoken):
        logger.error("Missing Instagram credentials. Please check your .env file for IG_USERNAME, IG_PASSWORD, IGSESSIONID, and IGCSRFTOKEN.")
        return False

    # Try loading session from file
    try:
        instance.load_session_from_file(username, "cookies.txt")
        logger.info("Loaded session from cookies.txt.")
    except FileNotFoundError:
        logger.warning("cookies.txt not found, trying other login methods.")
        # Try username/password login
        if password:
            logger.info("Trying to login with username and password.")
            try:
                instance.login(username, password)
            except Exception as e:
                # Handle 2FA
                if "two-factor authentication required" in str(e).lower():
                    logger.warning("Two-factor authentication required.")
                    two_factor_code = input("Enter your 2FA code: ")
                    try:
                        instance.two_factor_login(two_factor_code)
                        logger.info("2FA login successful.")
                    except Exception as e2:
                        logger.error(f"2FA login failed: {e2}")
                        return False
                else:
                    logger.error(f"Login failed with username and password: {e}")
                    return False
        else:
            # Try sessionid/csrftoken login
            logger.info("Trying to login with sessionid and csrftoken.")
            try:
                instance.load_session(
                    username,
                    {"sessionid": session, "csrftoken": csrftoken},
                )
            except Exception as e:
                logger.error(f"Login failed with sessionid and csrftoken: {e}")
                return False

    if getattr(instance.context, "is_logged_in", False):
        instance.save_session_to_file("cookies.txt")
        logger.info(f"Logged in as {username}")
        return instance
    else:
        logger.error("Login failed: Not actually logged in after attempts.")
        return False

def load_user_list(filename: str = "user_list.txt") -> List[str]:
    """Load a list of Instagram usernames from a file (one per line). If file doesn't exist, create it."""
    if not os.path.exists(filename):
        logger.warning(f"User list file '{filename}' not found. Creating an empty one.")
        with open(filename, "w") as f:
            f.write("# Add one Instagram username per line\n")
        return []
    with open(filename, "r") as f:
        users = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]
    return users

def wait_before_next_check(seconds: int = 86400) -> None:
    """Wait for a specified number of seconds (default: 1 day)."""
    hours = seconds // 3600
    logger.info(f"Waiting {hours} hour{'s' if hours != 1 else ''} before next check to avoid hitting Instagram's rate limits.")
    time.sleep(seconds)

def delete_old_files(folder_path: str, days: int = 2) -> None:
    """Delete files older than `days` in the given folder (recursively), and remove empty folders."""
    now = time.time()
    cutoff = now - days * 86400  # 86400 seconds in a day
    # First, delete old files
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getmtime(file_path) < cutoff:
                    os.remove(file_path)
                    logger.info(f"Deleted old file: {file_path}")
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")
    # Then, remove empty directories (bottom-up)
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    logger.info(f"Deleted empty folder: {dir_path}")
            except Exception as e:
                logger.error(f"Error deleting folder {dir_path}: {e}")