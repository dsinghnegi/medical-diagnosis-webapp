import argparse
import json

import numpy as np
import requests
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing import image

# Argument parser for giving input image_path from command line
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path of the image")
args = vars(ap.parse_args())

image_path = args['image']
# Preprocessing our input image
img = preprocess_input(image.img_to_array(image.load_img(image_path)))

# this line is added because of a bug in tf_serving(1.10.0-dev)
img = img.astype('float16')

payload = {
    "instances": [{'input_image': img.tolist()}]
}

# sending post request to TensorFlow Serving server
r = requests.post('http://localhost:8501/v1/models/chest_model:predict', json=payload)
pred = json.loads(r.content.decode('utf-8'))
print(pred)
