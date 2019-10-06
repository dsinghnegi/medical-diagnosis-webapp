# Serving the model
We will be using tensorflow serving for our application.
TensorFlow Serving is a flexible, high-performance serving system for machine learning models, designed for production environments. For more detail checkout the git: https://github.com/tensorflow/serving

## Quickstart 
### Convet keras model to tensorflow
- Take keras trained model as input and generate tensorflow model 
	```
  python3 keras_to_tensorflow.py -i ../model_training/sc_model.h5 -o ../models/skin_cancer_model_model/1
  python3 keras_to_tensorflow.py -i ../model_training/chest_model.h5 -o ../models/chest_model/1
  ```
- Create a model.config file as shown below on models directory
	```
  model_config_list {
    config {
      name: 'chest_model'
      base_path: '/models/chest_model'
      model_platform: "tensorflow"
    }
    config {
      name: 'skin_cancer_model_model'
      base_path: '/models/skin_cancer_model_model'
      model_platform: "tensorflow"
    }
  }
  ```
- Run the tensorflow serving
  Replace path/to/folder/models/ with folder location
  ```
  # Replace path/to/folder/models/ with models directory path 
  sudo docker run -p 8501:8501 --rm -v "path/to/folder/models/:/models/" -t --entrypoint=tensorflow_model_server tensorflow/serving:latest-gpu --model_config_file=/models/models.config --enable_batching
  ```
- Test the server. Run the test code with an  image
  ```
  # add path to the image
  python3 serving_test.py -i your/image/path
  ```
  Output will be like
  ```
   ...
   {'predictions': [[0.222532585, 0.77746737]]}

  ```
 ## References
 - https://www.tensorflow.org/tfx/serving/api_rest
 - https://towardsdatascience.com/deploying-keras-models-using-tensorflow-serving-and-flask-508ba00f1037
