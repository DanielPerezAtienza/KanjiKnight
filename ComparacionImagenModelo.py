from tensorflow.keras.models import load_model
import numpy as np
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from numpy import asarray
from PIL import Image

from kanjijapanese import label

# Cargar imagen
img = Image.open('Kanji 06-06-2022 12h34m17s.jpg')

# Conversión de la imagen a escala de grises
img = img.convert(mode='L')

# Conversión a array de numpy
data = asarray(img)
data = data.reshape((1, 48, 48, 1))
print("Dimensiones: ", data.shape)


with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
    model = load_model('kanji.h5')

prediction = model.predict(data)

char = label[np.argmax(prediction)]
print(char)