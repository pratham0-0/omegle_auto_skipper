import time
import cv2
import numpy as np
import config
import utils
from gender_detector import GenderDetector
import json
import os

def load_config():
    # Try to load from calibration.json
    if os.path.exists("calibration.json"):
        with open("calibration.json", "r") as f:
            data = json.load(f)
            return data["STRANGER_ROI"], data["NEXT_BUTTON_COORDS"]
    return config.STRANGER_ROI, config.NEXT_BUTTON_COORDS

def main():
    print("Initializing Ome.tv Bot...")
    
    try:
        detector = GenderDetector()
    except Exception as e:
        print(f"Failed to initialize detector: {e}")
        return

    roi, next_btn = load_config()
    print(f"Using ROI: {roi}")
    print(f"Next Button: {next_btn}")
    
    print("Starting loop. Press Ctrl+C to stop.")
    
    # State variables
    last_face_time = time.time()
    male_start_time = None
    female_start_time = None
    
    while True:
        start_time = time.time()
        
        # 1. Capture Screen
        frame = utils.capture_screen(region=roi)
        if frame is None:
            print("Failed to capture screen.")
            time.sleep(1)
            continue

        # 2. Detect Face
        faces = detector.detect_face(frame)
        
        if not faces:
            print("No face detected.")
            
            # Handle blank screen / loading
            if time.time() - last_face_time > config.BLANK_SCREEN_TIMEOUT:
                print("No face for too long. Skipping...")
                utils.click_at(*next_btn)
                last_face_time = time.time() # Reset timer
                time.sleep(config.DELAY_AFTER_SKIP)
        else:
            last_face_time = time.time()
            # 3. Predict Gender for the largest face
            # Assuming the largest face is the main person
            largest_face = max(faces, key=lambda b: (b[2]-b[0]) * (b[3]-b[1]))
            
            gender, confidence = detector.predict_gender(frame, largest_face)
            
            if gender:
                print(f"Detected: {gender} ({confidence:.2f})")
                
                # Visual Debug
                label = f"{gender}: {confidence:.2f}"
                color = (0, 255, 0) if gender == 'Female' else (0, 0, 255)
                cv2.rectangle(frame, (largest_face[0], largest_face[1]), (largest_face[2], largest_face[3]), color, 2)
                cv2.putText(frame, label, (largest_face[0], largest_face[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                
                # 4. Logic
                if gender == 'Male':
                    if confidence > config.MALE_THRESHOLD:
                        if male_start_time is None:
                            male_start_time = time.time()
                            print("Male detected. Verifying...")
                        
                        elapsed = time.time() - male_start_time
                        remaining = config.GENDER_CONFIRMATION_TIME - elapsed
                        
                        if elapsed > config.GENDER_CONFIRMATION_TIME:
                            print("SKIPPED THIS PERSON")
                            cv2.putText(frame, "SKIPPING", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                            cv2.imshow("OmeTV Bot View", frame)
                            cv2.waitKey(1)
                            utils.click_at(*next_btn)
                            male_start_time = None # Reset
                            time.sleep(config.DELAY_AFTER_SKIP)
                        else:
                            print(f"Male detected. Waiting {remaining:.1f}s...")
                            cv2.putText(frame, f"WAIT {remaining:.1f}s", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
                    else:
                        print("Male detected but low confidence. Waiting...")
                        male_start_time = None # Reset if confidence drops? Or keep? Let's reset to be safe.
                
                elif gender == 'Female':
                    male_start_time = None # Reset timer if we see a female
                    if confidence > config.FEMALE_THRESHOLD:
                        if female_start_time is None:
                            female_start_time = time.time()
                            print("Female detected. Verifying...")
                        
                        elapsed = time.time() - female_start_time
                        remaining = config.FEMALE_CONFIRMATION_TIME - elapsed
                        
                        if elapsed > config.FEMALE_CONFIRMATION_TIME:
                            print("Female detected! Staying.")
                            cv2.putText(frame, "STAYING", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            # Wait a bit to avoid re-processing same frame too fast? 
                            # Or just continue monitoring.
                            time.sleep(1) 
                        else:
                            print(f"Female detected. Waiting {remaining:.1f}s...")
                            cv2.putText(frame, f"WAIT {remaining:.1f}s", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    else:
                        print("Female detected but low confidence.")
                        female_start_time = None # Reset if confidence drops
                
        cv2.imshow("OmeTV Bot View", frame)
        
        # Check if 'q' is pressed or window is closed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        try:
            if cv2.getWindowProperty("OmeTV Bot View", cv2.WND_PROP_VISIBLE) < 1:
                break
        except Exception:
            pass
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
