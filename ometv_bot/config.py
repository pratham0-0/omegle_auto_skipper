# Screen resolution: 2560x1600
# You can adjust these values or run 'calibrate.py' (to be created) to set them automatically.

# Region of Interest (ROI) for the stranger's video feed
# Format: (left, top, width, height)
# User provided: ROI: (2425, 153, 1559, 1170)
STRANGER_ROI = (21, 167, 601, 574) 

# Coordinates for the "Next" button
# Format: (x, y)
# User provided: Next Button: Point(x=2614, y=1530)
NEXT_BUTTON_COORDS = (312, 858) 

# Gender Detection Thresholds
CONFIDENCE_THRESHOLD = 0.7 

MALE_THRESHOLD = 0.6
FEMALE_THRESHOLD = 0.8

# Timeouts
BLANK_SCREEN_TIMEOUT = 3.0 # Seconds to wait if no face is detected before skipping (optional)
DELAY_AFTER_SKIP = 1.5 # Seconds to wait after clicking next before analyzing again
GENDER_CONFIRMATION_TIME = 2.0 # Seconds to wait before skipping a male to confirm detection
FEMALE_CONFIRMATION_TIME = 1.0 # Seconds to wait before confirming a female
