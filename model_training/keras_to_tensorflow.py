import tensorflow as tf
from optparse import OptionParser
from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy

def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)

def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)

def convert_keras_to_tensorlow_model(input_model,output_directory):
	tf.keras.backend.set_learning_phase(0)  
	model = tf.keras.models.load_model(input_model,custom_objects={"top_2_accuracy": top_2_accuracy,"top_3_accuracy":top_3_accuracy})
	export_path = output_directory

	with tf.keras.backend.get_session() as sess:
		tf.saved_model.simple_save(
			sess,
			export_path,
			inputs={'input_image': model.input},
	outputs={t.name: t for t in model.outputs})


def get_args():
	parser = OptionParser()
	parser.add_option('-i', '--input_model', dest='input_model',
				  default="input_model", help='Keras model location')
	parser.add_option('-o', '--outpt_model', dest='outpt_model',
				  default="outpt_model", help='Output directory')

	(options, args) = parser.parse_args()
	return options

if __name__ == '__main__':
	args = get_args()
	input_model=args.input_model
	output_directory=args.outpt_model
	convert_keras_to_tensorlow_model(input_model,output_directory)