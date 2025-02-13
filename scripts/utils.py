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
    # Check if you have a session file to load, if not, login using credentials
    try:
        instance.load_session_from_file(username, "cookies.txt")

    except FileNotFoundError:
        try:
            instance.login(username, password)
        except:
            # If login fails, load the session using sessionid and csrftoken (not recommended if you use VPN)
            instance.load_session(
                username,
                {"sessionid": session , "csrftoken": csrftoken },
            )

    # Save the session to a file for future use
    instance.save_session_to_file("cookies.txt")

    if instance.context.is_logged_in:
        print(f"Logged as {username}")
    else:
        print("An error occurred while logging into the account.")
