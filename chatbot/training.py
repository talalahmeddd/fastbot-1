# import nltk
# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# import json
# import pickle

# import numpy as np
# from keras.models import Sequential
# from keras.layers import Dense, Activation, Dropout
# from keras.optimizers import SGD
# import random

# words=[]
# classes = []
# documents = []
# ignore_words = ['?', '!']
# data_file = open('data.json').read()

# intents = json.loads(data_file)


# for intent in intents['intents']:
#     for pattern in intent['patterns']:

#         #tokenize each word
#         w = nltk.word_tokenize(pattern)
#         words.extend(w)
#         #add documents in the corpus
#         documents.append((w, intent['tag']))

#         # add to our classes list
#         if intent['tag'] not in classes:
#             classes.append(intent['tag'])

# # lemmaztize and lower each word and remove duplicates
# words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
# words = sorted(list(set(words)))
# # sort classes
# classes = sorted(list(set(classes)))
# # documents = combination between patterns and intents
# print (len(documents), "documents")
# # classes = intents
# print (len(classes), "classes", classes)
# # words = all words, vocabulary
# print (len(words), "unique lemmatized words", words)


# pickle.dump(words,open('texts.pkl','wb'))
# pickle.dump(classes,open('labels.pkl','wb'))

# # create our training data
# training = []
# # create an empty array for our output
# output_empty = [0] * len(classes)
# # training set, bag of words for each sentence
# for doc in documents:
#     # initialize our bag of words
#     bag = []
#     # list of tokenized words for the pattern
#     pattern_words = doc[0]
#     # lemmatize each word - create base word, in attempt to represent related words
#     pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
#     # create our bag of words array with 1, if word match found in current pattern
#     for w in words:
#         bag.append(1) if w in pattern_words else bag.append(0)
    
#     # output is a '0' for each tag and '1' for current tag (for each pattern)
#     output_row = list(output_empty)
#     output_row[classes.index(doc[1])] = 1
    
#     training.append([bag, output_row])
# # shuffle our features and turn into np.array
# random.shuffle(training)
# training = np.array(training)
# # create train and test lists. X - patterns, Y - intents
# train_x = list(training[:,0])
# train_y = list(training[:,1])
# print("Training data created")


# # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# # equal to number of intents to predict output intent with softmax
# model = Sequential()
# model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(len(train_y[0]), activation='softmax'))

# # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# #fitting and saving the model 
# hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
# model.save('model.h5', hist)

# print("model created")
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import re

import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout, Input
from keras.optimizers import Adam, RMSprop
from keras.optimizers import SGD
import random
from sklearn.metrics import confusion_matrix, multilabel_confusion_matrix, mean_squared_error
from sklearn.model_selection import train_test_split
import keras_tuner as kt
from tensorflow import keras

words = []
classes = []
documents = []
ignore_words = ['?', '!', '&', '(', ')', ',', '.', '/', '-', '`']
data_file = open('data.json', encoding='utf-8').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:

        w = nltk.word_tokenize(pattern)
        words.extend(w)

        documents.append((w, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# print (len(documents), "documents", documents)

# print (len(classes), "classes", classes)

# print (len(words), "unique lemmatized words", words)

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# training data initialization
training = []
output_empty = [0] * len(classes)
for doc in documents:

    bag = []

    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# print(pattern_words)
# print(bag)
# print(output_row)
#print(training)
random.shuffle(training)
training = np.array(training)
#print(training)
# create train and test lists. X - patterns, Y - intents
x = list(training[:,0])
y = list(training[:,1])
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=5)
print("Training data created")
print(len(x_train))
print(len(x_train[0]))
print(len(y_train))
print(len(y_train[0]))
print(len(y_test))
print(len(x_test))

model = Sequential()
model.add(Dense(512, input_shape=(len(x_train[0]),), activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(y_train[0]), activation='softmax'))

print(model.summary())

test_x = []
test_y = []

test_x = np.array(x_test)
test_y = np.array(y_test)

adam = Adam(lr=0.001)
rmsprop = RMSprop(lr=0.001)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(x_train), np.array(y_train), epochs=200, batch_size=8, verbose=1, validation_data=(test_x, test_y))

