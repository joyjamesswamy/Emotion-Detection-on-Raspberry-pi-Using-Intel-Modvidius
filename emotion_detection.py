import cv2
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from openvino.runtime import Core
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Emotion detection using OpenVINO.")
parser.add_argument("-i", "--input", type=str, required=True, help="Path to input video file or '0' for webcam.")
parser.add_argument("-m", "--model", type=str, required=True, help="Path to the OpenVINO model XML file.")
args = parser.parse_args()

# Load model
core = Core()
compiled_model = core.compile_model(args.model, "CPU")
input_layer = compiled_model.input(0)

# Emotions labels
emotions = ['happy', 'surprise', 'sad', 'anger', 'disgust', 'fear', 'neutral']

# Transformations for input
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Face detection using Haar cascade
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Determine input source
input_source = 0 if args.input == "0" else args.input
video_capture = cv2.VideoCapture(input_source)

# Settings for text overlay
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.2
font_color = (0, 255, 0)
thickness = 3
line_type = cv2.LINE_AA

max_emotion = ''

def detect_emotion(video_frame):
    input_data = transform(video_frame).unsqueeze(0).numpy()
    result = compiled_model([input_data])[compiled_model.outputs]
    probabilities = F.softmax(torch.tensor(result), dim=1).cpu().numpy().flatten()
    return probabilities

def get_max_emotion(x, y, w, h, video_frame):
    crop_img = video_frame[y:y + h, x:x + w]
    pil_crop_img = Image.fromarray(crop_img)
    rounded_scores = detect_emotion(pil_crop_img)
    max_index = np.argmax(rounded_scores)
    return emotions[max_index]

def display_emotion(x, y, w, h, video_frame, max_emotion):
    org = (x, y - 15)
    cv2.putText(video_frame, max_emotion, org, font, font_scale, font_color, thickness, line_type)

def detect_bounding_box(video_frame, counter):
    global max_emotion
    gray_image = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(video_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if counter == 0:
            max_emotion = get_max_emotion(x, y, w, h, video_frame)
        display_emotion(x, y, w, h, video_frame, max_emotion)

    return faces

counter = 0
evaluation_frequency = 5

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    detect_bounding_box(frame, counter)
    cv2.imshow("Emotion Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    counter = (counter + 1) % evaluation_frequency

video_capture.release()
cv2.destroyAllWindows()
