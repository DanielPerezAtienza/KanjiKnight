import pygame
import random
from pygame import mixer


pygame.init()

clock = pygame.time.Clock()
fps = 60

# Dimensiones de la pantalla del juego
interfaz = 150
ancho = 800
alto = 466 + interfaz

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Kanji Knight')

mixer.init()
mixer.music.load('recursos/Musica/battle.mp3')
mixer.music.play()

# Variables del juego
combatientes_actuales = 1
combatientes_totales = 3
enfriamiento_accion = 0
tiempo_espera_accion = 90
atacar = False
ataque_caballero = False
pocion = False
efecto_pocion = 15
clicked = False
derrota = 0

# Fuente de letra
font = pygame.font.SysFont('Times New Roman', 26)

# Colores
rojo = (255, 0, 0)
verde = (0, 255, 0)

# Listas vacias para la comparación de posiciones en ataque del caballero
posicionSignificado = list("")
posicionKanji = list("")


# Cargar la imagen del fondo
imagen_fondo = pygame.image.load('recursos/Fondo/fondo.png').convert_alpha()
# Cargar la imagen de la interfaz
imagen_interfaz = pygame.image.load('recursos/Interfaz/interfaz.png').convert_alpha()
# Cargar imagen de botones
imagen_pocion = pygame.image.load('recursos/Interfaz/pocion.png').convert_alpha()
imagen_reiniciar = pygame.image.load('recursos/Interfaz/reintentar.png').convert_alpha()
# Cargar imagenes de victoria y derrota
imagen_victoria = pygame.image.load('recursos/Interfaz/victoria.png').convert_alpha()
imagen_derrota = pygame.image.load('recursos/Interfaz/derrota.png').convert_alpha()
# Cargar imagen de la espada
imagen_raton = pygame.image.load('recursos/Interfaz/espada.png').convert_alpha()


def dibujar():
    import random
    from tkinter import Tk, Canvas

    from PIL import Image, ImageDraw
    from datetime import datetime
    import PIL
    import os
    from InformacionKanji import info

    app = Tk()
    app.geometry("400x400")
    # app.eval('tk::PlaceWindow . center')
    altura = 300
    anchura = 300
    blanco = (255, 255, 255)

    def get_x_and_y(event):
        global lasx, lasy
        lasx, lasy = event.x, event.y

    def draw_smth(event):
        global lasx, lasy
        canvas.create_line((lasx, lasy, event.x, event.y),
                           fill='black',
                           width=30)
        draw.line([lasx, lasy, event.x, event.y],
                  fill='black',
                  width=30)
        lasx, lasy = event.x, event.y

    def guardar(event):
        # Guardamos las imagenes con el nombre, fecha y extensión (.jpg)
        print("Guardando la imagen...")
        ruta = "recursos/Kanjis/"
        fechayHora = datetime.now()
        extension = ".jpg"
        dibujo = "Kanji " + fechayHora.strftime("%d-%m-%Y %Hh%Mm%Ss") + extension
        rutaKanji = os.path.join(ruta, dibujo)
        imagen.save(rutaKanji)
        print("Guardado completado.")

        # El modelo está entrenado con imágenes con formato 48x48 píxeles por lo que deberemos convertir la imagen a este tamaño
        fijar_altura = 48
        image = Image.open(rutaKanji)
        height_percent = (fijar_altura / float(image.size[1]))
        width_size = int((float(image.size[0]) * float(height_percent)))
        image = image.resize((width_size, fijar_altura), PIL.Image.Resampling.NEAREST)
        image.save(rutaKanji)
        print("Redimensión completada.")

        #app.quit()

    def borrar(event):
        # Borrar el lienzo
        canvas.delete("all")
        # Poner sobre el lienzo un cuadrado blanco
        draw.rectangle((0, 0, 400, 400), fill="white")

        buttonBG = canvas.create_rectangle(0, 0, 200, 30, fill="red", outline="grey60")
        buttonTXT = canvas.create_text(100, 15, text="Borrar")
        canvas.tag_bind(buttonBG, "<Button-1>", borrar)
        canvas.tag_bind(buttonTXT, "<Button-1>", borrar)

        buttonBG2 = canvas.create_rectangle(200, 0, 400, 30, fill="green", outline="grey60")
        buttonTXT2 = canvas.create_text(300, 15, text="Aceptar")
        canvas.tag_bind(buttonBG2, "<Button-1>", guardar)
        canvas.tag_bind(buttonTXT2, "<Button-1>", guardar)

        TXT1Rectangulo = canvas.create_rectangle(400, 60, 0, 30, fill="yellow", outline="grey60")
        TXT1 = canvas.create_text(200, 45, text=kanji)

    canvas = Canvas(width=altura, height=anchura, bg='white')
    canvas.pack(anchor='nw', fill='both', expand=1)

    canvas.bind("<Button-1>", get_x_and_y)
    canvas.bind("<B1-Motion>", draw_smth)

    # Botón para borrar el lienzo
    buttonBG = canvas.create_rectangle(0, 0, 200, 30, fill="red", outline="grey60")
    buttonTXT = canvas.create_text(100, 15, text="Borrar")
    canvas.tag_bind(buttonBG, "<Button-1>", borrar)
    canvas.tag_bind(buttonTXT, "<Button-1>", borrar)

    # Botón para guardar dibujo en el lienzo
    buttonBG2 = canvas.create_rectangle(200, 0, 400, 30, fill="green", outline="grey60")
    buttonTXT2 = canvas.create_text(300, 15, text="Aceptar")
    canvas.tag_bind(buttonBG2, "<Button-1>", guardar)
    canvas.tag_bind(buttonTXT2, "<Button-1>", guardar)

    aleatorio = random.randint(0, 29)
    kanji = info[aleatorio]
    #print(info.index(kanji))
    posicionSignificado.append(info.index(kanji))
    #print("La posicion del significado es: ", posicionSignificado)

    # Cuadro con información sobre el kanji que dibujar
    TXT1Rectangulo = canvas.create_rectangle(400, 60, 0, 30, fill="yellow", outline="grey60")
    TXT1 = canvas.create_text(200, 45, text=kanji)

    imagen = Image.new("RGB", (400, 400), blanco)
    draw = ImageDraw.Draw(imagen)

    app.mainloop()

