# -*- coding: utf-8 -*-
"""Assignment 1 on CNN implementation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DUUbJ0wIIh_jnZfyYq_8XTISnxOE7iyt
"""

import numpy as np
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Flatten, Conv2D, MaxPooling2D, Dropout, Input
from tensorflow.keras import backend as k
from matplotlib import pyplot as plt

"""Iporting MNIST data set from keras library"""

(X_train,y_train),(X_test,y_test) = keras.datasets.mnist.load_data()

"""checking data dimention"""

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

y_train

"""Checking the data Handwritten image & train data by plotting"""

from matplotlib import pyplot as plt
plt.imshow(X_train[5])
print(y_train[5])

rows = 3
cols = 3
fig = plt.figure(figsize=(5,5))
for j in range(0, rows*cols):
  fig.add_subplot(rows, cols, j+1)
  plt.imshow(X_train[j])
  print(y_train[j])

"""Flattening the [28, 28] data set in to one dimentional data by reshaping and using as input."""

img_rows, img_cols=28, 28

if k.image_data_format() == 'channels_first':
   #reshape dataset to have a single channel
  X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
  X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
  inpx = (1, img_rows, img_cols)
else:
  #reshape dataset to have a single channel
  X_train = X_train.reshape(X_train.shape [0], img_rows, img_cols, 1)
  X_test = X_test.reshape(X_test.shape [0], img_rows, img_cols, 1)
  inpx = (img_rows, img_cols, 1)

"""As all the pixel value is between 1-255, converting the value to 0 to 1"""

X_train = X_train/255
X_test = X_test/255

"""=>Using the one dimentional data as input for the CNN considering kernel size (3,3) and 02 convolutional layer with 'relu' as activation function.

=>In layer3, MaxPooling has been done where pool size is coonsidered (3,3,).

=>To avoid overfitting, in layer4 Dropout function has been used.

=>layer5 flatten the out put of layer4

=>layer6 & layer7 is the fully connected node where 'relu' has been used for activation functon.


=>in the final layer, layer8 10 output nodes has been decalred as this is a multiclass problem and there are 10 classes from 0-9 and using softmax as activation function
"""

inpx = Input(shape=inpx)
layer1 = Conv2D(32, kernel_size=(3, 3), activation='relu') (inpx)
layer2 = Conv2D(64, (3, 3), activation='relu')(layer1)
layer3 = MaxPooling2D(pool_size=(3, 3))(layer2)
# To prevent overfitting
layer4 = Dropout (0.5) (layer3)

layer5 = Flatten()(layer4)
layer6 = Dense (250, activation='relu')(layer5)
layer7 = Dense (32, activation='relu')(layer6)
layer8 = Dense(10, activation='softmax') (layer7)

"""Training/Fitting the model with train data"""

model = Model([inpx], layer8)
model.compile(loss='sparse_categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])
history = model.fit(X_train,y_train,batch_size=500, epochs=10,validation_split=0.2)

"""evaluate the test data set and Checking Loss & Accuracy"""

score= model.evaluate(X_test,y_test, verbose=0)
print('loss=', score[0])
print('Accuracy=', score[1])

"""Predict test data possibibility where in every arrat it shows the probability of being 0-9 of that deigit. the acual number will the one with the highest probability."""

y_prob = model.predict(X_test)
y_pred= y_prob.argmax(axis=1)
print(y_pred)

"""Checking Accuaracy of the model"""

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

"""Plot training vs validation loss

"""

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("training Loss vs test/Validation Loss")
plt.legend(['traing loss', 'Validation loss'], loc = 'best')

"""Plot training vs validation accuracy"""

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Training Accuracy vs Testing/Validataion Accuracy")
plt.legend(['traing Accuracy', 'Validation Accuracy'], loc = 'best')

"""Plotting of a few correct predicted samples"""

for i in np.random.choice(np.arange(0,len(y_test)), size = (5,)):
  img = (X_test[i]*255).reshape((28,28)).astype('uint8')
  print("y_test",y_test[i])
  print("Predicted",y_pred[i])
  plt.imshow(img)
  plt.show()

"""Plotting of a few misclassified samples"""

mismatch_list = y_test-y_pred
mismatch_index = np.nonzero(mismatch_list)
index_value = mismatch_index[0]
for l in np.random.choice(np.arange(0,len(mismatch_index[0])), size = (10,)):
  miss_img = (X_test[index_value[l]]*255).reshape((28,28)).astype('uint8')
  print("y_pred=", y_pred[index_value[l]])
  print("y_test=", y_test[index_value[l]])
  plt.imshow(miss_img)
  plt.show()