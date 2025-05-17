import os
import asyncio
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv(override=True)
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_USER = os.getenv("TG_USER")  # Can be username (str) or user ID (int)
STORIES_DIR = "stories"
CHAT_ID_FILE = "chat_id.txt"

async def send_image(context, chat_id, file_path):
    with open(file_path, "rb") as image:
        await context.bot.send_photo(chat_id=chat_id, photo=image)
        print(f"Sent {file_path} to Telegram.")

async def send_all_images(context, chat_id):
    sent = False
    for root, _, files in os.walk(STORIES_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".mp4")):
                file_path = os.path.join(root, file)
                await send_image(context, chat_id, file_path)
                sent = True
    if sent:
        await context.bot.send_message(chat_id=chat_id, text="All images sent.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="No images found.")

class ImageHandler(FileSystemEventHandler):
    def __init__(self, context, chat_id, loop):
        self.context = context
        self.chat_id = chat_id
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith((".jpg", ".png", ".mp4")):
            # Wait until file is stable (size doesn't change for 0.5s)
            stable = False
            last_size = -1
            while not stable:
                try:
                    size = os.path.getsize(event.src_path)
                    if size == last_size:
                        stable = True
                    else:
                        last_size = size
                        time.sleep(0.5)
                except FileNotFoundError:
                    time.sleep(0.1)
            asyncio.run_coroutine_threadsafe(
                send_image(self.context, self.chat_id, event.src_path),
                self.loop
            )

def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))

def load_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            return int(f.read().strip())
    return None

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    # Save chat_id for future use
    save_chat_id(chat_id)
    # Check if TG_USER is username or user ID
    if (str(user.id) == TG_USER) or (user.username and user.username.lower() == TG_USER.lower()):
        await context.bot.send_message(chat_id=chat_id, text="Hello, I received your message! Sending all images...")
        await send_all_images(context, chat_id)
        if not context.application.bot_data.get("observer_started"):
            loop = asyncio.get_running_loop()
            event_handler = ImageHandler(context, chat_id, loop)
            observer = Observer()
            observer.schedule(event_handler, STORIES_DIR, recursive=True)
            observer.start()
            context.application.bot_data["observer_started"] = True
            await context.bot.send_message(chat_id=chat_id, text="Now watching for new images.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Sorry, you are not authorized to use this bot.")

def main():
    if not TG_TOKEN or TG_TOKEN.strip() == "":
        print("Error: TELEGRAM_TOKEN is missing or empty in your .env file.")
        return
    print("Telegram bot is starting...")  # Print to terminal when bot starts
    app = Application.builder().token(TG_TOKEN).build()
    chat_id = load_chat_id()
    if chat_id:
        # Start observer immediately if chat_id is known
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        event_handler = ImageHandler(app, chat_id, loop)
        observer = Observer()
        observer.schedule(event_handler, STORIES_DIR, recursive=True)
        observer.start()
        app.bot_data["observer_started"] = True
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))
    app.run_polling()

if __name__ == "__main__":
    main()