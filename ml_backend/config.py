
"""Change it to true for tensorflow serving """
TF_SERVING=False

MODEL_INFO={
	"breast_cancer":{
		"path":"models/classifiers/breat_cancer_classifier.pickle",
		"input_data":['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
						'smoothness_mean', 'compactness_mean', 'concavity_mean',
						'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
						'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
						'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
						'fractal_dimension_se', 'radius_worst', 'texture_worst',
						'perimeter_worst', 'area_worst', 'smoothness_worst',
						'compactness_worst', 'concavity_worst', 'concave points_worst',
   						'symmetry_worst', 'fractal_dimension_worst',
   					],
   		"CLASS_LABEL":['benign','malignant']

	}
}


SKIN_CANCER={
	"PATH": "models/keras_model/sc_model_1.h5",
	"CLASS_LABEL":['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc'],
	"MODEL": "skin_cancer_model_model"
}

CHEST_XRAY={
	"PATH": "models/keras_model/chest_model.h5",
	"CLASS_LABEL":['NORMAL','PNEUMONIA'],
	"MODEL": "chest_model"
}




