import cv2
import pickle
import numpy as np
import os
# Open the default camera (usually the built-in webcam)
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
faces_data=[] #emty list

i=0

name=input("Enter Your Name: ")
while True:
    # Capture frame-by-frame
    ret, frame = video.read()
    
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #for color and conversion
    faces= facedetect.detectMultiScale(gray, 1.3, 5)
    #get coordinate from faces: xy and w h widtyh height 
    for (x,y,w,h) in faces:
        crop_img= frame[y:y+h, x:x+w,: ]
        resized_img= cv2.resize(crop_img, (50,50))
        if len(faces_data)<=100 and i%10==0:
            faces_data.append(resized_img)
        i=i+1
        cv2.putText(frame, str(len(faces_data)), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1,(50,50,255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50,50,225),1 )   
    # Display the resulting frame
    cv2.imshow("Frame", frame)
    
    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q') or len(faces_data)==100:
        break

# Release the video capture object
video.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

faces_data= np.asarray(faces_data)
faces_data= faces_data.reshape(100, -1)

#for names
if 'names.pkl' not in os.listdir('data/'):
    names= [name]*100
    with open ('data/names.pkl','wb') as f:
        pickle.dump(names, f)
        
else:
    with open ('data/names.pkl','rb') as f:
        names= pickle.load(f)
    names =names+[name]*100
    with open ('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)   
        
#for faces        
if 'faces_data.pkl' not in os.listdir('data/'):
    with open ('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
        
else:
    with open ('data/faces_data.pkl', 'rb') as f:
        faces= pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open ('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)                  