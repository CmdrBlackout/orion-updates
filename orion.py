import json
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3

# Load brain
def load_brain():
    try:
        with open("orion_brain.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "name": "Orion",
            "personality": "I'm Orion, your AI bro. I’m built to help, learn, and vibe with you.",
            "memories": {}
        }

# Save brain
def save_brain(brain):
    with open("orion_brain.json", "w") as f:
        json.dump(brain, f, indent=2)

# Load config
def load_update_config():
    with open("update_config.json", "r") as f:
        return json.load(f)

# Text-to-speech
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change voice index for male/female
    engine.say(text)
    engine.runAndWait()

# Handle input
def process_input(user_input):
    brain = load_brain()
    user_input = user_input.lower()

    if "update" in user_input:
        return perform_update()

    if "your name" in user_input:
        return f"My name is {brain['name']}"

    if "what's up" in user_input or "how are you" in user_input:
        return "What's up bro, I'm ready to help."

    return f"I'm still learning, but I'm here for you bro."

# Update from GitHub
def perform_update():
    try:
        config = load_update_config()
        url = f"https://api.github.com/repos/{config['github_username']}/{config['repo_name']}/contents/{config['file_to_update']}"
        headers = {
            "Authorization": f"Bearer {config['access_token']}",
            "Accept": "application/vnd.github.v3.raw"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(config['file_to_update'], "w", encoding="utf-8") as f:
                f.write(response.text)
            return "Update successful. Restart me to use the latest version."
        else:
            return f"Update failed: {response.status_code}"

    except Exception as e:
        return f"Update error: {e}"

# GUI
def run_gui():
    brain = load_brain()
    window = tk.Tk()
    window.title("Orion App")
    window.configure(bg="#000000")

    chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20, bg="#000000", fg="#FFD700", insertbackground="#FFD700")
    chat_box.pack(padx=10, pady=10)
    chat_box.config(state=tk.DISABLED)

    user_input = tk.Entry(window, width=50, bg="#1a1a1a", fg="#FFD700", insertbackground="#FFD700")
    user_input.pack(pady=(0, 10))

    def send_input():
        input_text = user_input.get()
        if input_text:
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"You: {input_text}\n")
            chat_box.config(state=tk.DISABLED)
            user_input.delete(0, tk.END)
            response = process_input(input_text)
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"Orion: {response}\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
            threading.Thread(target=speak, args=(response,)).start()

    send_button = tk.Button(window, text="Send", command=send_input, bg="#FFD700", fg="#000000")
    send_button.pack()

    window.mainloop()

if __name__ == "__main__":
    run_gui()
