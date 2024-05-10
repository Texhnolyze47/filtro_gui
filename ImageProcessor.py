from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import tkinter as tk
import cv2 as cv
import numpy as np
import pytesseract
import skimage.feature
from PIL import ImageTk, Image


def read_img(path_image):
    input_image = cv.imread(path_image)
    if input_image is None:
        messagebox.showerror("Error", "Archivo no encontrado")
        return None
    input_image = cv.cvtColor(input_image, cv.COLOR_BGR2RGB)
    return input_image


def convert_pil_image(original_image_array):
    # Comprueba las dimensiones de un array
    if original_image_array.ndim == 2:
        original_pil_image = Image.fromarray(original_image_array)
    else:
        original_pil_image = Image.fromarray(original_image_array.astype(np.uint8))
    original_tk_image = ImageTk.PhotoImage(original_pil_image)
    return original_tk_image


def convert_filtered_image(filtered_image_array):
    if filtered_image_array.ndim == 2:
        generic_image = Image.fromarray(np.uint8(filtered_image_array))
    else:
        generic_image = Image.fromarray(filtered_image_array[:, :, 0].astype(np.uint8))

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


class ImageProcessor:
    def __init__(self):
        self.img_files = []

    def open_file_manager(self):
        file = askopenfilename(filetypes=(
            ("File jpg", "*.jpg"),
            ("File png", "*.png")))
        if file:
            try:
                if self.img_files:
                    self.img_files[0] = file
                else:
                    self.img_files.append(file)
            except IndexError:
                messagebox.showerror("Error", "No hay archivo cargado")

    def load_image(self):
        window = tk.Toplevel()
        window.geometry("1000x400")
        window.title("Imagen cargada")
        path_file = ""
        try:
            path_file = self.img_files[0]
        except IndexError:
            messagebox.showerror("Error", "No hay un archivo pre cargado")
        img = Image.open(path_file)
        tk_image = ImageTk.PhotoImage(img)
        # TODO: fix - Expected type '_Image | str', got 'PhotoImage' instead
        label = tk.Label(window, image=tk_image)

        label.pack()
        window.mainloop()

    def get_image(self):
        try:
            return read_img(self.img_files[0])
        except IndexError:
            messagebox.showerror("Error", "No hay un archivo cargado")
            return None

    def sobel_filter(self):
        img = self.get_image()

        if img is None:
            return

        r = np.matrix("1 2 1; 0 0 0; -1 -2 -1")
        b = np.zeros(img.shape[:3])
        b[:, :, 0] = cv.filter2D(img[:, :, 0], -1, r)

        display_compare_window(img, b, "sobel_filter")

    def laplacian_filter(self):
        img = self.get_image()

        if img is None:
            return

        # Aplicar el filtro Laplaciano
        laplacian = cv.Laplacian(img, cv.CV_64F)

        display_compare_window(img, laplacian, "Laplacian_filter")

    def roberts_filter(self):
        img = self.get_image()

        if img is None:
            return

        # Convertir la imagen a escala de grises
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        roberts_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=1)
        roberts_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=1)
        roberts = np.hypot(roberts_x, roberts_y)

        display_compare_window(img, np.uint8(roberts), "robers_filter")

    def high_pass_filter(self):
        img = self.get_image()

        if img is None:
            return

        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        kernel = np.matrix("-1 -1 -1; -1 8 -1; -1 -1 -1")
        high_pass = cv.filter2D(gray, -1, kernel)

        display_compare_window(img, high_pass, "High Pass Filter")

    def low_pass_filter(self):
        img = self.get_image()

        if img is None:
            return

        # Aplicar el filtro de paso bajo
        kernel = np.ones((5, 5), np.float32) / 25
        low_pass = cv.filter2D(img, -1, kernel)

        display_compare_window(img, low_pass, "Low Pass Filter")

    def edge_enhancement(self):
        img = self.get_image()

        if img is None:
            return

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        edges = skimage.feature.canny(
            image=gray,
            sigma=3,
            low_threshold=0.0,
            high_threshold=5.0
        )

        edges = edges * 255

        display_compare_window(img, edges, "edge-enhancement")

    def ocr(self):
        img = self.get_image()

        if img is None:
            return

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        threshold_img = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        text = pytesseract.image_to_string(threshold_img)

        if text == "":
            text = "No se pudo reconocer ningun texto"

        messagebox.showinfo("Mesaje", text)