# Función para hacer una predicción constratando con el modelo que entrenamos
def comparar():

    from kanjijapanese import label
    from tensorflow.keras.models import load_model

    import numpy as np
    from keras.utils import CustomObjectScope
    from keras.initializers import glorot_uniform

    from numpy import asarray
    from PIL import Image
    import glob
    import os

    # cargar última imagen creada en la carpeta de Kanjis
    folder_path = r'recursos/Kanjis'
    file_type = r'\*.jpg'
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    img = Image.open(max_file)

    # conversión de imagen a escala de grises
    img = img.convert(mode='L')

    # Conversión a array de numpy
    data = asarray(img)
    data = data.reshape((1, 48, 48, 1))
    #print(data.shape)

    # cargar el modelo que entrenamos
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model('kanji.h5')

    # hacer predicciones en cuanto al modelo
    prediction = model.predict(data)
    # print(prediction)
    # contrastar la posición de la predicción con un diccionario que creamos (kanjijapanese)
    char = label[np.argmax(prediction)]
    print("Caracter detectado: ", char)

    posicionKanji.append(label.index(label[np.argmax(prediction)]))
    # print("La posición del kanji escrito es: ", posicionKanji)



# Establecer texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    pantalla.blit(img, (x, y))


# Establecer fondo
def draw_bg():
    pantalla.blit(imagen_fondo, (0, 0))


# Establecer interfaz
def draw_panel():
    # Establecer el rectángulo de la interfaz
    pantalla.blit(imagen_interfaz, (0, alto - interfaz))
    # Mostrar estadísticas de los caballeros
    draw_text(f'{Caballero.name} HP: {Caballero.hp}', font, rojo, 100, alto - interfaz + 10)
    for count, i in enumerate(lista_enemigos):
        # Mostrar nombre y vida
        draw_text(f'{i.name} HP: {i.hp}', font, rojo, 550, (alto - interfaz + 10) + count * 60)


