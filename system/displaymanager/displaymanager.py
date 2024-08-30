import os
import ctypes
import tempfile
import threading
import tkinter as tk
from PIL import Image, ImageFilter, ImageTk
import pyautogui

def show_blurred_image(blurred_image):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)   
    root.attributes('-disabled', True)    # disable interactions with the underlying windows
    root.attributes('-transparentcolor', 'black')

    img_tk = ImageTk.PhotoImage(blurred_image)

    label = tk.Label(root, image=img_tk)
    label.pack(expand=True)

    root.mainloop()

class DisplayManager:

    def __init__(self) -> None:
        self.thread = None

    def change_desktop_background(self, image_path: str) -> bool:   
        path = os.path.abspath(image_path)
        
         # the parameter to change the wallpaper is 20
        SPI_SETDESKWALLPAPER = 20
        result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)

        return result != 0

    def blur_display(self) -> bool:

        try:
            screenshot = pyautogui.screenshot()
            image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())

            blurred_image = image.filter(ImageFilter.GaussianBlur(15))

            self.thread = threading.Thread(target=show_blurred_image, args=(blurred_image,), daemon=True)
            self.thread.start()

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


