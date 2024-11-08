import cv2
import easyocr
import pyautogui
from PIL import Image
import numpy as np
import time
import mss
import torch

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=True)
print(torch.cuda.is_available())

# Function to capture the screen quickly using mss
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        image = np.array(screenshot)
        # Save the captured screen
        cv2.imwrite("captured_screen.png", cv2.cvtColor(image, cv2.COLOR_BGRA2BGR))
        return image

# Function to search for specific text in an image
def search_for_text(image, search_text):
    # Convert to grayscale for better OCR accuracy
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use EasyOCR to extract text data from the image
    results = reader.readtext(gray_image)

    for (bbox, text, prob) in results:
        if search_text.lower() in text.lower():
            # Get bounding box coordinates
            (top_left, top_right, bottom_right, bottom_left) = bbox
            x, y = int(top_left[0]), int(top_left[1])
            w, h = int(bottom_right[0] - top_left[0]), int(bottom_right[1] - top_left[1])
            return x, y, w, h
    return None

# Function to move the mouse pointer to the specified coordinates
def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=0.1)

# Main function to capture the screen, search for text, and move the mouse
def main():
    time.sleep(1)  # Adding shorter delay for preparation

    # Step 1: Capture screen
    image = capture_screen()

    # Step 2: Search for specific characters/text
    search_text = "GPU"  # Change this to the text you want to find
    coordinates = search_for_text(image, search_text)

    if coordinates:
        x, y, w, h = coordinates

        # Step 3: Move mouse pointer to the center of the found text
        move_mouse(x + w // 2, y + h // 2)
        print(f"Moved mouse to the text '{search_text}' at ({x + w // 2}, {y + h // 2})")
    else:
        print(f"Text '{search_text}' not found on screen.")

    search_text = "search_for_text"  # Change this to the text you want to find
    coordinates = search_for_text(image, search_text)

    if coordinates:
        x, y, w, h = coordinates

        # Step 3: Move mouse pointer to the center of the found text
        move_mouse(x + w // 2, y + h // 2)
        print(f"Moved mouse to the text '{search_text}' at ({x + w // 2}, {y + h // 2})")
    else:
        print(f"Text '{search_text}' not found on screen.")

if __name__ == "__main__":
    main()
