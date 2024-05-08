import tkinter as tk
from ImageProcessor import ImageProcessor

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1300x650+20+0")
    root.minsize(600, 370)
    root.title("PDI: PROCESAMIENTO DIGITAL DE IMAGENES")

    image_processor = ImageProcessor()

    root.columnconfigure((0, 1), weight=1, uniform="a")
    barraMenu = tk.Menu(root)
    menuArchivo = tk.Menu(barraMenu)
    menuArchivo.add_command(label="Subir imagen", command=image_processor.open_file_manager)
    menuArchivo.add_command(label="Imagenes precargadas", command=image_processor.load_image)
    menuArchivo.add_separator()
    menuArchivo.add_command(label="Exit")
    barraMenu.add_cascade(label="Imagenes", menu=menuArchivo)

    feMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="Filtro Espacial", menu=feMenu)
    feMenu.add_command(label="Sobel", command=image_processor.sobel_filter)
    feMenu.add_command(label="Laplaciano", command=image_processor.laplacian_filter)
    feMenu.add_command(label="roberts", command=image_processor.roberts_filter)

    ffMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="Filtro Frecuencia", menu=ffMenu)
    ffMenu.add_command(label="Paso Alto")
    ffMenu.add_command(label="Paso Bajo")
    ffMenu.add_command(label="Realce y Deteccion de Bordes")

    fondo = tk.PhotoImage(file="./assets/background_image.gif")
    tk.Label(root, image=fondo).place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
    root.config(menu=barraMenu)
    root.mainloop()