# Clase combatiente
class Combatiente():
    def __init__(self, x, y, name, max_hp, strength, pociones):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_pociones = pociones
        self.pociones = pociones
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:estático, 1:atacar, 2:herir, 3:morir
        self.update_time = pygame.time.get_ticks()
        # Cargar imagen estática
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'recursos/{self.name}/Estatico/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # cargar imagen de atacar
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'recursos/{self.name}/Atacar/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # cargar imagen de herir
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'recursos/{self.name}/Herido/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # cargar imagen de morir
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'recursos/{self.name}/Muerte/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        enfriamiento_animacion = 100
        # Actualizar imagen
        self.image = self.animation_list[self.action][self.frame_index]
        # comprobar tiempo pasado desde la actualizacion
        if pygame.time.get_ticks() - self.update_time > enfriamiento_animacion:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Resetear animación al acabar
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # Animación a estático
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def ataque_caballero(self, objetivo):
        dibujar()
        comparar()

        if posicionKanji[-1] == posicionSignificado[-1]:
            # Hacer daño al enemigo
            print("Kanji correcto.")
            rand = random.randint(-5, 5)
            daño = self.strength + rand
            objetivo.hp -= daño
            # Animación de herido del enemigo
            objetivo.hurt()
            # Comprobar si el enemigo ha muerto
            if objetivo.hp < 1:
                objetivo.hp = 0
                objetivo.alive = False
                objetivo.death()
            texto_daño = TextoDaño(objetivo.rect.centerx, objetivo.rect.y, str(daño), rojo)
            texto_daño_grupo.add(texto_daño)
            # Variables de animacion de atacar
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        else:
            # Hacer daño al enemigo
            print("Kanji incorrecto.")
            rand = random.randint(0, 1)
            daño = self.strength * 0 + rand
            objetivo.hp -= daño
            # Animación de herido del enemigo
            objetivo.hurt()
            # Comprobar si el enemigo ha muerto
            if objetivo.hp < 1:
                objetivo.hp = 0
                objetivo.alive = False
                objetivo.death()
            texto_daño = TextoDaño(objetivo.rect.centerx, objetivo.rect.y, str(daño), rojo)
            texto_daño_grupo.add(texto_daño)
            # Variables de animacion de atacar
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def atacar(self, objetivo):
        # Hacer daño al enemigo
        rand = random.randint(-5, 5)
        daño = self.strength + rand
        objetivo.hp -= daño
        # Animación de herido del enemigo
        objetivo.hurt()
        # Comprobar si el enemigo ha muerto
        if objetivo.hp < 1:
            objetivo.hp = 0
            objetivo.alive = False
            objetivo.death()
        texto_daño = TextoDaño(objetivo.rect.centerx, objetivo.rect.y, str(daño), rojo)
        texto_daño_grupo.add(texto_daño)
        # Variables de animacion de atacar
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # Variables de animación de herir
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # Variables de animación de muerte
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.pociones = self.start_pociones
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        pantalla.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # actualizar la vida
        self.hp = hp
        # calcular ratio de vida
        ratio = self.hp / self.max_hp
        pygame.draw.rect(pantalla, rojo, (self.x, self.y, 150, 20))
        pygame.draw.rect(pantalla, verde, (self.x, self.y, 150 * ratio, 20))


