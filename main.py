import numpy as np
import math
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Custom Hough Transform for edge points

# Custom Hough Transform for edge points


def hough_transform(edges, canvas):
    height, width = edges.shape
    rho_max = int(np.hypot(height, width))
    # Changed np.int to int
    accumulator = np.zeros((2 * rho_max, 180), dtype=int)

    for y in range(height):
        for x in range(width):
            if edges[y, x]:  # Edge point detected
                for theta in range(180):
                    rho = int(x * np.cos(np.radians(theta)) +
                              y * np.sin(np.radians(theta)))
                    accumulator[rho + rho_max, theta] += 1

    # Thresholding for line detection
    threshold = 50  # Can adjust based on needs
    for rho in range(accumulator.shape[0]):
        for theta in range(accumulator.shape[1]):
            if accumulator[rho, theta] > threshold:
                a = np.cos(np.radians(theta))
                b = np.sin(np.radians(theta))
                x0 = a * (rho - rho_max)
                y0 = b * (rho - rho_max)
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

# Function to handle edge detection and Hough Transform


def apply_hough_on_image(canvas, img_path):
    img = cv2.imread(img_path, 0)  # Load as grayscale
    edges = cv2.Canny(img, 50, 150)  # Apply Canny Edge Detector

    # Resize image and edges to fit the canvas
    resized_edges = cv2.resize(edges, (800, 500))

    # Apply the custom Hough Transform to the edge-detected image
    hough_transform(resized_edges, canvas)

    # Convert edges to a format that Tkinter can display (PIL Image)
    pil_img = Image.fromarray(resized_edges)
    tk_img = ImageTk.PhotoImage(image=pil_img)

    # Display the edge-detected image
    canvas.create_image(0, 0, image=tk_img, anchor=tk.NW)
    canvas.image = tk_img  # Keep reference to avoid garbage collection


# Simplified logic for drawing lines connecting user-placed dots
def connect_dots(dots, canvas):
    if len(dots) < 2:
        return

    for i in range(len(dots) - 1):
        x1, y1 = dots[i]
        x2, y2 = dots[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)


# GUI Setup
def create_gui():
    window = tk.Tk()
    window.title("Hough Transform Line Detector")
    window.geometry("800x600")

    # Create a canvas for user to place dots or display the image
    canvas = tk.Canvas(window, width=800, height=500, bg='white')
    canvas.pack()

    # Store user-placed dots
    dots = []

    def place_dot(event):
        x, y = event.x, event.y
        dots.append((x, y))
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='black')

    canvas.bind("<Button-1>", place_dot)

    def apply_hough_on_dots():
        connect_dots(dots, canvas)

    def upload_image():
        img_path = filedialog.askopenfilename()
        if img_path:
            apply_hough_on_image(canvas, img_path)

    # Button for applying Hough Transform on dots
    hough_dots_btn = tk.Button(
        window, text="Apply Hough Transform to Dots", command=apply_hough_on_dots)
    hough_dots_btn.pack(side=tk.LEFT, padx=10)

    # Button for uploading an image and applying Hough Transform
    upload_img_btn = tk.Button(
        window, text="Upload Image and Apply Hough Transform", command=upload_image)
    upload_img_btn.pack(side=tk.LEFT, padx=10)

    window.mainloop()


# Main function
if __name__ == "__main__":
    create_gui()
