import mss
import numpy as np
import cv2
import pyautogui

def capture_screen(region=None):
    """
    Captures the screen or a specific region using MSS.
    Args:
        region: tuple (left, top, width, height)
    Returns:
        numpy array (BGR image for OpenCV)
    """
    try:
        with mss.mss() as sct:
            if region:
                # MSS requires a dict for region: {'top': int, 'left': int, 'width': int, 'height': int}
                monitor = {
                    "left": int(region[0]),
                    "top": int(region[1]),
                    "width": int(region[2]),
                    "height": int(region[3])
                }
                screenshot = sct.grab(monitor)
            else:
                screenshot = sct.grab(sct.monitors[1]) # Default to primary if no region

            frame = np.array(screenshot)
            # MSS returns BGRA, convert to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

def click_at(x, y):
    """
    Clicks at the specified coordinates.
    """
    try:
        pyautogui.click(x, y)
    except Exception as e:
        print(f"Error clicking at ({x}, {y}): {e}")
