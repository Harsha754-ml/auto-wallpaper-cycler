# copy the exact script you were given earlier; here's the same one for convenience
import os
import random
import time
import threading
import ctypes
from tkinter import Tk, Button, Label, filedialog, StringVar

SPI_SETDESKWALLPAPER = 20

def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)

class WallpaperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Wallpaper Cycler")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        self.folder_path = StringVar()
        self.running = False

        Label(root, text="Select folder with wallpapers:", font=("Segoe UI", 10)).pack(pady=10)
        Button(root, text="Browse", command=self.select_folder, width=15).pack()

        self.status = Label(root, text="No folder selected.", fg="gray", font=("Segoe UI", 9))
        self.status.pack(pady=10)

        self.start_button = Button(root, text="Start", command=self.start_cycle, width=15, bg="#d1ffd1")
        self.start_button.pack(pady=5)

        self.stop_button = Button(root, text="Stop", command=self.stop_cycle, width=15, bg="#ffd1d1")
        self.stop_button.pack(pady=5)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Wallpaper Folder")
        if folder:
            self.folder_path.set(folder)
            self.status.config(text=f"Selected: {folder}", fg="black")

    def start_cycle(self):
        if not self.folder_path.get():
            self.status.config(text="Please select a folder first!", fg="red")
            return

        if not self.running:
            self.running = True
            self.status.config(text="Cycling wallpapers...", fg="green")
            threading.Thread(target=self.cycle_wallpapers, daemon=True).start()

    def stop_cycle(self):
        self.running = False
        self.status.config(text="Stopped.", fg="gray")

    def cycle_wallpapers(self):
        folder = self.folder_path.get()
        images = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

        if not images:
            self.status.config(text="No image files found in folder!", fg="red")
            self.running = False
            return

        while self.running:
            image = random.choice(images)
            full_path = os.path.join(folder, image)
            try:
                set_wallpaper(full_path)
                self.status.config(text=f"Wallpaper set: {image}", fg="green")
            except Exception as e:
                self.status.config(text=f"Error: {e}", fg="red")
            time.sleep(30)

if __name__ == "__main__":
    root = Tk()
    app = WallpaperApp(root)
    root.mainloop()
