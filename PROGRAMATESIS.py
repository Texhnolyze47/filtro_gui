import cv2
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import matplotlib.pyplot as plt

archivo = ""
def abrirImagen():
    archivo = askopenfilename(filetypes=(("Template files", "*.tplate"),
                                          ("HTML files", "*.html;*.htm"),
                                          ("All files", "*.*")))

    if archivo:
        try:
            a = cv2.imread(archivo)
            plt.imshow(cv2.cvtColor(a,cv2.COLOR_BGR2RGB))
            plt.show()
        except:
            showerror("error al carga la imagen")



def filtro():
    ventAbrir=Tk()
    ventAbrir.geometry("1000x400+100+100")
    ventAbrir.title("otra ventana")
def filtro1():
    print("filtro 1")


ventana = Tk()
ventana.geometry("1300x650+20+0")
ventana.minsize(600, 370)
ventana.title("PDI: PROCESAMIENTO DIGITAL DE IMAGENES")
barraMenu = Menu(ventana)
menuArchivo = Menu(barraMenu)
menuArchivo.add_command(label="Subir imagen", command=abrirImagen)
menuArchivo.add_command(label="Imagenes precargadas", command = filtro)
menuArchivo.add_separator()
menuArchivo.add_command(label="Exit")
barraMenu.add_cascade(label= "Imagenes",menu=menuArchivo)

feMenu = Menu(barraMenu)
barraMenu.add_cascade(label="Filtro Espacial", menu=feMenu)
feMenu.add_command(label="Sobel",command=filtro1)
feMenu.add_command(label="Laplaciano")
feMenu.add_command(label="roberts")

ffMenu = Menu(barraMenu)
barraMenu.add_cascade(label="Filtro Frecuencia", menu=ffMenu)
ffMenu.add_command(label="Paso Alto")
ffMenu.add_command(label="Paso Bajo")
ffMenu.add_command(label="Realce y Deteccion de Bordes")

fondo=PhotoImage(file="./assets/background_image.gif")
lblFondo = Label(ventana, image= fondo) .place(x=0, y=0)
ventana.config(menu=barraMenu)
ventana.mainloop()

