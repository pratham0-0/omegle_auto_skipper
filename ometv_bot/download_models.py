import requests
import os

def download_file(url, filename):
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename} successfully.")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def main():
    models = [
        {
            "url": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
            "filename": "deploy.prototxt"
        },
        {
            "url": "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel",
            "filename": "res10_300x300_ssd_iter_140000.caffemodel"
        },
        {
            "url": "https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/gender_deploy.prototxt",
            "filename": "gender_deploy.prototxt"
        },
        {
            # Alternative URL with blob/raw logic
            "url": "https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/gender_net.caffemodel", 
            "filename": "gender_net.caffemodel"
        }
    ]

    for model in models:
        if not os.path.exists(model["filename"]):
            success = download_file(model["url"], model["filename"])
            if not success:
                print(f"CRITICAL: Could not download {model['filename']}. Please download it manually.")
        else:
            print(f"{model['filename']} already exists.")

if __name__ == "__main__":
    main()
