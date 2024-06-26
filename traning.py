import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer # word lemmatizer example: convert -> work working worke works to: work

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, TFSMLayer
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']


for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern) # for example sentence: "Show my stock portfolio" -> ['Show', 'my', 'stock', 'portfolio']
        words.extend(word_list) # like push in javascript
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words)) # sort by alphabet

# print(classes) # tag names


pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


training = []
output_empty = [0] * len(classes)

print(words, 0)
for document in documents:
    print(document, 1) # 1

    bag = []
    word_patterns = document[0]
    print(word_patterns, 2) # 2 
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    print(word_patterns, 3) # 3 

    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    print(bag, 4) # 4
    print(output_row, 5) # 5
    print("----------------------------------------")
    output_row[classes.index(document[1])] = 1
    print(output_row, 6)
    training.append([bag, output_row])
    print(training, 7)
    print("<<<<<<<<<<<--------->>>>>>>>>>>>")

# print(training)

random.shuffle(training)
"""
Converts the `training` list into a NumPy array.

This is a common preprocessing step before feeding the data into a machine learning model. Converting the list to a NumPy array allows the model to efficiently operate on the data.
"""

training = np.array(training, dtype=object)

train_x = list(training[:, 0]) # words
train_y = list(training[:, 1]) # tags


pickle.dump(train_x, open('train_x.pkl', 'wb'))
pickle.dump(train_y, open('train_y.pkl', 'wb'))

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) # not works
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Export the model to a HDF5 file
# model.save('chatbotmodel.h5') # works

model.save('chatbotmodel.keras', hist)

print("Done")