loss = hist.history['loss']
val_loss = hist.history['val_loss']
accuracy = hist.history['accuracy']
val_accuracy = hist.history['val_accuracy']
data = {
    'accuracy': accuracy[-1],
    'loss': loss[-1],
    'val_accuracy': val_accuracy[-1],
    'val_loss': val_loss[-1],
}
#keras-tuner function for model
def build_model(hp):
    model = keras.Sequential()
    model.add(keras.layers.Dense(units=hp.Int('units',
                                              min_value=32,
                                              max_value=512,
                                              step=32),
                                 activation='relu',
                                 input_shape=(len(x_train[0]),)))
    model.add(keras.layers.Dropout(rate=hp.Float('dropout_rate',
                                                 min_value=0.1,
                                                 max_value=0.5,
                                                 step=0.1)))
    model.add(keras.layers.Dense(len(classes), activation='softmax'))

    model.compile(optimizer=keras.optimizers.Adam(
                     hp.Float('learning_rate',
                              min_value=1e-4,
                              max_value=1e-2,
                              sampling='LOG',
                              default=1e-3)),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model
#define the tuner
tuner = kt.Hyperband(build_model,
                    objective='val_accuracy',
                    max_epochs=200,
                    factor=3,
                    directory='my_dir',
                    project_name='chatbot_tuning')

#perform hyperparametre search
tuner.search(np.array(test_x), np.array(test_y), epochs=200, validation_data=(np.array(x_test), np.array(y_test)))

#get best model
best_model = tuner.get_best_models(1)[0]
best_hyperparameters = tuner.get_best_hyperparameters(1)[0]

#Train on best model
best_model.fit(np.array(test_x), np.array(test_y), epochs=200, batch_size=5, verbose=1)

# Save data as JSON
with open('accuracy_report.json', 'w') as json_file:
    json.dump(data, json_file)

model.save('chatbot_model.h5', hist)

print("model created")



y_predict = model.predict(x_train)
rmse = (np.sqrt(mean_squared_error(y_train, y_predict)))

print("Performance of training data")
print('RMSE is {}'.format(rmse))
print("\n")

y_predict_test = model.predict(x_test)
rmse = (np.sqrt(mean_squared_error(y_test, y_predict_test)))
y_predict_test = (y_predict_test > 0.5)

print("Performance of testing data")
print('RMSE is {}'.format(rmse))
print("\n")

y_predict = np.argmax(model.predict(x,batch_size=8),axis=1)
# test_x_output = np.argmax(test_x_output, axis=1)
test_y = np.argmax(y, axis=1)


predictedValues = confusion_matrix(test_y, y_predict)
sns.heatmap(predictedValues)


print(predictedValues)


# Plot and save the training loss graph
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training Loss')
plt.plot(epochs, val_loss, 'r', label='Validation Loss')
plt.title('Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
save_path = '../client/public/images/training_loss.png'
plt.savefig(save_path)
plt.close()

# Plot and save the training accuracy graph
plt.plot(epochs, accuracy, 'y', label='Training Accuracy')
plt.plot(epochs, val_accuracy, 'r', label='Validation Accuracy')
plt.title('Training Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
save_path = '../client/public/images/training_accuracy.png'
plt.savefig(save_path)
plt.close()

plt.figure(figsize=(5,5))
plt.scatter(y_test, y_predict_test)
plt.plot([np.min(y_predict_test), np.max(y_predict_test)], [np.min(y_predict_test), np.max(y_predict_test)])
plt.xlabel('Actual')
plt.ylabel('Predicted')
save_path = '../client/public/images/test.png'
plt.savefig(save_path)
plt.close()