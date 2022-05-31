import os
from datetime import timedelta
from typing import Union
from flask import Flask,jsonify,request,make_response
from util import Preprocessing
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from database import init,getalluser,registerdb,logindb
from flask_cors import CORS


#init flask and sql
app = Flask(__name__)
CORS(app)
mysql = init(app)

#load tensorflow model
preprocess = Preprocessing("model.h5")
prediction_results = preprocess.predict()

#JWT
app.config["JWT_SECRET_KEY"] = "capstone-secret-key" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    #current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
    return "Hello World"

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['password']
    user = logindb(mysql,email,pwd)
    if user != "":
        access_token = create_access_token(identity=email)
        data = {"message": "Login Successful" , "user": user, "access_token" : access_token}
        return jsonify(data),200
    return jsonify({"msg": "username atau password salah"}), 401

@app.route('/predict', methods=['GET'])
@jwt_required()
def predict():
  data = {'success': 'true','data': prediction_results}                                                                                                                                                                                                                                                 
  return jsonify(data)

@app.route("/predict/<product_name>", methods=['GET'])
def predictByProductName(product_name, days: Union[int, None] = None):
    try:
        data = next(product for product in prediction_results if product["product_name"] == product_name)
    except:
        return jsonify(status_code=404, content = {"message": f"Product '{product_name}' doesn\'t exist"})

    if (days):
        data["predictions"] = data["predictions"][:days]
        return data
    return data

@app.route("/<product_name>", methods=['POST'])
def input_product(product_name):
    input_date = request.form['input_date']
    sold = request.form['sold']
    try:
        data = next(product for product in prediction_results if product["product_name"] == product_name)
    except:
        return jsonify(status_code=404, content = {"message": f"Product '{product_name}' doesn\'t exist"})
    
    prediction = next(item for item in data["predictions"] if item["date"] == input_date)
    prediction["real"] = sold
    return data




@app.route('/register', methods=['POST'])
def register():
    username = request.form['name']
    email = request.form['email']
    pwd = request.form['password']
    return registerdb(mysql,username,email, pwd)
 
@app.route('/users',methods=['GET'])
def userlist():
    user = getalluser(mysql)
    return jsonify(user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
    #$Env:PORT=4000
    

#@app.route('/predict', methods=['POST'])
#def predictpost():
#    model = preprocess.predict(request.form['key1'])
#   return model
#
