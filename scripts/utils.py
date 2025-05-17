import os
    
def delete_files_with_specific_extensions(folder_path, extensions):
    for root_folder, _, files in os.walk(folder_path):
        for file in files:
            file_extension = file.split(".")[-1]
            if file_extension in extensions:
                file_path = os.path.join(root_folder, file)
                try:
                    os.remove(file_path)
                    print(f"{file_path} deleted.")
                except Exception as e:
                    print(f"Error occurred while deleting {file_path}: {e}")

# Try to login using the credentials, if it fails, load the session using sessionid and csrftoken
def ig_login(instance, username, password, session, csrftoken):
    if not password and (not session or not csrftoken):
        print("Missing Instagram credentials. Please check your .env file for IG_USERNAME, IG_PASSWORD, IGSESSIONID, and IGCSRFTOKEN.")
        return False
    try:
        instance.load_session_from_file(username, "cookies.txt")
    except FileNotFoundError:
        print("cookies.txt not found, trying other login methods.")
        if password:
            print("Trying to login with username and password.")
            try:
                instance.login(username, password)
            except Exception as e:
                # Handle 2FA
                if "two-factor authentication required" in str(e).lower():
                    print("Two-factor authentication required.")
                    two_factor_code = input("Enter your 2FA code: ")
                    try:
                        instance.two_factor_login(two_factor_code)
                        print("2FA login successful.")
                    except Exception as e2:
                        print(f"2FA login failed: {e2}")
                        return False
                else:
                    print(f"Login failed with username and password: {e}")
                    return False
        else:
            print("Trying to login with sessionid and csrftoken.")
            try:
                instance.load_session(
                    username,
                    {"sessionid": session, "csrftoken": csrftoken},
                )
            except Exception as e:
                print(f"Login failed with sessionid and csrftoken: {e}")
                return False

    if instance.context.is_logged_in:
        instance.save_session_to_file("cookies.txt")
        print(f"Logged in as {username}")
        return instance
    else:
        print("Login failed: Not actually logged in after attempts.")
        return False