from pynput import keyboard
import pygame
import string
import threading
import time

# Initialize Pygame mixer
pygame.mixer.init()

sound_queue = []
is_playing = False

def play_next_sound():
    global is_playing
    if sound_queue:
        is_playing = True
        file_name = sound_queue.pop(0)
        try:
            pygame.mixer.music.load(file_name)
            print('playing ', file_name)
            pygame.mixer.music.play()
        except pygame.error:
            print(f"File {file_name} not found. Skipping.")
            play_next_sound()
    else:
        is_playing = False

def on_press(key):
    global is_playing
    try:
        char = key.char.lower()
        if char in string.ascii_lowercase + string.digits:
            file_name = f"{char}.wav"
            print(file_name)
            sound_queue.append(file_name)
            if not is_playing:
                play_next_sound()
    except AttributeError:
        pass  # ignore special keys

# Background thread to check if music finished
def music_checker():
    global is_playing
    while True:
        if is_playing and not pygame.mixer.music.get_busy():
            play_next_sound()
        time.sleep(0.05)  # 50ms delay

# Start key listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start music checking thread
thread = threading.Thread(target=music_checker, daemon=True)
thread.start()

# Keep main thread alive
listener.join()
