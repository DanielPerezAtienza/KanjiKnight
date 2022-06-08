import glob
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split  ### 追加
from tensorflow import keras
from keras import backend as K

folder = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
          "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]

image_size = 48
batch_size = 128
epochs = 50

x = []
y = []

for index, name in enumerate(folder):
    dir = "./moji/" + name
    files = glob.glob(dir + "/*.png")
    for i, file in enumerate(files):
        image = Image.open(file)
        image = image.convert("L")
        image = image.resize((image_size, image_size))
        data = np.asarray(image)
        x.append(data)
        y.append(index)

x = np.array(x)
y = np.array(y)

x = x.astype('float32')
x = x / 255.0

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=111)
x_train = np.reshape(x_train, [-1, image_size, image_size, 1])
x_test = np.reshape(x_test, [-1, image_size, image_size, 1])
original_dim = 2304  ### 48×48=2304
image_size = 48

print("Number of training examples:")
print("X:", x.shape)
print("y:", y.shape)


if K.image_data_format() == "channels_first":
  x_train = x_train.reshape(x_train.shape[0], 1,48,48)
  x_test = x_test.reshape(x_test.shape[0], 1,48,48)
  shape = (1,48,48)
else:
  x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
  x_test = x_test.reshape(x_test.shape[0], 48, 48, 1)
  shape = (48,48,1)


model = keras.Sequential([
  keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=shape),
  keras.layers.MaxPooling2D(2,2),
  keras.layers.Conv2D(64, (3,3), activation='relu'),
  keras.layers.MaxPooling2D(2,2),
  keras.layers.Flatten(),
  keras.layers.Dropout(0.5),
  keras.layers.Dense(2048, activation='relu'),
  keras.layers.Dense(879, activation="softmax")
])

model.summary()

model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, callbacks=[keras.callbacks.TerminateOnNaN()])

test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test Accuracy: ", test_acc)

model.save('kanji.h5')
