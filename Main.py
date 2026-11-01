import sys
import os
import pygame
from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QSlider
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from pynput import keyboard

pygame.mixer.init()

MASTER_VOLUME = 0.8

class DrumPad(QPushButton):
    def __init__(self, pad_number, parent=None):
        super().__init__("Pad " + str(pad_number), parent)
        self.pad_number = pad_number
        self.sound_file = None
        self.setAcceptDrops(True)
        self.setFixedSize(180, 180)
        self.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: 4px solid #555555;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
                border: 4px solid #777777;
            }
            QPushButton:pressed {
                background-color: #00ffcc;
                border: 4px solid #ffffff;
                color: black;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            path = files[0]
            if path.lower().endswith(('.wav', '.mp3', '.ogg')):
                self.sound_file = path
                print(f"Loaded: {path} onto Pad {self.pad_number}")
                self.setText(os.path.basename(path))
            else:
                print("Unsupported file type. Please drop a .wav, .mp3, or .ogg file.")

    def play_sound(self):
        if self.sound_file:
            try:
                sound = pygame.mixer.Sound(self.sound_file)
                sound.set_volume(MASTER_VOLUME)
                sound.play()
                self.setDown(True)
                QTimer.singleShot(100, lambda: self.setDown(False))   
            except Exception as e:
                print(f"Error playing sound: {e}")
        else:
            print(f"No sound loaded for pad {self.pad_number} please drop a sound file onto the pad.")

    def mousePressEvent(self, event):
        self.play_sound()
        super().mousePressEvent(event)


class DrumMachine(QWidget):
    pad_triggered = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InstroSoft - Drum Machine")
        self.setFixedSize(600, 750)
        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.pads = []
        for row in range(3):
            for col in range(3):
                pad_num = row * 3 + col + 1
                pad = DrumPad(pad_num)
                self.grid_layout.addWidget(pad, row, col)
                self.pads.append(pad)
        self.main_layout.addLayout(self.grid_layout)
        self.pad_triggered.connect(self.trigger_pad)
        self.volume_layout = QHBoxLayout()
        self.volume_layout.addWidget(QPushButton("Volume"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(int(MASTER_VOLUME * 100))
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.update_volume)
        self.volume_layout.addWidget(self.volume_slider)
        self.main_layout.addLayout(self.volume_layout)       
        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.start_keyboard_listener()

    def update_volume(self):
        global MASTER_VOLUME
        MASTER_VOLUME = self.volume_slider.value() / 100.0
        print(f"Master Volume: {MASTER_VOLUME}")

    def trigger_pad(self, index):
        self.pads[index].play_sound()

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                key_text = str(key)
                if "num_1" in key_text: self.pad_triggered.emit(0)
                elif "num_2" in key_text: self.pad_triggered.emit(1)
                elif "num_3" in key_text: self.pad_triggered.emit(2)
                elif "num_4" in key_text: self.pad_triggered.emit(3)
                elif "num_5" in key_text: self.pad_triggered.emit(4)
                elif "num_6" in key_text: self.pad_triggered.emit(5)
                elif "num_7" in key_text: self.pad_triggered.emit(6)
                elif "num_8" in key_text: self.pad_triggered.emit(7)
                elif "num_9" in key_text: self.pad_triggered.emit(8)
                elif hasattr(key, 'char') and key.char in "123456789":
                    index = int(key.char) - 1
                    if 0 <= index <= 8:
                        self.pad_triggered.emit(index)
            except Exception as e:
                print(f"Keyboard error: {e}")
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(12)
    app.setFont(font)
    window = DrumMachine()
    window.show()
    sys.exit(app.exec())