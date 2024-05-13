from tkinter.filedialog import askopenfilename

import numpy as np
import pytesseract
import skimage.feature
from image_processing_utils import *


class ImageProcessor:
    """
    A class
    """
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

    def median_filter(self):
        img = self.get_image()

        if img is None:
            return

        copy_image = np.zeros(img.shape[:3], np.uint8)

        b = np.zeros(9, np.uint8)

        n = img.shape[0]
        m = img.shape[1]

        for g in range(3):
            for i in range(1, n - 1):
                for j in range(1, m - 1):
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            b[3 * (k + 1) + l + 1] = img[i + k, j + l, g]

                    b.sort()
                    copy_image[i, j, g] = int(b[5])
        display_compare_window(original_image=img, filtered_image=copy_image, filter_name="Mediana")


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

    def gaussian_blur(self):
        img = self.get_image()

        if img is None:
            return

        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

        noise_gaussian = np.zeros((gray.shape[0], img.shape[1]), dtype="uint8")

        cv.randn(noise_gaussian, 32, 16)
        img_noise = cv.add(gray, noise_gaussian)

        display_compare_window(img,img_noise,"gaussian")

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
