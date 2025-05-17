# IG2TG: Instagram Stories to Telegram Automation

**IG2TG** is a Python package and CLI tool that automatically downloads Instagram stories from specified users and sends them to your Telegram chat.  
It leverages [Instaloader](https://instaloader.github.io/) for Instagram scraping and [python-telegram-bot](https://python-telegram-bot.org/) for Telegram integration.

---

## Features

- Download Instagram stories from any public or followed private account.
- Automatically cleans up unnecessary files after download.
- Sends new stories to your Telegram chat via a bot.
- Easy configuration with environment variables.

---

## Requirements

- Python 3.7+
- Instagram account credentials or session cookies
- Telegram Bot Token
- Instagram accounts to download stories.

---

## Installation

Install dependencies (for development or direct use):

```bash
pip install -r requirements.txt
```

Or, if you want to install as a package (after building):

```bash
pip install .
```

---

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/brockar/ig2tg.git
    cd ig2tg
    ```

2. **Configure environment variables:**

    Copy the example environment file and fill in your credentials:

    ```bash
    cp env.example .env
    ```

    Edit `.env` and set:
    - `IG_USERNAME` and `IG_PASSWORD` (or `IGSESSIONID` and `IGCSRFTOKEN` for session login) (works with 2FAs)
    - `TELEGRAM_TOKEN` (your Telegram bot token) and `TG_USER` to just send images to your telegram user.

    **How to get Instagram session cookies:**
    1. Go to [instagram.com](https://instagram.com) and log in.
    2. Open Developer Tools (F12 or right-click → Inspect).
    3. Go to the "Application" tab, then "Cookies".
    4. Copy the values for `sessionid` (set as `IGSESSIONID`) and `csrftoken` (set as `IGCSRFTOKEN`).

3. **Add Instagram usernames to monitor:**

    Create a file named `user_list.txt` in the project root and add one Instagram username per line (no `@`):

    ```
    testuser1
    testuser2
    ```

    Also can add comments with `#`

---

## Usage

### As a CLI tool (recommended)

After installing as a package, run:

```bash
ig2tg
```

### As a Python script

You can also run the main script directly:

```bash
python -m ig2tg.main
```

The tool will:
- Log in to Instagram using your credentials or session.
- Download stories for each user in `user_list.txt`.
- Clean up unnecessary files.
- Send new stories to your Telegram chat.
- Repeat the process every 24 hours.

---

## Running from a GitHub Release

1. **Download the latest built package**

   Go to the [Releases](https://github.com/brockar/ig2tg/releases) page and download either:
   - `ig2tg-0.0.1-py3-none-any.whl` (wheel)
   - or `ig2tg-0.0.1.tar.gz` (source distribution)

2. **Install the package**

   Replace `<filename>` with the name of the file you downloaded:

   ```bash
   pip install <filename>
   ```

   For example:

   ```bash
   pip install ig2tg-0.0.1-py3-none-any.whl
   # or
   pip install ig2tg-0.0.1.tar.gz
   ```

3. **Run the tool**

   After installation, you can run the CLI:

   ```bash
   ig2tg
   ```

   Or as a Python module:

   ```bash
   python -m ig2tg.main
   ```

---

## Telegram Integration

- The Telegram bot will send all new stories to the chat where you first interact with it.
- Only the user specified in your `.env` as `TG_USER` can trigger the bot.

---

## Project Structure

```
ig2tg/
    __init__.py
    main.py
    stories.py
    tg.py
    utils.py
stories/
    <downloaded stories organized by user>
user_list.txt
.env
README.md
pyproject.toml
LICENSE
```

---

## License

This project is licensed under the [GNU GPLv3](LICENSE).

---

**Note:**  
Use this tool responsibly and respect Instagram's and Telegram's terms of service.
