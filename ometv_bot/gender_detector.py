import cv2
import numpy as np
import os

class GenderDetector:
    def __init__(self):
        # Paths to models
        self.face_proto = "deploy.prototxt"
        self.face_model = "res10_300x300_ssd_iter_140000.caffemodel"
        self.gender_proto = "gender_deploy.prototxt"
        self.gender_model = "gender_net.caffemodel"
        
        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self.gender_list = ['Male', 'Female']

        # Load networks
        if not os.path.exists(self.face_model) or not os.path.exists(self.gender_model):
            raise FileNotFoundError("Model files not found. Please ensure .prototxt and .caffemodel files are in the directory.")

        self.face_net = cv2.dnn.readNet(self.face_model, self.face_proto)
        self.gender_net = cv2.dnn.readNet(self.gender_model, self.gender_proto)

    def detect_face(self, frame, conf_threshold=0.5):
        frame_opencv_dnn = frame.copy()
        frame_height = frame_opencv_dnn.shape[0]
        frame_width = frame_opencv_dnn.shape[1]
        
        blob = cv2.dnn.blobFromImage(frame_opencv_dnn, 1.0, (300, 300), [104, 117, 123], False, False)
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frame_width)
                y1 = int(detections[0, 0, i, 4] * frame_height)
                x2 = int(detections[0, 0, i, 5] * frame_width)
                y2 = int(detections[0, 0, i, 6] * frame_height)
                bboxes.append([x1, y1, x2, y2])
        
        return bboxes

    def predict_gender(self, frame, bbox):
        padding = 20
        x1, y1, x2, y2 = bbox
        
        # Ensure coordinates are within frame
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(frame.shape[1] - 1, x2 + padding)
        y2 = min(frame.shape[0] - 1, y2 + padding)
        
        face_crop = frame[y1:y2, x1:x2]
        
        if face_crop.size == 0:
            return None, 0.0

        blob = cv2.dnn.blobFromImage(face_crop, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        
        gender = self.gender_list[gender_preds[0].argmax()]
        confidence = gender_preds[0].max()
        
        return gender, confidence
