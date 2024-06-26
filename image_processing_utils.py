import cv2 as cv
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np
import tkinter as tk


def read_img(path_image):
    input_image = cv.imread(path_image)
    if input_image is None:
        messagebox.showerror("Error", "Archivo no encontrado")
        return None
    input_image = cv.cvtColor(input_image, cv.COLOR_BGR2RGB)
    return input_image


def resize_image(image_array, target_size=(500, 500)):
    """Redimensiona la imagen manteniendo la relación de aspecto."""
    h, w = image_array.shape[:2]
    scale = min(target_size[0] / h, target_size[1] / w)
    new_size = (int(w * scale), int(h * scale))
    resized_image = cv.resize(image_array, new_size, interpolation=cv.INTER_AREA)
    return resized_image

def convert_pil_image(original_image_array):
    # Comprueba las dimensiones de un array
    resized_image_array = resize_image(original_image_array)
    if original_image_array.ndim == 2:
        original_pil_image = Image.fromarray(resized_image_array)
    else:
        original_pil_image = Image.fromarray(resized_image_array.astype(np.uint8))
    original_tk_image = ImageTk.PhotoImage(original_pil_image)
    return original_tk_image


def convert_filtered_image(filtered_image_array):
    resized_image_array = resize_image(filtered_image_array)

    if filtered_image_array.ndim == 2:
        generic_image = Image.fromarray(np.uint8(resized_image_array))
    else:
        generic_image = Image.fromarray(resized_image_array[:, :, 0].astype(np.uint8))

    filtred_tk_image = ImageTk.PhotoImage(generic_image)
    return filtred_tk_image


def display_compare_window(original_image, filtered_image, filter_name):
    window = tk.Toplevel()
    window.title(filter_name)

    original_image = convert_pil_image(original_image_array=original_image)

    orignal_label_image = tk.Label(window, image=original_image)
    orignal_label_image.pack(side=tk.LEFT)

    filtered_image = convert_filtered_image(filtered_image_array=filtered_image)

    filtered_label_image = tk.Label(window, image=filtered_image)
    filtered_label_image.pack(side=tk.RIGHT)

    window.mainloop()


