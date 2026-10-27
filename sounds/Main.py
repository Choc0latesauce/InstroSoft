import pygame
from pynput import keyboard
import os

pygame.mixer.init()

sound_map = {
    '1': "sounds/kick.mp3",
    '2': "sounds/snare.mp3",
    '3': "sounds/hihat.mp3"
}

def play_sound(key_input):
    if key_input in sound_map:
        try:
            sound = pygame.mixer.Sound(sound_map[key_input])
            sound.play()
            print(f"Playing: {sound_map[key_input]}")
        except Exception as e:
            print(f"Error playing sound: {e}")

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = key
    play_sound(k)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()