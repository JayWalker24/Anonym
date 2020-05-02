from flask import Flask     
from flask import request
from flask import jsonify
from flask_cors import CORS
import tensorflow as tf
import anonymForm

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from tensorflow.python.keras.backend import set_session
from keras.models import load_model
import json
import random


sess = tf.Session()
graph = tf.get_default_graph()

set_session(sess)
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


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
        anonymForm.createReport(response)  
        return jsonify(response)

@app.route("/message", methods=['GET','POST'])
def processMessage():
    if request.method == 'GET':
        return "It works!"

    if request.method == 'POST':
        response = request.json
        question = response.get('sendMessage').get('message')
        answer = send(question)
        return jsonify({"answer":answer})



def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    global sess
    global graph
    with graph.as_default():
        set_session(sess)
        res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):  
    
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def send(msg):
    if msg != '':
        res = chatbot_response(msg)
        return res

if __name__ == "__main__":
    app.run(host = 'localhost')      
    
