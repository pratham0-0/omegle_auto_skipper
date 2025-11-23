# OmeTV Gender Detection Bot

An automated bot for Ome.tv that detects the gender of the person you're connected with and automatically skips males.

## Features

- **Gender Detection**: Uses deep learning models to detect faces and classify gender
- **Auto-Skip**: Automatically clicks "Next" when a male is detected (with confirmation delay)
- **Smart Waiting**: Waits to confirm gender before taking action to avoid false positives
- **Edge Case Handling**: Skips if no face is detected for too long
- **Visual Feedback**: Shows detection status and countdown timers on screen

## Requirements

- **Python 3.7+**
- **Windows OS** (uses `pyautogui` for clicking)
- **Dependencies**: See `requirements.txt`

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download Model Files

Run the download script to get the required AI models (~56MB):

```bash
python download_models.py
```

This will download:
- Face detection model (`res10_300x300_ssd_iter_140000.caffemodel`)
- Gender classification model (`gender_net.caffemodel`)

### Step 3: Calibrate for Your Screen

1. Open Ome.tv in your browser and start a chat
2. Run the calibration script:

```bash
python calibrate.py
```

3. Follow the on-screen instructions:
   - Hover your mouse on top-left of stranger's video feed ,  then on bottom right of it, follow the instructions in terminal
   - Click on the **"Next" button** location
   - Press `Enter` to save

This creates a `calibration.json` file with your screen-specific settings.

## Usage

### Running the Bot

```bash
python main.py
```

### What It Does

1. **Captures** the stranger's video feed from your screen
2. **Detects faces** in the video
3. **Classifies gender** with confidence scores
4. **Takes action**:
   - **Male detected** (confidence > 60%): Waits 2 seconds to confirm, then skips
   - **Female detected** (confidence > 80%): Waits 1 second to confirm, then stays
   - **No face detected** for 3+ seconds: Skips
   - **Low confidence**: Waits and continues monitoring

### Terminal Output

- `Male detected. Verifying...` - Male detected, starting confirmation timer
- `Male detected. Waiting X.Xs...` - Countdown before skipping
- `SKIPPED THIS PERSON` - Bot clicked "Next"
- `Female detected. Verifying...` - Female detected, starting confirmation timer
- `Female detected! Staying.` - Confirmed female, staying on chat
- `No face detected.` - No face found in frame
- `No face for too long. Skipping...` - Skipped due to blank screen timeout

### On-Screen Display

The bot shows a window with:
- **Green box** around detected female faces
- **Red box** around detected male faces
- **Status text**:
  - `WAIT X.Xs` - Countdown timer (orange for males, green for females)
  - `SKIPPING` - About to skip (red)
  - `STAYING` - Confirmed female (green)

### Stopping the Bot

- Press `Q` in the bot window, or
- Press `Ctrl+C` in the terminal, or
- Close the bot window

## Configuration

Edit `config.py` to customize behavior:

```python
# Region of Interest - stranger's video area (left, top, width, height)
STRANGER_ROI = (1000, 184, 500, 1129)

# Next button coordinates (x, y)
NEXT_BUTTON_COORDS = (2598, 1514)

# Gender detection thresholds (0.0 to 1.0)
MALE_THRESHOLD = 0.6          # Confidence needed to classify as male
FEMALE_THRESHOLD = 0.8        # Confidence needed to classify as female (higher = stricter)

# Timing settings (in seconds)
BLANK_SCREEN_TIMEOUT = 3.0           # Skip if no face for this long
DELAY_AFTER_SKIP = 1.5               # Wait after clicking next
GENDER_CONFIRMATION_TIME = 2.0       # Wait before skipping a male
FEMALE_CONFIRMATION_TIME = 1.0       # Wait before confirming a female
```

## Testing

### Test Gender Detection on an Image

```bash
python demo.py
```

This will test the gender detection on a sample image and save the result as `demo_result.jpg`.

### Test Detection Without Clicking

Comment out the skip line in `main.py`:

```python
# utils.click_at(*next_btn)  # Comment this to disable clicking
```

## Troubleshooting

### "Model files not found"
- Run `python download_models.py` to download the AI models

### Bot clicks wrong location
- Re-run `python calibrate.py` to recalibrate the button position
- Make sure your browser is in the same position/size as when you calibrated

### Bot doesn't detect faces
- Check that the ROI (Region of Interest) is correctly set to the stranger's video
- Re-run `python calibrate.py` if you've changed your screen resolution or browser size

### Too many false positives (skipping females)
- Increase `FEMALE_THRESHOLD` in `config.py` (e.g., to 0.85 or 0.9)
- Increase `FEMALE_CONFIRMATION_TIME` to wait longer before confirming

### Too many false negatives (not skipping males)
- Decrease `MALE_THRESHOLD` in `config.py` (e.g., to 0.5)
- Decrease `GENDER_CONFIRMATION_TIME` to skip faster


## Limitations

- **Accuracy**: Gender detection is not 100% accurate (especially for androgynous appearances, poor lighting, or side profiles)
- **Screen-dependent**: Requires calibration for each screen resolution/browser setup
- **Windows only**: Uses Windows-specific automation (can be adapted for other OS)
- **Active window**: Works best when the browser is the active window

## Privacy & Ethics

This bot is for educational purposes. Please use responsibly and respect others' privacy. Be aware that:
- Automated bots may violate Ome.tv's terms of service
- Gender classification can be inaccurate and potentially offensive
- Use at your own risk

## License

This project is provided as-is for educational purposes.
