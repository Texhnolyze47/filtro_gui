from tkinter.filedialog import askopenfilename

import numpy as np
import pytesseract
import skimage.feature
from image_processing_utils import *


class ImageProcessor:

    def __init__(self):
        """
        Constructor que se encarga de crear una instancia ImageProcessor y de inicializar la lista de imagenes img_files
        """
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

    def select_image(self):
        img = self.get_image()

        if img is None:
            return

        return img

    def sobel_filter(self):
        img = self.select_image()

        r = np.matrix("1 2 1; 0 0 0; -1 -2 -1")
        b = np.zeros(img.shape[:3])
        b[:, :, 0] = cv.filter2D(img[:, :, 0], -1, r)

        display_compare_window(img, b, "sobel_filter")

    def laplacian_filter(self):
        # Aplicar el filtro Laplaciano
        laplacian = cv.Laplacian(self.select_image(), cv.CV_64F)

        display_compare_window(self.select_image(), laplacian, "Laplacian_filter")

    def derivative(self):
        img = self.select_image()

        copy_image = np.zeros(img.shape[:3], np.uint8)

        r1 = np.matrix("1,1,1;0,0,0;-1,-1,-1")

        for i in range(3):
            a = img[:, :, i]
            a = cv.filter2D(a, -1, r1)
            copy_image[:, :, i] = a

        display_compare_window(img, copy_image, "derivative")

    def median_filter(self):
        img = self.select_image()

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

    def canny(self):

        gray = cv.cvtColor(self.select_image(), cv.COLOR_BGR2GRAY)

        edges = skimage.feature.canny(
            image=gray,
            sigma=3,
            low_threshold=0.0,
            high_threshold=5.0
        )

        edges = edges * 255

        display_compare_window(self.select_image(), edges, "edge-enhancement")

    def sharp(self):
        img = self.select_image()

        filtered_image = np.zeros(img.shape[:3], np.uint8)

        r1 = np.matrix("-1,-1,-1;-1,9,-1;-1,-1,-1")

        for i in range(3):
            filtered_image[:, :, i] = cv.filter2D(img[:, :, i], -1, r1)

        display_compare_window(img, filtered_image, "mejora")

    def gaussian_blur(self):
        img = self.select_image()

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        noise_gaussian = np.zeros((gray.shape[0], img.shape[1]), dtype="uint8")

        cv.randn(noise_gaussian, 32, 16)
        img_noise = cv.add(gray, noise_gaussian)

        display_compare_window(img, img_noise, "gaussian")

    def gaussian_filter(self):
        img = self.select_image()

        copy_image = np.zeros(img.shape[:3], np.uint8)

        r1 = np.matrix("1,2,1;2,4,2;1,2,1") / 16

        for i in range(3):
            a = img[:, :, i]
            a = cv.filter2D(a, -1, r1)
            copy_image[:, :, i] = a
        display_compare_window(img, copy_image, "gaussian_filter")

    def ocr(self):
        img = self.select_image()

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        threshold_img = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        text = pytesseract.image_to_string(threshold_img)

        if text == "":
            text = "No se pudo reconocer ningun texto"

        messagebox.showinfo("Mesaje", text)

    def dft(self):
        img = self.select_image()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                m = ((i - (gray.shape[0] / 2)) ** 2 + (j - (gray.shape[1] / 2)) ** 2) ** 0.5
                if m < 50:
                    gray[i, j] = 1
        dft_image = np.fft.fft2(gray)
        dft_image = np.fft.fftshift(dft_image)
        magnitude_spectrum = np.abs(dft_image)
        magnitude_spectrum = np.log(1 + magnitude_spectrum)
        magnitude_spectrum = cv.normalize(magnitude_spectrum, None, 0, 255, cv.NORM_MINMAX)
        display_compare_window(gray, magnitude_spectrum, "DFT")






