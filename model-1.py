# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:51:45 2021

@author: LENOVO
"""


import sys,os#os for interaction with os but i doubt it will be useful here
#import opencv-python #for computer vision and identification purposes
import tensorflow#for AI models, using data flow graphs to build models.
import numpy as np#for linear processing, for Scientific Computing.
import pandas as pd#For dealing with data analysis and manipulation
# for developing and evaluating deep learning models
import matplotlib 

from keras.models import Sequential 
#dense layer:classic fully connected neural network layer:each input node is connected to each output node.
#Dropout layer:similar except that when the layer is used, the activations are set to zero for some random nodes. This is a way to prevent overfitting.
#activation functions help in reducing unneccessary noise
#activation functions help the network use the important information and suppress the irrelevant data points.
#flatten:didn't understand fully but i think it is used to convert matrix to single array
#Flattening a tensor means to remove all of the dimensions except for one. This is exactly what the Flatten layer do.
from keras.layers import Dense, Dropout, Activation, Flatten  
#Conv2D for two dimensional convolutions network
# Max pooling is a sample-based discretization process. 
# The objective is to down-sample an input representation
#  (image, hidden-layer output matrix, etc.), reducing its
#   dimensionality and allowing for assumptions to be made about features
#   contained in the sub-regions binned.
#Batch Normalization helps in accelearting the learning DNNs
#Average Pooling2d:Bouncer
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization,AveragePooling2D
#categorical_crossentropy : don't know
from keras.losses import categorical_crossentropy  
#adam:replacement optimization algorithm for stochastic gradient descent for training deep learning models.#don't understand what it is 
from keras.optimizers import Adam  
#l2:allows you to add a penalty for weight size to the loss function
from keras.regularizers import l2 
#np_utils:Numpy-related utilities. 
from keras.utils import np_utils  

# why is it commented out??
# pd.set_option('display.max_rows', 500)  
# pd.set_option('display.max_columns', 500)  
# pd.set_option('display.width', 1000)  

df = pd.read_csv("C:/Users/LENOVO/Desktop/fer2013.csv") 

# print(df.info())  
# print(df["Usage"].value_counts())  

# print(df.head()) #tell about what is int he data frame 
X_train,train_y,X_test,test_y=[],[],[],[]  

for index, row in df.iterrows():  
    val=row['pixels'].split(" ")  
    try:  
        if 'Training' in row['Usage']:  
           X_train.append(np.array(val,'float32'))  
           train_y.append(row['emotion'])  
        elif 'PublicTest' in row['Usage']:  
           X_test.append(np.array(val,'float32'))  
           test_y.append(row['emotion'])  
    except:  
        print(f"error occured at index :{index} and row:{row}")  


num_features = 64  
num_labels = 7  
batch_size = 64  
epochs = 50
width, height = 48, 48  
emotion_labels = ["sinirli", "tiksinmis", "korkmus", "mutlu", "mutsuz", "saskin", "Neutral"]
classes=np.array(("sinirli", "tiksinmis", "korkmus", "mutlu", "mutsuz", "saskin", "Neutral"))


X_train = np.array(X_train,'float32')  
train_y = np.array(train_y,'float32')  
X_test = np.array(X_test,'float32')  
test_y = np.array(test_y,'float32')  

train_y=np_utils.to_categorical(train_y, num_classes=num_labels)  
test_y=np_utils.to_categorical(test_y, num_classes=num_labels)  

#cannot produce  
#normalizing data between oand 1  
X_train -= np.mean(X_train, axis=0)  
X_train /= np.std(X_train, axis=0)  

X_test -= np.mean(X_test, axis=0)  
X_test /= np.std(X_test, axis=0)  

X_train = X_train.reshape(X_train.shape[0], 48, 48, 1)  

X_test = X_test.reshape(X_test.shape[0], 48, 48, 1)  

# print(f"shape:{X_train.shape}")  
##designing the cnn  
#1st convolution layer  
model = Sequential()  

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(X_train.shape[1:])))  
model.add(Conv2D(64,kernel_size= (3, 3), activation='relu'))  
# model.add(BatchNormalization())  
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))  
model.add(Dropout(0.5))  

#2nd convolution layer  
model.add(Conv2D(32, (3, 3), activation='relu'))  
model.add(Conv2D(32, (3, 3), activation='relu'))  
# model.add(BatchNormalization())  
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))  
model.add(Dropout(0.5))  

#3rd convolution layer  
model.add(Conv2D(64, (3, 3), activation='relu'))  
model.add(Conv2D(64, (3, 3), activation='relu'))  
# model.add(BatchNormalization())  
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))  

model.add(Flatten())  

#fully connected neural networks  
model.add(Dense(128, activation='relu'))  
model.add(Dropout(0.2))  
model.add(Dense(128, activation='relu'))  
model.add(Dropout(0.2))  

model.add(Dense(num_labels, activation='softmax'))  

# model.summary()  

#Compliling the model  
model.compile(loss=categorical_crossentropy,  
              optimizer=Adam(),  
              metrics=['accuracy'])  

#Training the model  
history = model.fit(X_train, train_y,  
          batch_size=batch_size,  
          epochs=epochs,  
          verbose=1,  
          validation_data=(X_test, test_y),  
          shuffle=True)  


#Saving the  model to  use it later on  
fer_json = model.to_json()  
with open("fer.json", "w") as json_file:  
    json_file.write(fer_json)  
model.save_weights("fer.h5") 

weights = model.get_weights()
np.save('my_model_weights', weights)

loss = model.evaluate(X_train/255., train_y) 
print("Train Loss " + str(loss[0]))
print("Train Acc: " + str(loss[1]))

loss = model.evaluate(X_test/255., test_y) 
print("Test Loss " + str(loss[0]))
print("Test Acc: " + str(loss[1]))



