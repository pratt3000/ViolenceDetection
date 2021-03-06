# %% [code]
import numpy as np
#import tensorflow as tf
#import keras as k
import pandas as pd
import matplotlib.pyplot as plt
import cv2 
import math
import os


# %% [code]
fps = 30
title = 'normal speed video'
delay = int(100/ fps)

# %% [code]
X = []
count = 0
for i in range (1,1000):
    videoFile = "C:/Users/pratt/Desktop/RealLifeViolenceDataset/Violence/V_%d.mp4" % i
    cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
    frameRate = cap.get(5)
    #print(frameRate)
    #print(cap.isOpened())
    while(cap.isOpened()):
        #print(1)
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            X_temp = cv2.resize(frame, (64,64))
            X.append(X_temp)
    cap.release()
print(X)
# %% [code]
#1 for violence


X = np.reshape(X, (5827, 64*64*3))
print(np.shape(X))
X = np.concatenate((X,np.ones((5827,1))), axis = 1)
print(np.shape(X))

# %% [code]
X2 = []
count = 0
for i in range (1,1000):
    videoFile = "C:/Users/pratt/Desktop/RealLifeViolenceDataset/NonViolence/NV_%d.mp4" % i
    cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
    frameRate = cap.get(5) #frame rate
    #print(frameRate)
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            X_temp = cv2.resize(frame, (64,64))
            X2.append(X_temp)
    cap.release()

# %% [code]
print(np.shape(X2))

# %% [code]
#0 for non-violence


X2 = np.reshape(X2, (4980, 64*64*3))
print(np.shape(X2))
X2 = np.concatenate((X2,np.zeros((4980,1))), axis = 1)
print(np.shape(X2))

# %% [code]
X_true = np.concatenate((X,X2), axis = 0)
print(np.shape(X_true))

# %% [code]
np.random.shuffle(X_true)
X_true = X_true.astype(int)
#print(X_true)

# %% [code]
y_true = X_true[:, -1]
print(y_true)
X_true = np.delete(X_true, -1, 1)

# %% [code]
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import optimizers
import keras as K
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
seed = 78
test_size = 0.33

# %% [code]
X_train, X_test, y_train, y_test = train_test_split(X_true, y_true, test_size=test_size, random_state=seed)

# %% [code]
X_train = X_train/255
X_test = X_test/255

# %% [code]
np.savetxt('C:/Users/pratt/Desktop/Y_train.csv', y_train, delimiter=',')

# %% [code]
from numpy import loadtxt
from xgboost import XGBClassifier

# %% [code]
model = XGBClassifier()
model.fit(X_train, y_train)

# %% [code]
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
y_pred = model.predict(X_test).round()

# %% [code]
# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

# %% [code]
import cv2
from PIL import Image, ImageDraw, ImageFont
import time
 
ImageFont.load_default()
font = ImageFont.load_default()


# %% [code]


videoFile = "C:/Users/pratt/Downloads/test.mp4"
cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
frameRate = cap.get(5) 
i = 0
y_temp= []
deno = 0
while(cap.isOpened()):
    #print(1)
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        X_temp = cv2.resize(frame, (64,64))
        
        #im = Image.fromarray(frame)
        #plt.figure()
        #plt.imshow(im)
        X_temp = np.reshape(X_temp, (1, 64*64*3))
        X_temp = X_temp/255
        
        y_temp.append(model.predict(X_temp))
        sum = y_temp[i]#.astype(float)
        for k in range (1,7):
            if (i-k) > 0:
                sum = sum + ( y_temp[i-k] / (k+1))
                #print(i-k)
            else:    #print(y_temp[i])
                deno = deno + (1/(k+1))
                break
        sum = sum/deno
        
        if sum<0.5 :
            y_temp[i] = 0
            #message = "NON-VIOLENT"
        else:
            y_temp[i] = 1
            #message = "VIOLENT"
        #draw = ImageDraw.Draw(im)
        #draw.text((50, 50), message, fill=(255,255,255,128), font = font)
        #plt.imshow(im)
        i = i+1
cap.release()

print(y_temp)

# %% [code]
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
#filename = 'C:/Users/pratt/Desktop/finalized_model.sav'
#pickle.dump(model, open(filename, 'wb'))
 
# some time later...
 
# load the model from disk
#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, y_test)
#print(result)
# %% [code]
#np.savetxt('/kaggle/output/working/Y_true.csv', y_true, delimiter=',')
import cv2 
import numpy as np 
   
# Create a VideoCapture object and read from input file 
cap = cv2.VideoCapture('C:/Users/pratt/Downloads/test.mp4') 
   
# Check if camera opened successfully 
if (cap.isOpened()== False):  
  print("Error opening video  file") 
i =0  
# Read until video is completed 
while(cap.isOpened()): 
      
  # Capture frame-by-frame 
  ret, frame = cap.read() 
  if ret == True: 
    font = cv2.FONT_HERSHEY_SIMPLEX 
  
    # Use putText() method for 
    # inserting text on video
    
    if (y_temp[1] == 0):
        cv2.putText(frame,  
                    'NON VIOLENCE',  
                    (50, 50),  
                    font, 1,  
                    (0, 255, 255),  
                    2,  
                    cv2.LINE_4)
    if (y_temp[1] == 1):
        cv2.putText(frame,  
                    'VIOLENCE',  
                    (50, 50),  
                    font, 1,  
                    (0, 255, 255),  
                    2,  
                    cv2.LINE_4)
    # Display the resulting frame 
    cv2.imshow('Frame', frame) 
    i = i+1
    # Press Q on keyboard to  exit 
    if cv2.waitKey(25) & 0xFF == ord('q'): 
      break
  
  # Break the loop 
  else:  
    break
   
# When everything done, release  
# the video capture object 
cap.release() 
   
# Closes all the frames 
cv2.destroyAllWindows() 
# %% [code]
#np.savetxt('/kaggle/output/working/X_true.csv', X_true, delimiter=',')

import pickle
pickle.dump(model, open('C:/Users/pratt/Desktop/ViolenceNonviolence.dat', 'wb'))