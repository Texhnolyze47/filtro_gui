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


def filtro():
    ventAbrir = tk.Toplevel()
    ventAbrir.geometry("1000x400")
    ventAbrir.title("otra ventana")
    path_file = img_file[0]
    img = Image.open(path_file)
    tk_image = ImageTk.PhotoImage(img)
    label = tk.Label(ventAbrir, image=tk_image)
    label.pack()
    ventAbrir.mainloop()


def sobel_filter():
    r = np.matrix("1 2 1; 0 0 0; -1 -2 -1")
    a = read_img(img_file[0])
    b = np.zeros(a.shape[:3])
    a = cv.cvtColor(a, cv.COLOR_BGR2RGB)
    b[:, :, 0] = cv.filter2D(a[:, :, 0], -1, r)
    window = tk.Toplevel()

    pil_image = Image.fromarray(b[:, :, 0].astype(np.uint8))

    tk_image = ImageTk.PhotoImage(pil_image)

    label_image = tk.Label(window, image=tk_image)
    label_image.pack()

    window.mainloop()


if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.geometry("1300x650+20+0")
    ventana.minsize(600, 370)
    ventana.title("PDI: PROCESAMIENTO DIGITAL DE IMAGENES")
    barraMenu = tk.Menu(ventana)
    menuArchivo = tk.Menu(barraMenu)
    menuArchivo.add_command(label="Subir imagen", command=open_file_manager)
    menuArchivo.add_command(label="Imagenes precargadas", command=filtro)
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
    tk.Label(ventana, image=fondo).place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
    ventana.config(menu=barraMenu)
    ventana.mainloop()
