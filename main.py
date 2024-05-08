import cv2 as cv
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import numpy as np
from PIL import ImageTk, Image

img_file = []


def read_img(path_image):
    try:
        file_image = cv.imread(path_image)
    except IndexError:
        messagebox.showerror("Error", "No hay un archivo cargado")
    file_image = cv.cvtColor(file_image, cv.COLOR_BGR2RGB)
    return file_image


def open_file_manager():
    archivo = askopenfilename(filetypes=(
        ("File jpg", "*.jpg"),
        ("File png", "*.png")))
    if archivo:
        try:
            if img_file:
                img_file[0] = archivo
            else:
                img_file.append(archivo)
        except IndexError:
            messagebox.showerror("Error", "No hay un archivo cargado")


def load_image():
    window = tk.Toplevel()
    window.geometry("1000x400")
    window.title("Imagen cargada")
    path_file = ""
    try:
        path_file = img_file[0]
    except IndexError:
        messagebox.showerror("Error", "No hay un archivo pre cargado")
    img = Image.open(path_file)
    tk_image = ImageTk.PhotoImage(img)
    # TODO: fix - Expected type '_Image | str', got 'PhotoImage' instead
    label = tk.Label(window, image=tk_image)
    label.pack()
    window.mainloop()


def sobel_filter():
    window = tk.Toplevel()
    window.title("Filtro sobel")

    r = np.matrix("1 2 1; 0 0 0; -1 -2 -1")
    a = ""
    try:
        a = read_img(img_file[0])
    except IndexError:
        messagebox.showerror("Error", "No hay un archivo cargado")
    b = np.zeros(a.shape[:3])
    b[:, :, 0] = cv.filter2D(a[:, :, 0], -1, r)

    original_pil_image = Image.fromarray(a.astype(np.uint8))
    original_tk_image = ImageTk.PhotoImage(original_pil_image)

    orignal_label_image = tk.Label(window, image=original_tk_image)
    orignal_label_image.pack(side=tk.LEFT)

    filtred_pil_image = Image.fromarray(b[:, :, 0].astype(np.uint8))
    filtred_tk_image = ImageTk.PhotoImage(filtred_pil_image)

    filtered_label_image = tk.Label(window, image=filtred_tk_image)
    filtered_label_image.pack(side=tk.RIGHT)

    window.mainloop()


def laplacian_filter():
    window = tk.Toplevel()
    window.title("Filtro Laplaciano")

    try:
        img = read_img(img_file[0])
    except IndexError:
        messagebox.showerror("Error", "No hay un archivo cargado")
        return

    # Aplicar el filtro Laplaciano
    laplacian = cv.Laplacian(img, cv.CV_64F)

    original_pil_image = Image.fromarray(img.astype(np.uint8))
    original_tk_image = ImageTk.PhotoImage(original_pil_image)

    orignal_label_image = tk.Label(window, image=original_tk_image)
    orignal_label_image.pack(side=tk.LEFT)

    # Convertir la imagen procesada a formato PIL para mostrarla en Tkinter
    laplacian_pil_image = Image.fromarray(laplacian.astype(np.uint8))
    laplacian_tk_image = ImageTk.PhotoImage(laplacian_pil_image)

    # Crear una etiqueta para mostrar la imagen
    laplacian_label_image = tk.Label(window, image=laplacian_tk_image)
    laplacian_label_image.pack(side=tk.RIGHT)



    window.mainloop()


def roberts_filter():
    window = tk.Toplevel()
    window.title("Filtro Roberts")

    try:
        img = read_img(img_file[0])
    except IndexError:
        messagebox.showerror("Error", "No hay un archivo cargado")
        return

    # Convertir la imagen a escala de grises
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    roberts_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=1)
    roberts_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=1)
    roberts = np.hypot(roberts_x, roberts_y)

    original_pil_image = Image.fromarray(img)
    original_tk_image = ImageTk.PhotoImage(original_pil_image)

    orignal_label_image = tk.Label(window, image=original_tk_image)
    orignal_label_image.pack(side=tk.LEFT)

    roberts_pil_image = Image.fromarray(np.uint8(roberts))
    roberts_tk_image = ImageTk.PhotoImage(roberts_pil_image)

    roberts_label_image = tk.Label(window, image=roberts_tk_image)
    roberts_label_image.pack(side=tk.RIGHT)

    window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1300x650+20+0")
    root.minsize(600, 370)
    root.title("PDI: PROCESAMIENTO DIGITAL DE IMAGENES")

    root.columnconfigure((0, 1), weight=1, uniform="a")
    barraMenu = tk.Menu(root)
    menuArchivo = tk.Menu(barraMenu)
    menuArchivo.add_command(label="Subir imagen", command=open_file_manager)
    menuArchivo.add_command(label="Imagenes precargadas", command=load_image)
    menuArchivo.add_separator()
    menuArchivo.add_command(label="Exit")
    barraMenu.add_cascade(label="Imagenes", menu=menuArchivo)

    feMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="Filtro Espacial", menu=feMenu)
    feMenu.add_command(label="Sobel", command=sobel_filter)
    feMenu.add_command(label="Laplaciano")
    feMenu.add_command(label="roberts")

    ffMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="Filtro Frecuencia", menu=ffMenu)
    ffMenu.add_command(label="Paso Alto")
    ffMenu.add_command(label="Paso Bajo")
    ffMenu.add_command(label="Realce y Deteccion de Bordes")

    fondo = tk.PhotoImage(file="./assets/background_image.gif")
    tk.Label(root, image=fondo).place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
    root.config(menu=barraMenu)
    root.mainloop()