class TextoDaño(pygame.sprite.Sprite):
    def __init__(self, x, y, daño, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(daño, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # texto de daño ascendente
        self.rect.y -= 1
        # borrar el texto después de unos segundos
        self.counter += 1
        if self.counter > 30:
            self.kill()


class Button():
    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        action = False

        # obtener posición del ratón
        pos = pygame.mouse.get_pos()

        # comprobar hover y condiciones de clicado
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # establecer botón
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


texto_daño_grupo = pygame.sprite.Group()

Caballero = Combatiente(200, 370, 'Caballero', 40, 10, 3)
Enemigo1 = Combatiente(600, 370, 'Enemigo', 15, 6, 1)
Enemigo2 = Combatiente(700, 370, 'Enemigo', 15, 6, 1)

lista_enemigos = []
lista_enemigos.append(Enemigo1)
lista_enemigos.append(Enemigo2)

Caballero_health_bar = HealthBar(100, alto - interfaz + 40, Caballero.hp, Caballero.max_hp)
Enemigo1_health_bar = HealthBar(550, alto - interfaz + 40, Enemigo1.hp, Enemigo1.max_hp)
Enemigo2_health_bar = HealthBar(550, alto - interfaz + 100, Enemigo2.hp, Enemigo2.max_hp)

# Crear botones pocion y reintentar
boton_pocion = Button(pantalla, 100, alto - interfaz + 70, imagen_pocion, 64, 64)
boton_reintentar = Button(pantalla, 330, 250, imagen_reiniciar, 80, 80)


run = True
while run:

    clock.tick(fps)

    # establecer fondo
    draw_bg()

    # establecer interfaz
    draw_panel()
    Caballero_health_bar.draw(Caballero.hp)
    Enemigo1_health_bar.draw(Enemigo1.hp)
    Enemigo2_health_bar.draw(Enemigo2.hp)

    # establecer combatientes
    Caballero.update()
    Caballero.draw()
    for Enemigo in lista_enemigos:
        Enemigo.update()
        Enemigo.draw()

    # texto con daño
    texto_daño_grupo.update()
    texto_daño_grupo.draw(pantalla)

    # acciones de control de jugador
    # resetear variables de acciones
    atacar = False
    ataque_caballero = False
    pocion = False
    objetivo = None
    # raton visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, Enemigo in enumerate(lista_enemigos):
        if Enemigo.rect.collidepoint(pos):
            # ocultar ratón
            pygame.mouse.set_visible(False)
            # mostrar espada en lugar del ratón
            pantalla.blit(imagen_raton, pos)
            if clicked == True and Enemigo.alive == True:
                ataque_caballero = True
                objetivo = lista_enemigos[count]
    if boton_pocion.draw():
        pocion = True
    # mostrar número de pociones restantes
    draw_text(str(Caballero.pociones), font, rojo, 150, alto - interfaz + 70)

    if derrota == 0:
        # accion del jugador
        if Caballero.alive == True:
            if combatientes_actuales == 1:
                enfriamiento_accion += 1
                if enfriamiento_accion >= tiempo_espera_accion:
                    # atacar
                    if ataque_caballero == True and objetivo != None:
                        Caballero.ataque_caballero(objetivo)
                        combatientes_actuales += 1
                        enfriamiento_accion = 0
                    # pocion
                    if pocion == True:
                        if Caballero.pociones > 0:
                            # comprobar si poción curaría por encima del nivel de vida del jugador
                            if Caballero.max_hp - Caballero.hp > efecto_pocion:
                                cantidad_curacion = efecto_pocion
                            else:
                                cantidad_curacion = Caballero.max_hp - Caballero.hp
                            Caballero.hp += cantidad_curacion
                            Caballero.pociones -= 1
                            texto_daño = TextoDaño(Caballero.rect.centerx, Caballero.rect.y, str(cantidad_curacion), verde)
                            texto_daño_grupo.add(texto_daño)
                            combatientes_actuales += 1
                            enfriamiento_accion = 0
        else:
            derrota = -1

        # accion del enemigo
        for count, Enemigo in enumerate(lista_enemigos):
            if combatientes_actuales == 2 + count:
                if Enemigo.alive == True:
                    enfriamiento_accion += 1
                    if enfriamiento_accion >= tiempo_espera_accion:
                        # comprobar si el enemigo necesita curarse antes
                        if (Enemigo.hp / Enemigo.max_hp) < 0.5 and Enemigo.pociones > 0:
                            # comprobar si poción curaría por encima del nivel de vida del enemigo
                            if Enemigo.max_hp - Enemigo.hp > efecto_pocion:
                                cantidad_curacion = efecto_pocion
                            else:
                                cantidad_curacion = Enemigo.max_hp - Enemigo.hp
                            Enemigo.hp += cantidad_curacion
                            Enemigo.pociones -= 1
                            texto_daño = TextoDaño(Enemigo.rect.centerx, Enemigo.rect.y, str(cantidad_curacion), verde)
                            texto_daño_grupo.add(texto_daño)
                            combatientes_actuales += 1
                            enfriamiento_accion = 0
                        # atacar
                        else:
                            Enemigo.atacar(Caballero)
                            combatientes_actuales += 1
                            enfriamiento_accion = 0
                else:
                    combatientes_actuales += 1

        # resetear si todos los personajes han tenido un turno
        if combatientes_actuales > combatientes_totales:
            combatientes_actuales = 1

    # comprobar si los enemigos han muerto
    enemigos_vivos = 0
    for Enemigo in lista_enemigos:
        if Enemigo.alive == True:
            enemigos_vivos += 1
    if enemigos_vivos == 0:
        derrota = 1

    # comprobar si la partida ha terminado
    if derrota != 0:
        if derrota == 1:
            pantalla.blit(imagen_victoria, (150, 50))
        if derrota == -1:
            pantalla.blit(imagen_derrota, (150, 50))
        if boton_reintentar.draw():
            Caballero.reset()
            for Enemigo in lista_enemigos:
                Enemigo.reset()
            combatientes_actuales = 1
            enfriamiento_accion
            derrota = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
