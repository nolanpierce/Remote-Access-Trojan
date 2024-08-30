import os
import ctypes
import tempfile
import threading
import tkinter as tk
from PIL import Image, ImageFilter, ImageTk
import pyautogui

# Define the standalone function to handle the Tkinter window
def show_blurred_image(blurred_image):
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make the window fullscreen
    root.attributes('-topmost', True)     # Keep the window on top
    root.attributes('-disabled', True)    # Disable interactions with the underlying windows
    root.attributes('-transparentcolor', 'black')  # Handle transparency (if needed)

    # Convert the blurred image to a format compatible with Tkinter
    img_tk = ImageTk.PhotoImage(blurred_image)

    # Create a label to hold the image
    label = tk.Label(root, image=img_tk)
    label.pack(expand=True)

    # Start the Tkinter main loop
    root.mainloop()

class DisplayManager:

    def __init__(self) -> None:
        self.thread = None

    def change_desktop_background(self, image_path: str) -> bool:   
        if not image_path:
            return False  # Failed to input path to image
    
        try:
            path = os.path.abspath(image_path)
            # SPI_SETDESKWALLPAPER is the parameter to change the wallpaper
            SPI_SETDESKWALLPAPER = 20
            result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
            return result != 0
        except Exception:
            return False

    def blur_display(self) -> bool:
        try:
            # Take a screenshot
            screenshot = pyautogui.screenshot()
            image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())

            # Apply blur
            blurred_image = image.filter(ImageFilter.GaussianBlur(15))

            # Start the Tkinter window in a new thread
            self.thread = threading.Thread(target=show_blurred_image, args=(blurred_image,), daemon=True)
            self.thread.start()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


