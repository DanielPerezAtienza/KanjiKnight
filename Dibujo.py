from tkinter import *

from PIL import Image,ImageTk,ImageDraw
from datetime import datetime
import PIL


app = Tk()
app.geometry("400x400")
altura=300
anchura=300
negro=(0,0,0)
blanco=(255, 255, 255)


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_smth(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y),
                      fill='black',
                      width=15)
    draw.line([lasx, lasy, event.x, event.y],
                      fill='black',
                      width=15)
    lasx, lasy = event.x, event.y



def guardar(event):
    # Guardamos las imagenes con el nombre, fecha y extensión (.jpg)
    print("Guardando la imagen...")
    fechayHora=datetime.now()
    extension=".jpg"
    dibujo = "Kanji "+fechayHora.strftime("%d-%m-%Y %Hh%Mm%Ss")+extension
    imagen.save(dibujo)
    print("Guardado completado.")

    #El modelo está entrenado con imágenes con formato 48x48 píxeles por lo que deberemos convertir la imagen a este tamaño
    fixed_height = 48
    image = Image.open(dibujo)
    height_percent = (fixed_height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))
    image = image.resize((width_size, fixed_height), PIL.Image.NEAREST)
    image.save(dibujo)
    print("Redimensión completada.")

    app.destroy()



canvas = Canvas(width=altura,height=anchura, bg='white')
canvas.pack(anchor='nw', fill='both', expand=1)

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)

buttonBG = canvas.create_rectangle(0, 0, 100, 30, fill="grey40", outline="grey60")
buttonTXT = canvas.create_text(50, 15, text="Guardar")
canvas.tag_bind(buttonBG, "<Button-1>", guardar) ## when the square is clicked runs function "clicked".
canvas.tag_bind(buttonTXT, "<Button-1>", guardar) ## same, but for the text.

imagen = Image.new("RGB", (400,400), blanco)
draw = ImageDraw.Draw(imagen)


""""
image = Image.open("dibujo1.jpg")
image = image.resize((400,400), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
canvas.create_image(0,0, image=image, anchor='nw')
"""
app.mainloop()

