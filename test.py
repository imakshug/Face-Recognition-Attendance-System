from sklearn.neighbors import KNeighborsClassifier 
import cv2
import pickle
import numpy as np
import os
import csv 
import time
from datetime import datetime

from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.speak(str1) 

# Open the default camera (usually the built-in webcam)
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
with open ('data/names.pkl','rb') as f:
        LABLES= pickle.load(f)
with open ('data/faces_data.pkl', 'rb') as f:
        FACES= pickle.load(f)

knn= KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABLES) 
    
imgBackground= cv2.imread("background.png")    

COL_NAMES = ['NAME', 'TIME']
    
faces_data=[] #emty list

while True:
    # Capture frame-by-frame
    ret, frame = video.read()
    
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #for color and conversion
    faces= facedetect.detectMultiScale(gray, 1.3, 5)
    #get coordinate from faces: xy and w h widtyh height 
    for (x,y,w,h) in faces:
        crop_img= frame[y:y+h, x:x+w,: ]
        resized_img= cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output= knn.predict(resized_img)
        ts= time.time()
        date= datetime.fromtimestamp(ts).strftime("%d-%m-%y")
        timestamp= datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exit= os.path.isfile("Attendance/Attendance_" + date + ".csv")
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50,50,225),1 )   
        attendance = [str(output[0]), str(timestamp)]
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    # Display the resulting frame
    cv2.imshow("Frame", imgBackground)
    k= cv2.waitKey(1)
    if k ==ord ('o'):
        speak("Attendance Taken!") 
        time.sleep(5)

        if exit:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
                csvfile.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
                csvfile.close()
                    
    # Check if the user pressed the 'q' key
    if k == ord('q') :
        break

# Release the video capture object
video.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
