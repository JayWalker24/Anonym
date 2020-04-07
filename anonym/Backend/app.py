from flask import Flask     
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)     
CORS(app)

@app.route("/")                   
def hello():                    
    return "Bruh!"       

'''
Python back end is running on localhost:5000
UI is running on localhost:3000. but using an alias to 
appear as localhost:5000
'''
@app.route("/api", methods=['GET','POST'])
def processData():
    if request.method == 'GET':
        return "It works!"

    if request.method == 'POST':
        response = request.json
        print(response)
        return jsonify(response)


if __name__ == "__main__":        
    app.run(host = 'localhost')                     