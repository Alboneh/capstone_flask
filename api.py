from flask import Flask
from util import Preprocessing

preprocess = Preprocessing("model.h5")
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello World"
  
@app.route('/predict', methods=['GET'])
def predict():
  return preprocess.predict()


if __name__ == '__main__':
    app.run(port=3000)