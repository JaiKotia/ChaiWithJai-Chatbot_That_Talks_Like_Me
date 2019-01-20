#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 17:43:26 2019

@author: jai
"""

import pandas as pd
import re
import numpy as np

messageDictionary = {}
myName = 'Jai Kotia'

friendName = 'Rishika'

data = pd.read_csv('WhatsApp Chat with ' + friendName + '.txt', sep="m - ", header=None, engine='python', names=['a', 'b'])
data = data.drop('a', axis=1)
data['b'] = data['b'].map(lambda x: str(x).replace('<Media omitted>', ' '))
data = data.replace(to_replace='None', value=np.nan).dropna()
data = data.replace(to_replace='Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info.', value=np.nan).dropna()

#Run function
createDictionary(data)

#Convert messages to lowercase
messageDictionary = dict((k.lower(), v.lower()) for k,v in messageDictionary.items())

#Strip whitespaces
messageDictionary = dict((k.strip(), v.strip()) for k,v in messageDictionary.items())

#Remove empty items in dictionary
messageDictionary = {k:v for k,v in messageDictionary.items() if v != ' '}
messageDictionary = {k:v for k,v in messageDictionary.items() if k != ' '}

        
def createDictionary(data):
    friendsMessage, myMessage = '', ''
    for row in data.iterrows():
        #Check who sent the message
        if(row[1]['b'].startswith(friendName + ': ')):
            #Check if the reply is complete
            if myMessage and friendsMessage:
                myMessageCleaned = cleanMessage(myMessage)
                friendsMessageCleaned = cleanMessage(friendsMessage)
                messageDictionary[friendsMessageCleaned] = myMessageCleaned
                myMessage, friendsMessage = '', ''
            friendsMessage = friendsMessage + ' ' + row[1]['b'].split(friendName + ': ')[1]
                
        else:
            myMessage = myMessage + ' ' + row[1]['b'].split(myName + ': ')[1]
    
def cleanMessage(message):
    # Remove punctuation
    cleanedMessage = re.sub('([.,!?*$#%@&:;_|\(\)\[\]\{\}^~+=<>\'\"-\\/])','', message)
    #Remove emojis
    cleanedMessage = remove_emoji(cleanedMessage)
    # Remove multiple spaces in message
    cleanedMessage = re.sub(' +',' ', cleanedMessage)
    return cleanedMessage

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

#Save dictionary as files
np.save('conversationDictionary.npy', messageDictionary)

conversationFile = open('conversationData.txt', 'w')
for key,value in messageDictionary.items():
    conversationFile.write(key.strip() + ' ' + value.strip() + ' ')
    

