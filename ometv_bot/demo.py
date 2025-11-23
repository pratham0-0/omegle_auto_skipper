import cv2
import numpy as np
from gender_detector import GenderDetector
import config

def demo(image_path):
    print(f"--- Processing {image_path} ---")
    
    try:
        detector = GenderDetector()
    except Exception as e:
        print(f"Error initializing detector: {e}")
        return

    frame = cv2.imread(image_path)
    if frame is None:
        print("Could not read image.")
        return

    # Detect face
    faces = detector.detect_face(frame)
    
    if not faces:
        print("No faces detected.")
        return

    print(f"Found {len(faces)} faces.")
    
    # Process each face
    for i, bbox in enumerate(faces):
        gender, confidence = detector.predict_gender(frame, bbox)
        
        action = "WAIT"
        if gender == 'Male':
            if confidence > config.MALE_THRESHOLD:
                action = "SKIP"
            else:
                action = "WAIT (Low Conf)"
        elif gender == 'Female':
            if confidence > config.FEMALE_THRESHOLD:
                action = "STAY"
            else:
                action = "WAIT (Low Conf)"
        
        print(f"Face {i+1}: Gender={gender}, Score={confidence:.4f}, Action={action}")
        
        # Draw on image for visual verification (saved to file)
        x1, y1, x2, y2 = bbox
        color = (0, 255, 0) if action == "STAY" else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{gender}: {confidence:.2f} ({action})"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    output_path = "demo_result.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Saved result to {output_path}")

if __name__ == "__main__":
    # Use the path from metadata
    img_path = r"C:/Users/PRATHAM/.gemini/antigravity/brain/0200c879-9336-4f2c-82be-13d90f2f46a2/uploaded_image_1763873278303.png"
    demo(img_path)
