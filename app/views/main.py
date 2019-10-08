from flask import render_template, jsonify
from flask import request
from app import app
import random
import os
import base64

from ml_backend import disease_helper

dp=disease_helper.disease_predictor()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')



@app.route('/chestXray',methods=['POST'])
def chestXray():
	# print(Image_path=request.form['fileToUpload'])
	# graphJSON = jsonify(request.form['fileToUpload'])
	file=request.files['fileToUpload']
	filepath=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
	file.save(filepath)
	# with open(filepath, "rb") as image_file:
	#     encoded_string = base64.b64encode(image_file.read())
	prediction="Loading..."
	score="Loading..."

	return render_template('uploaded.html',predictions=prediction,score=score,image_path=os.path.join(app.config['UPLOAD_FOLDER'].split('/')[-1], file.filename),filelocation=filepath,cat='chest')

@app.route('/skincancer',methods=['POST'])
def skincancer():
	# print(Image_path=request.form['fileToUpload'])
	# graphJSON = jsonify(request.form['fileToUpload'])
	file=request.files['fileToUpload']
	filepath=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
	file.save(filepath)
	# with open(filepath, "rb") as image_file:
	#     encoded_string = base64.b64encode(image_file.read())
	# data=dp.read_image(filepath)
	# prediction,score=dp.skin_cancer(data)
	# score=round(score*100)
	prediction="Loading..."
	score="Loading..."

	return render_template('uploaded.html',predictions=prediction,score=score,image_path=os.path.join(app.config['UPLOAD_FOLDER'].split('/')[-1], file.filename),filelocation=filepath,cat="skin")


@app.route('/upload',methods=['POST'])
def upload_file2():
	# print(Image_path=request.form['fileToUpload'])
	# graphJSON = jsonify(request.form['fileToUpload'])
	file=request.files['fileToUpload']
	filepath=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
	file.save(filepath)
	# with open(filepath, "rb") as image_file:
	#     encoded_string = base64.b64encode(image_file.read())
	data=dp.read_image(filepath)
	prediction,score=dp.chest_xray(data)
	score=round(score*100)

	return render_template('uploaded.html',predictions=prediction,score=score,image_path=os.path.join(app.config['UPLOAD_FOLDER'].split('/')[-1], file.filename))

@app.route('/price')
def price():
	return render_template('price.html', title='Pricing')



@app.route('/service',methods=['POST'])
def service():
	print("********************************************************************")
	filepath=os.path.join(app.config['UPLOAD_FOLDER'],request.form['image_path'].split('/')[-1])
	service=request.form['service'].replace(" ",'')
	print('#',service,'#')
	data=dp.read_image(filepath)
	if 'chest' in service  :
		print('#########################################################')
		prediction,score=dp.chest_xray(data)
		score=round(score*100)
	else:
		print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
		prediction,score=dp.skin_cancer(data)
		score=round(score*100)
	print("********************************************************************")
	print(prediction,score)
	return render_template('result.html', prediction=prediction,scores=score)


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
	points = [(random.uniform(48.8434100, 48.8634100),
			random.uniform(2.3388000, 2.3588000))
			for _ in range(random.randint(2, 9))]
	return jsonify({'points': points})


@app.route('/contact')
def contact():
	return render_template('contact.html', title='Contact')