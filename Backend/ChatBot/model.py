import pickle
import json
import random

# NLP stuff
import nltk
# nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer

# TensorFlow stuff
import numpy as np
import tflearn
import tensorflow as tf
import os
import time

stemmer = LancasterStemmer()



intents_dict = dict()
folder_entities = "entities/"
for file_name in os.listdir(folder_entities):

    name_entity = file_name.split(".txt")[0]
    print(name_entity)
    intents_dict[name_entity] = list()
    file = open(folder_entities + file_name, "r")

    for line in file:
        line = line.strip()
        if line:
            print(line)
            intents_dict[name_entity].append(line)


words = []
classes = []
documents = []


for intent in intents_dict:

    classes.append(intent)
    for pattern in intents_dict[intent]:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our word list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent))
        # add to our classes list
# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

# create training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')

pickle.dump({
    'words': words,
    'classes': classes,
    'train_x': train_x,
    'train_y': train_y
}, open('training_data', 'wb'))


