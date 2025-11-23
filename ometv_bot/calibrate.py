import pyautogui
import time
import json
import os
import cv2
import numpy as np
import mss

def get_mouse_pos(prompt):
    print(prompt)
    print("Move your mouse to the target position in 7 seconds...")
    for i in range(7, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    pos = pyautogui.position()
    print(f"Captured: {pos}")
    return pos

def capture_full_screen():
    """Capture the entire screen"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame

def show_confirmation(roi, next_btn_coords):
    """Show visual confirmation of ROI and button location"""
    print("\n=== Visual Confirmation ===")
    print("Capturing screen to show your calibration...")
    time.sleep(1)  # Give user a moment
    
    # Capture screen
    frame = capture_full_screen()
    
    # Draw ROI rectangle (green)
    x, y, w, h = roi
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.putText(frame, "STRANGER VIDEO ROI", (x, y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Draw Next button marker (red circle)
    btn_x, btn_y = next_btn_coords
    cv2.circle(frame, (btn_x, btn_y), 20, (0, 0, 255), 3)
    cv2.circle(frame, (btn_x, btn_y), 5, (0, 0, 255), -1)
    cv2.putText(frame, "NEXT BUTTON", (btn_x + 30, btn_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Add instructions at top
    cv2.putText(frame, "Press 'Y' to confirm and save, 'N' to recalibrate, 'Q' to quit", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Show the image
    cv2.imshow("Calibration Confirmation", frame)
    
    print("\nPlease review the calibration on screen:")
    print("  - GREEN box = Stranger's video area (ROI)")
    print("  - RED circle = Next button location")
    print("\nPress:")
    print("  'Y' = Confirm and save")
    print("  'N' = Recalibrate")
    print("  'Q' = Quit without saving")
    
    while True:
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('y') or key == ord('Y'):
            cv2.destroyAllWindows()
            return True
        elif key == ord('n') or key == ord('N'):
            cv2.destroyAllWindows()
            return False
        elif key == ord('q') or key == ord('Q'):
            cv2.destroyAllWindows()
            return None

def calibrate():
    print("=== Ome.tv Bot Calibration ===")
    print("We need to define the Stranger's Video Area and the Next Button.")
    print("\nIMPORTANT: Make sure Ome.tv is open and visible on your screen!")
    input("\nPress Enter when ready to start...")
    
    while True:
        print("\n--- Stranger Video Area ---")
        top_left = get_mouse_pos("Hover over the TOP-LEFT corner of the stranger's video.")
        bottom_right = get_mouse_pos("Hover over the BOTTOM-RIGHT corner of the stranger's video.")
        
        roi = (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)
        
        print("\n--- Next Button ---")
        next_btn = get_mouse_pos("Hover over the center of the NEXT button.")
        
        config_data = {
            "STRANGER_ROI": roi,
            "NEXT_BUTTON_COORDS": (next_btn.x, next_btn.y)
        }
        
        print("\nCalibration captured!")
        print(f"ROI: {roi}")
        print(f"Next Button: {next_btn}")
        
        # Show visual confirmation
        confirmation = show_confirmation(roi, (next_btn.x, next_btn.y))
        
        if confirmation is True:
            # User confirmed, save the calibration
            with open("calibration.json", "w") as f:
                json.dump(config_data, f, indent=4)
            
            print("\n✓ Calibration saved to calibration.json!")
            print("The bot will use these values when you run main.py")
            break
        elif confirmation is False:
            # User wants to recalibrate
            print("\nRecalibrating...")
            continue
        else:
            # User quit
            print("\nCalibration cancelled. No changes saved.")
            break

if __name__ == "__main__":
    calibrate()
