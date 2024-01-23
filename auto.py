import random
import time
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

api_id = "29399077"
api_hash = "b5e06d82909a68906f85cd59f3e7144d"

# Replace "session_name" with a unique session name for your account
app = Client("session_name", api_id=api_id, api_hash=api_hash)

# Dictionary to store the autotyping status for each group
autotype_status = {}

# List of random sentences to be sent
random_sentences = [
    "Hello, how are you?",
    "What's up?",
    "This is a random sentence.",
    "Python is awesome!",
    "Greetings from your bot.",
    "Have a great day!",
    # Add more sentences as needed
]

# The filter has been updated to include both private chats and groups
@app.on_message(filters.command(["autotype", "stop"]))
def autotype_command(client, message: Message):
    try:
        chat_id = message.chat.id

        if message.command[0] == "autotype":
            # Extract the interval from the command
            interval = int(message.command[1]) if len(message.command) > 1 else 10

            # Validate the interval to be between 3 and 100 seconds
            interval = max(3, min(interval, 100))

            # Store autotyping status for the current group
            autotype_status[chat_id] = {"interval": interval, "running": True}

            # Send random sentences at the specified interval
            while autotype_status[chat_id]["running"]:
                for sentence in random_sentences:
                    client.send_message(chat_id, sentence)
                    time.sleep(interval)

        elif message.command[0] == "stop":
            # If the command is /stop, stop the autotyping process for the current group
            if chat_id in autotype_status:
                autotype_status[chat_id]["running"] = False
                client.send_message(chat_id, "Autotyping stopped.")

    except Exception as e:
        print(f"Error processing command: {e}")
        client.send_message(chat_id, "Error processing command.")

if __name__ == "__main__":
    app.run()
