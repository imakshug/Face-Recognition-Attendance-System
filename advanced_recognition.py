from sklearn.neighbors import KNeighborsClassifier 
import cv2
import pickle
import numpy as np
import os
import csv 
import time
from datetime import datetime
import pygame
import threading
from win32com.client import Dispatch

class AdvancedFaceRecognition:
    def __init__(self):
        self.setup_system()
        self.load_models()
        self.setup_audio()
        
    def setup_system(self):
        """Initialize system components"""
        self.video = cv2.VideoCapture(0)
        self.facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        self.attendance_marked = set()  # Track who has been marked today
        self.last_recognition = {}  # Prevent spam marking
        self.confidence_threshold = 0.7
        
    def load_models(self):
        """Load trained face recognition models"""
        try:
            with open('data/names.pkl', 'rb') as f:
                self.LABELS = pickle.load(f)
            with open('data/faces_data.pkl', 'rb') as f:
                self.FACES = pickle.load(f)
            
            self.knn = KNeighborsClassifier(n_neighbors=5)
            self.knn.fit(self.FACES, self.LABELS)
            print("✅ Face recognition models loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            
    def setup_audio(self):
        """Setup audio notifications"""
        try:
            pygame.mixer.init()
            self.speak_engine = Dispatch("SAPI.SpVoice")
            print("✅ Audio system initialized")
        except:
            print("⚠️ Audio system not available")
            
    def speak(self, text):
        """Text to speech"""
        try:
            self.speak_engine.speak(text)
        except:
            print(f"🔊 {text}")
            
    def play_sound(self, sound_type="success"):
        """Play notification sounds"""
        try:
            if sound_type == "success":
                # Generate a simple beep
                frequency = 1000  # Hz
                duration = 200    # ms
                # Note: This is a placeholder - you'd need actual sound files
                print("🔔 *Beep*")
        except:
            pass
            
    def get_face_confidence(self, face_encoding):
        """Calculate confidence score for face recognition"""
        distances = self.knn.kneighbors([face_encoding], return_distance=True)[0][0]
        confidence = 1.0 - (np.mean(distances) / 100)  # Normalize
        return max(0, min(1, confidence))
        
    def draw_enhanced_ui(self, frame, name, confidence, x, y, w, h):
        """Draw enhanced UI elements on frame"""
        # Main face rectangle
        color = (0, 255, 0) if confidence > self.confidence_threshold else (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Name and confidence background
        label_bg = (x, y-70, x+w, y)
        cv2.rectangle(frame, (x, y-70), (x+w, y), color, -1)
        
        # Name text
        cv2.putText(frame, name, (x+5, y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Confidence text
        conf_text = f"Conf: {confidence:.2f}"
        cv2.putText(frame, conf_text, (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Status indicator
        status_text = "✓ READY" if confidence > self.confidence_threshold else "? UNCERTAIN"
        cv2.putText(frame, status_text, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
        
    def draw_system_info(self, frame):
        """Draw system information on frame"""
        height, width = frame.shape[:2]
        
        # System info background
        cv2.rectangle(frame, (10, 10), (400, 120), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (400, 120), (255, 255, 255), 2)
        
        # System info text
        info_lines = [
            "🎯 Advanced Face Recognition System",
            f"👥 Trained Users: {len(set(self.LABELS))}",
            f"📅 Date: {datetime.now().strftime('%d-%m-%Y')}",
            "⌨️ Controls: 'O'=Mark | 'Q'=Quit | 'R'=Reset"
        ]
        
        for i, line in enumerate(info_lines):
            y_pos = 30 + (i * 20)
            cv2.putText(frame, line, (15, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        # Today's attendance count
        today_count = len(self.attendance_marked)
        cv2.putText(frame, f"📊 Today's Attendance: {today_count}", (15, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                   
        return frame
        
    def mark_attendance(self, name):
        """Mark attendance for recognized person"""
        current_time = time.time()
        
        # Prevent spam marking (30 second cooldown)
        if name in self.last_recognition:
            if current_time - self.last_recognition[name] < 30:
                return False
                
        # Update tracking
        self.last_recognition[name] = current_time
        self.attendance_marked.add(name)
        
        # Save to CSV
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        
        attendance_file = f"Attendance/Attendance_{date}.csv"
        file_exists = os.path.isfile(attendance_file)
        
        try:
            with open(attendance_file, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["NAME", "TIME"])
                writer.writerow([name, timestamp])
                
            # Audio notifications
            self.speak(f"Attendance marked for {name}")
            self.play_sound("success")
            
            print(f"✅ Attendance marked: {name} at {timestamp}")
            return True
            
        except Exception as e:
            print(f"❌ Error marking attendance: {e}")
            return False
            
    def run(self):
        """Main recognition loop"""
        print("🚀 Starting Advanced Face Recognition System...")
        print("📋 Controls:")
        print("  - Press 'O' to mark attendance")
        print("  - Press 'Q' to quit")
        print("  - Press 'R' to reset today's attendance")
        
        try:
            # Load background if exists
            if os.path.exists("background.png"):
                img_background = cv2.imread("background.png")
            else:
                img_background = None
                
            while True:
                ret, frame = self.video.read()
                if not ret:
                    break
                    
                # Detect faces
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.facedetect.detectMultiScale(gray, 1.3, 5)
                
                # Process each detected face
                for (x, y, w, h) in faces:
                    # Extract and process face
                    crop_img = frame[y:y+h, x:x+w, :]
                    resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                    
                    # Predict identity
                    output = self.knn.predict(resized_img)
                    confidence = self.get_face_confidence(resized_img[0])
                    
                    name = output[0] if confidence > self.confidence_threshold else "Unknown"
                    
                    # Draw enhanced UI
                    frame = self.draw_enhanced_ui(frame, name, confidence, x, y, w, h)
                
                # Draw system information
                frame = self.draw_system_info(frame)
                
                # Apply background if available
                if img_background is not None:
                    try:
                        # Overlay frame on background
                        bg_copy = img_background.copy()
                        h, w = frame.shape[:2]
                        bg_h, bg_w = bg_copy.shape[:2]
                        
                        if h <= bg_h and w <= bg_w:
                            bg_copy[162:162+h, 55:55+w] = frame
                            frame = bg_copy
                    except:
                        pass  # Use original frame if overlay fails
                
                # Display frame
                cv2.imshow("🎯 Advanced Face Recognition System", frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('o') or key == ord('O'):
                    # Mark attendance for all recognized faces
                    for (x, y, w, h) in faces:
                        crop_img = frame[y:y+h, x:x+w, :]
                        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                        output = self.knn.predict(resized_img)
                        confidence = self.get_face_confidence(resized_img[0])
                        
                        if confidence > self.confidence_threshold:
                            self.mark_attendance(output[0])
                            
                elif key == ord('r') or key == ord('R'):
                    # Reset today's attendance tracking
                    self.attendance_marked.clear()
                    self.last_recognition.clear()
                    print("🔄 Today's attendance tracking reset")
                    
        except Exception as e:
            print(f"❌ Error in recognition loop: {e}")
            
        finally:
            # Cleanup
            self.video.release()
            cv2.destroyAllWindows()
            print("👋 Face Recognition System stopped")

if __name__ == "__main__":
    system = AdvancedFaceRecognition()
    system.run()
