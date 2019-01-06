import numpy as np
import pickle
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
import model

import sys
import logging

# Load in data structures
with open("data/wordList.txt", "rb") as fp:
    wordList = pickle.load(fp)
wordList.append('<pad>')
wordList.append('<EOS>')

# Load in hyperparamters
vocabSize = len(wordList)
batchSize = 24
maxEncoderLength = 15
maxDecoderLength = 15
lstmUnits = 112
numLayersLSTM = 3

# Create placeholders
encoderInputs = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxEncoderLength)]
decoderLabels = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxDecoderLength)]
decoderInputs = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxDecoderLength)]
feedPrevious = tf.placeholder(tf.bool)

encoderLSTM = tf.nn.rnn_cell.BasicLSTMCell(lstmUnits, state_is_tuple=True)
#encoderLSTM = tf.nn.rnn_cell.MultiRNNCell([singleCell]*numLayersLSTM, state_is_tuple=True)
decoderOutputs, decoderFinalState = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(encoderInputs, decoderInputs, encoderLSTM, vocabSize, vocabSize, lstmUnits, feed_previous=feedPrevious)

decoderPrediction = tf.argmax(decoderOutputs, 2)

# Start session and get graph
sess = tf.Session()
#y, variables = model.getModel(encoderInputs, decoderLabels, decoderInputs, feedPrevious)

# Load in pretrained model
saver = tf.train.Saver()
saver.restore(sess, tf.train.latest_checkpoint('models'))
zeroVector = np.zeros((1), dtype='int32')

def pred(inputString):
    inputVector = model.getTestInput(inputString, wordList, maxEncoderLength)
    print(inputVector)
    feedDict = {encoderInputs[t]: inputVector[t] for t in range(maxEncoderLength)}
    feedDict.update({decoderLabels[t]: zeroVector for t in range(maxDecoderLength)})
    feedDict.update({decoderInputs[t]: zeroVector for t in range(maxDecoderLength)})
    feedDict.update({feedPrevious: True})
    print(feedDict)
    ids = (sess.run(decoderPrediction, feed_dict=feedDict))
    print(ids)
    return model.idsToSentence(ids, wordList)

# webapp
app = Flask(__name__, template_folder='./')


@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    '''
    print(request)
    print(request.data)
    print(request.form)
    print(request.form['message'])
    '''
    response =  pred(str(request.form['message']))
    return jsonify(response)

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
