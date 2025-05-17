import os
import logging

logger = logging.getLogger(__name__)

def delete_files_with_specific_extensions(folder_path, extensions):
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

def ig_login(instance, username, password, session, csrftoken):
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