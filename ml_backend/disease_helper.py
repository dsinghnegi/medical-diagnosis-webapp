from ml_backend import config
import argparse
import json

import numpy as np
import requests
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
import pickle
import tensorflow as tf
from tensorflow.keras.metrics import top_k_categorical_accuracy
# #
# tf.keras.backend.clear_session()
graph = tf.get_default_graph()
TF_SERVING=config.TF_SERVING

def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)

def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)


def read_keras__model(input_model):
	"""  We will be use this function when serving is off"""
	tf.keras.backend.set_learning_phase(0)  
	model = tf.keras.models.load_model(input_model,custom_objects={"top_2_accuracy": top_2_accuracy,"top_3_accuracy":top_3_accuracy})

	# model._make_predict_function()
	return model

def read_pkl(path):
	with open(path, 'rb') as handle:
		classifier=pickle.load(handle)
	return classifier


class disease_predictor(object):
	"""docstring for disease_predictor"""
	def __init__(self):
		super(disease_predictor, self).__init__()
		self.models={}
		# if TF_SERVING == False:
		# 	self.load_keras_model()

	def load_keras_model(self):
		for model_info in [config.SKIN_CANCER]: #config.CHEST_XRAY
			self.models[model_info["MODEL"]]=read_keras__model(model_info["PATH"])

	def serving_based_prediction(self,model_info,data):
		img = preprocess_input(image.img_to_array(data))
		img = img.astype('float16')

		payload = {
		"instances": [{'input_image': img.tolist()}]
		}

		# sending post request to TensorFlow Serving server
		r = requests.post('http://localhost:8501/v1/models/{}:predict'.format(model_info["MODEL"]), json=payload)
		pred = json.loads(r.content.decode('utf-8'))['predictions']
		label=model_info["CLASS_LABEL"][np.argmax(pred[0])]
		return label.upper(),np.max(pred[0])


	def image_prediction(self,model_info,data):
		if TF_SERVING:
			return self.serving_based_prediction(model_info,data)
		else:
			return 	self.keras_model_based_prediction(model_info,data)	

	def keras_model_based_prediction(self,model_info,data):
		img = image.img_to_array(data)
		img = np.expand_dims(img, axis=0)
		img = preprocess_input(img)
		# print(model_info)
		model = read_keras__model(model_info["PATH"])
		# model=self.models[model_info["MODEL"]]
		# with graph.as_default():
		pred=model.predict(img)
		label=model_info["CLASS_LABEL"][np.argmax(pred[0])]
		return label.upper(),np.max(pred[0])


	def pickle_based_classification(self,model_info,data):
		classifier=read_pkl(model_info['path'])
		label=model_info["CLASS_LABEL"][classifier.predict([data])[0]]

		return label.upper()

	def skin_cancer(self,data):
		return self.image_prediction(config.SKIN_CANCER,data)

	def chest_xray(self,data):
		return self.image_prediction(config.CHEST_XRAY,data)

	def breast_cancer(self,data):
		model_info=config.MODEL_INFO['breast_cancer']
		return self.pickle_based_classification(model_info,data)

	def read_image(self,path):
		return image.load_img(path, target_size=(229, 229))

if __name__ == '__main__':
	dp=disease_predictor()
	image_path='person1_bacteria_1.jpeg'
	data=image.load_img(image_path)
	print(dp.chest_xray(data))
	print(dp.skin_cancer(data))
	data=np.array([1.799e+01, 1.038e+01, 1.228e+02, 1.001e+03, 1.184e-01, 2.776e-01,
       3.001e-01, 1.471e-01, 2.419e-01, 7.871e-02, 1.095e+00, 9.053e-01,
       8.589e+00, 1.534e+02, 6.399e-03, 4.904e-02, 5.373e-02, 1.587e-02,
       3.003e-02, 6.193e-03, 2.538e+01, 1.733e+01, 1.846e+02, 2.019e+03,
       1.622e-01, 6.656e-01, 7.119e-01, 2.654e-01, 4.601e-01, 1.189e-01])
	print(dp.breast_cancer(data))	

