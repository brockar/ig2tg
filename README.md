# IG2TG: Instagram Stories to Telegram

**IG2TG** is a Python tool that automatically downloads Instagram stories from a specified user and sends updates to your Telegram chat. It leverages [Instaloader](https://instaloader.github.io/) for Instagram scraping and [python-telegram-bot](https://python-telegram-bot.org/) for Telegram integration.

## Features

- Download Instagram stories from any public or followed private account.
- Automatically cleans up unnecessary files after download.
- Designed for easy integration with Telegram bots to send story updates to your chat.

## Requirements

- Python 3.7+
- Instagram account credentials or session cookies
- Telegram Bot Token

Install dependencies with:

```bash
pip install -r requirements.txt
```
## Setup

1. **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd ig2tg
    ```

2. **Configure environment variables:**

    Copy the example environment file and fill in your credentials:

    ```bash
    cp env.example .env
    ```

    Edit `.env` and set:
    - `IG_USERNAME` and `IG_PASSWORD` (or `IGSESSIONID` and `IGCSRFTOKEN` for session login)
    - `TELEGRAM_TOKEN` (your Telegram bot token)

    The script uses environment variables for authentication. Here’s how to get each one:
    - **IG_USERNAME**: Your Instagram username (email or handle).
    - **IG_PASSWORD**: Your Instagram password.
    - **IGSESSIONID** and **IGCSRFTOKEN**:  
    If you prefer not to use your password, you can log in to Instagram in your browser, open the Developer Tools, and copy these cookies from your session:
    1. Go to [instagram.com](https://instagram.com) and log in.
    2. Open Developer Tools (F12 or right-click → Inspect).
    3. Go to the "Application" tab, then "Cookies".
    4. Copy the values for `sessionid` (set as `IGSESSIONID`) and `csrftoken` (set as `IGCSRFTOKEN`).

3. **Run the script:**

    ```bash
    python scripts/stories.py
    ```

    You will be prompted to enter the Instagram username whose stories you want to download.

## Sending Stories to Telegram

To send downloaded stories to your Telegram chat, extend the script using the `python-telegram-bot` library. You can use the `TELEGRAM_TOKEN` from your `.env` file to authenticate your bot and send media files to your chat.

## License

This project is licensed under the [GNU GPLv3](LICENSE).

---

**Note:** Use this tool responsibly and respect Instagram's terms of service.
