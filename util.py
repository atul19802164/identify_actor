import cv2
import numpy as np
import base64
import json
import pickle
from wavlet import w2d
class_name_to_number={}
class_number_to_name={}
model=None
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def classify_image(image_base64_data, file_path=None):
    result=[]
    img = get_cropped_images(file_path, image_base64_data)
    scaled_raw_img = cv2.cvtColor(cv2.resize(img, (32, 32)), cv2.COLOR_BGR2GRAY)
    img_har = w2d(img, 'db1', 5)
    scaled_img_har = cv2.resize(img_har, (32, 32))
    combined_img = np.vstack((scaled_raw_img.reshape(32, 32), scaled_img_har.reshape(32, 32)))
    x = np.asarray(combined_img).reshape(64 * 32).astype(float)
    actor=class_number_to_name[np.argmax(model.predict_proba([x]))]
    result.append({
        'class':actor,
        'class_probability': np.around(model.predict_proba([x]) * 100, 2).tolist()[0],
        'class_dictionary': class_name_to_number
    })
    return result
def get_b64_test_image_for_ayushman():
    with open("b64.txt") as f:
        return f.read()
def get_cv2_image_from_base64_string(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_images(image_path, image_base64_data):
    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_color = img[y:y + h, x:x + w]
        if(len(faces)>0):
            return roi_color
def load_saved_artifacts():
    global class_name_to_number
    global class_number_to_name
    with open("class_dictionary.json", "r") as f:
        class_name_to_number = json.load(f)
        class_number_to_name = {v:k for k,v in class_name_to_number.items()}
    global model
    if model is None:
        with open('saved_model.pickle', 'rb') as f:
            model = pickle.load(f)
load_saved_artifacts()

