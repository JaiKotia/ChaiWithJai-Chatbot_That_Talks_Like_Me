# Chai With Jai

A chatbot that has been trained on my whatsapp chat data to learn to respond to text messages like I do.

## Whatsapp Chat Data Processing
Script that takes exported Whatsapp chat data and generates a dictionary of responses and replies. It outputs WordList and ConversationData files which will be used ahead.

## Word2Vec
Creates vectors for each word in the WordList prepared from the chat processing script.

## Seq2Seq
We use this model to map the sentences in ConversationData to the Word Vectors created. Here we add PAD and EOS tokens as we encode each conversation item from the dictionary. Look for Hyperparameters to modify the model as per requirements. Output of this is a model folder containing meta, data and checkpoint files.

## Flask Server
We use a flask server deployed using Heroku where we host the chatbot. It takes a input sentence and generates a likely response. We use the model output from Seq2Seq to generate responses from our chatbot. (Note: The current deployed model has been trained for only 88,000 steps. Further training, upto 500,000 would ensure better results.)

### Check out the live demo at: https://evening-temple-33627.herokuapp.com
