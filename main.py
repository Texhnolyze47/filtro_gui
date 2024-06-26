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

    medianMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="median-filter", menu=medianMenu)
    medianMenu.add_command(label="mediana", command=image_processor.median_filter)
    medianMenu.add_command(label="gaussian_filter", command=image_processor.gaussian_filter)

    ffMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="Realce-deteccion de border", menu=ffMenu)
    ffMenu.add_command(label="Derivada", command=image_processor.derivative)
    ffMenu.add_command(label="Canny", command=image_processor.canny)

    ocrMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="OCR", menu=ocrMenu)
    ocrMenu.add_command(label="OCR", command=image_processor.ocr)

    sharpMenu = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="sharp",menu=sharpMenu)
    sharpMenu.add_command(label="sharp", command=image_processor.sharp)

    fourier = tk.Menu(barraMenu)
    barraMenu.add_cascade(label="fourier", menu=fourier)
    fourier.add_command(label="DFT", command=image_processor.dft)

    fondo = tk.PhotoImage(file="./assets/background_image.gif")
    tk.Label(root, image=fondo).place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

    root.config(menu=barraMenu)
    root.mainloop()
