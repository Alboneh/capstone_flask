
from flask import Flask,jsonify
from util import Preprocessing

preprocess = Preprocessing("model.h5")
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello World"
  
@app.route('/predict', methods=['GET'])
def predict():
  data = {'success': 'true','data': preprocess.predict()}                                                                                                                                                                                                                                                 
  return jsonify(data)


if __name__ == '__main__':
    app.run(port=3000)