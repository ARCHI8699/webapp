#Important Modules
from flask import Flask,render_template, url_for ,flash , redirect
#from forms import RegistrationForm, LoginForm
#from sklearn.externals import joblib
#import sklearn.external.joblib as extjoblib
import joblib
from flask import request
import numpy as np
import tensorflow
import os
from flask import send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
#from this import SQLAlchemy
#from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__,template_folder='template')


# RELATED TO THE SQL DATABASE
#app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
#db=SQLAlchemy(app)

#from model import User,Post


dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

#graph = tf.get_default_graph()
#with graph.as_default():;
from tensorflow.keras.models import load_model
model = load_model('model111.h5')
model222=load_model("my_model.h5")

#FOR THE FIRST MODEL

# call model to predict an image
def api(full_path):

    data = image.load_img(full_path, target_size=(50, 50, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    #with graph.as_default():
    predicted = model.predict(data)
    return predicted
#FOR THE SECOND MODEL
def api1(full_path):
    data = image.load_img(full_path, target_size=(64, 64, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    #with graph.as_default():
    predicted = model222.predict(data)
    return predicted


# home page

#@app.route('/')
#def home():
 #  return render_template('index.html')


# procesing uploaded file and predict it
@app.route('/upload', methods=['POST','GET'])
def upload_file():

    if request.method == 'GET':

        return render_template('index.html')
    else:

        try:

            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {0: 'PARASITIC', 1: 'Uninfected', 2: 'Invasive carcinomar', 3: 'Normal'}
            result = api(full_name)
            print(result)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            return render_template('predict.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        except:

            flash("Invalid selection!!", "danger")      
            return redirect(url_for("Malaria"))

@app.route('/upload11', methods=['POST','GET'])
def upload11_file():

    if request.method == 'GET':

        return render_template('index2.html')
    else:

        try:

            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {0: 'Normal', 1: 'Pneumonia'}
            result = api1(full_name)
            
            if (result>50):
                label= indices[1]
                accuracy= result
            else:
                label= indices[0]
                accuracy= 100-result
            return render_template('predict1.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        except:
            flash("Invalid selection !!", "danger")      
            return redirect(url_for("Pneumonia"))


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)






#//////////////////////////////////////////////

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

#db=SQLAlchemy(app)

#class User(db.Model):
##   username = db.Column(db.String(20), unique=True, nullable=False)
 #   email = db.Column(db.String(120), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
 #   password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    #def __repr__(self):
	#	return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@app.route("/")
def home():
	return render_template("home.html")
 
@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/Malaria")
def Malaria():
    return render_template("index.html")

@app.route("/Pneumonia")
def Pneumonia():
    return render_template("index2.html")



'''@app.route("/register", methods=["GET", "POST"])
def register():
	form =RegistrationForm()
	if form.validate_on_submit():
		#flash("Account created for {form.username.data}!".format("success"))
		flash("Account created","success")		
		return redirect(url_for("home"))
	return render_template("register.html", title ="Register",form=form )

@app.route("/login", methods=["POST","GET"])
def login():
	form =LoginForm()
	if form.validate_on_submit():
		#if form.email.data =="sho" and form.password.data=="password":
		flash("You Have Logged in !","success")
		return redirect(url_for("home"))
	#else:
	#	flash("Login Unsuccessful. Please check username and password","danger")
	return render_template("login.html", title ="Login",form=form )'''



if __name__ == "__main__":
	app.run(debug=True)
