'''
Helper functions for twitter tweets classification
Author: Tushar Makkar <tusharmakkar08[at]gmail.com>
Date: 21.02.2015
'''

import json, os, re

def cleanTweet(tweet):
    '''
    Returns the cleaned version of tweet
    Args : 
        Original Tweet
    Returns : 
        A string with cleaned tweet
    '''
    cleanedTweet = ""
    cleanedTweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',tweet) # Remove urls
    cleanedTweet = cleanedTweet.lower() # Convert to lowercase
    cleanedTweet = re.sub('@[^\s]+',' ', cleanedTweet) # Remove username
    cleanedTweet = re.sub('[\s]+', ' ', cleanedTweet) # remove extra white space
    cleanedTweet = re.sub(r'#([^\s]+)', r'\1', cleanedTweet) # remove #
    cleanedTweet = cleanedTweet.strip('\'"') # trim
    return cleanedTweet

def getProbability(cleanedTweet):
    '''
    Returns the Probability Array of [negative,neutral,positive]
    Args : 
        Cleaned Tweet
    Returns : 
        An Array with probability of [negative,neutral,positive]
    '''
    jsonString = os.popen('curl -d "text='+cleanedTweet+'" http://text-processing.com/api/sentiment/').read()
    jsonDict = json.loads(jsonString)
    return [jsonDict["probability"]["neg"], jsonDict["probability"]["neutral"], jsonDict["probability"]["pos"],jsonDict["label"]]
    
def checkMatch(listOfWords, tweet):
    '''
    Returns bool variable
    Args:
        listOfWords : list of words
        tweet : string to be matched in
    Returns:
        boolean variable whether listOfWords is in tweet or not
    '''
    for word in listOfWords : 
        if word in tweet : 
            return True
    return False
    
def tweetClassifier(tweet):
    '''
    Returns the type of tweet
    Args:
        Original Tweet extracted from API
    Returns:
        An string denoting following : Love, Anger, Happy, Sad, Neutral
    '''
    cleanedTweet = cleanTweet(tweet)
    probabilitySentiment = getProbability(cleanedTweet)
    loveWords = ["love","mua","aww","friend","lust","fond","affection","passion","infatuation","yearning"];
    angerWords = ["anger","screw","bang","suck","shag","hump","angry","fuck","bastard","annoy","fury","rage","violence"];
    if(probabilitySentiment[3] == 'pos' and checkMatch(loveWords, cleanedTweet)):
        return "love"
    elif (probabilitySentiment[3] == 'neg' and checkMatch(angerWords, cleanedTweet)):
        return "anger"
    elif (probabilitySentiment[3] == 'pos'):
        return "happy"
    elif (probabilitySentiment[3] == 'neg'):
        return "sad"
    else: 
        return "neutral"

if __name__ == '__main__':
    tweet = "@redditindia muahh You suck"
    print tweetClassifier(tweet)
    
