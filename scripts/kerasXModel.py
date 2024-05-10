from keras.models import load_model 
from PIL import Image, ImageOps  
import numpy as np

class predict:
    def __init__(self, xray):
        np.set_printoptions(suppress=True)

        # Load the model
        self.model = load_model("keras_Model.h5", compile=False)
        self.class_names = open("labels.txt", "r").readlines()

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(xray).convert("RGB")

        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        prediction = self.model.predict(data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        self.prediction_result = class_name[2:]
        self.confidence_score = confidence_score
