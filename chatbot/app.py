# import nltk

# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# import pickle
# import numpy as np

# from keras.models import load_model
# model = load_model('chatbot_model.h5')
# import json
# import random
# intents = json.loads(open('data.json').read())
# words = pickle.load(open('texts.pkl','rb'))
# classes = pickle.load(open('labels.pkl','rb'))

# def clean_up_sentence(sentence):
#     # tokenize the pattern - split words into array
#     sentence_words = nltk.word_tokenize(sentence)
#     # stem each word - create short form for word
#     sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
#     return sentence_words

# # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

# def bow(sentence, words, show_details=True):
#     # tokenize the pattern
#     sentence_words = clean_up_sentence(sentence)
#     # bag of words - matrix of N words, vocabulary matrix
#     bag = [0]*len(words)  
#     for s in sentence_words:
#         for i,w in enumerate(words):
#             if w == s: 
#                 # assign 1 if current word is in the vocabulary position
#                 bag[i] = 1
#                 if show_details:
#                     print ("found in bag: %s" % w)
#     return(np.array(bag))

# def predict_class(sentence, model):
#     # filter out predictions below a threshold
#     p = bow(sentence, words,show_details=False)
#     res = model.predict(np.array([p]))[0]
#     ERROR_THRESHOLD = 0.25
#     results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
#     # sort by strength of probability
#     results.sort(key=lambda x: x[1], reverse=True)
#     return_list = []
#     for r in results:
#         return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
#     return return_list

# def getResponse(ints, intents_json):
#     tag = ints[0]['intent']
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         if(i['tag']== tag):
#             result = random.choice(i['responses'])
#             break
#     return result

# def chatbot_response(msg):
#     ints = predict_class(msg, model)
#     res = getResponse(ints, intents)
#     return res


# from flask import Flask, render_template, request

# app = Flask(__name__)
# app.static_folder = 'static'

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return chatbot_response(userText)


# if __name__ == "__main__":
#     app.run(host="localhost", port=8000)

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from flask import Flask, render_template, request
import re


app = Flask(__name__)
app.static_folder = 'static'

# Load the trained model
model = load_model('chatbot_model.h5')

# Load the words and classes
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

with open('data.json') as file:
    intents = json.load(file)

def clean_up_sentence(sentence):
    sentence = re.sub(r'[^\w\s?]', '', sentence)  # Remove special characters except '?'
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word.isalpha() or word == '?']
    return sentence_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# import pickle
# import numpy as np
# from keras.models import load_model
# import json
# import random
# from flask import Flask, render_template, request

# app = Flask(__name__)
# app.static_folder = 'static'

# # Load the trained model
# model = load_model('chatbot_model.h5')

# # Load the words and classes
# words = pickle.load(open('words.pkl', 'rb'))
# classes = pickle.load(open('classes.pkl', 'rb'))

# with open('data.json') as file:
#     intents = json.load(file)

# # Download stopwords if not already downloaded
# nltk.download('stopwords')

# # Get the stopwords
# stop_words = set(stopwords.words('english'))

# def clean_up_sentence(sentence):
#     sentence_words = nltk.word_tokenize(sentence)
#     sentence_words = [word.lower() for word in sentence_words]
#     sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words if word not in stop_words]
#     return sentence_words

# def bow(sentence, words, show_details=True):
#     sentence_words = clean_up_sentence(sentence)
#     bag = [0] * len(words)
#     for s in sentence_words:
#         for i, w in enumerate(words):
#             if w == s:
#                 bag[i] = 1
#                 if show_details:
#                     print("found in bag: %s" % w)
#     return np.array(bag)

def predict_class(sentence, model, words, classes):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:  # No matching intent found
        return "I'm sorry, but I don't understand. Please try again with a different message."
    
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg, model, words, classes, intents):
    ints = predict_class(msg, model, words, classes)
    res = get_response(ints, intents)
    return res

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    userText = userText.strip()  # Remove leading/trailing whitespace
    # Check if userText contains invalid characters
    if re.search(r'[^?\w\s,".]|\d', userText):
        return "Please enter a valid message."
    else:
        response = chatbot_response(userText, model, words, classes, intents)
        return response

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
