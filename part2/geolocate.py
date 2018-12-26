#!/usr/bin/env python3
# Program to implement tweet classification  
import nltk
import re 
import sys
from collections import Counter
import pandas as pd
nltk.download('punkt')

# Read files
train_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]
train = open(train_file, 'r', errors='ignore').read()
test = open(test_file, 'r', errors='ignore').read()
location_wise_data, location_counts = {},{}
bag_of_words = []

# Preprocessing data by removing spacial characters 
def preprocess_data(fileData):
    clean_data = re.sub(r'[^a-zA-Z\d,_\s]', '', fileData)
    clean_data = re.sub('([_]+)_','_', clean_data)
    clean_data = re.sub('([ ]+)',' ', clean_data)
    clean_data = clean_data.replace("\n"," ")
    return clean_data

# Created a dictionary of dictionary to store 
# Location : {word : count}
def populate_train_data(clean_train):
    prev_start, prev_city = -1, ''
    bag_of_words_str = ''
    
    # Regular expression matches with the format of city,_state
    for m in re.compile(r'\w{4,},_\w+ ').finditer(clean_train):
        if(prev_start != -1 and prev_city != ''): # empty initially
            if prev_city not in location_wise_data:
                data = {}
                tweet = clean_train[prev_start+len(prev_city)+1:m.start()]
                tweet = tweet.replace(",","")
                location_wise_data[prev_city] = tweet
                location_counts[prev_city] = 1
                bag_of_words_str += tweet
            else:
                data = location_wise_data.get(prev_city)
                tweet = clean_train[prev_start+len(prev_city)+1:m.start()]
                tweet = tweet.replace(",","")
                location_wise_data[prev_city] =location_wise_data.get(prev_city)+ ' ' +tweet
                location_counts[prev_city] = location_counts.get(prev_city)+1
                bag_of_words_str += tweet            
        prev_start = m.start()
        prev_city = m.group()
        prev_city = prev_city.replace(" ","")
        
    bag_of_words_str = re.sub('([ ]+) ',' ', bag_of_words_str)
    bag_of_words = bag_of_words_str.split(" ")

# Function to generate tokens from tweet 
# Find the probability of each word as count of word in location / number of words in a location 
def generate_tokens_prob():
    for k,v in (location_wise_data.items()):        
        list_of_words = v.lower().split(" ")
        # Remove stop words
        list_of_words = [x for x in list_of_words if x not in ['', '_', ',','\'','a','an','and','are','the','as', 'at', 'be' ,'by' ,'us','it','too','she' ,'for', 'from', 'has','he', 'in', 'yes','is', 'its', 'of', 'on', 'that', 'to', 'was', 'were', 'will', 'with','my','you','mine','yours','we','can','this','our','because','him','his','her']]
        total_words = len(list_of_words)
        location_wise_data[k] = Counter(list_of_words)
        counter_dict = location_wise_data.get(k)
        for k2,v2 in counter_dict.items(): 
            counter_dict[k2] = v2 / total_words


clean_train = preprocess_data(train)
clean_test = test
populate_train_data(clean_train)
generate_tokens_prob()


# Test data is stored in dataframe
prev_start, prev_city = -1, '' 
cols = ['actual','clean_tweet','tweet', 'predicted']
list_data = []
for m in re.compile(r'\w{4,},_\w+ ').finditer(clean_test):
    if(prev_start != -1 and prev_city != ''): # empty initially
        tweet = clean_test[prev_start+len(prev_city)+1:m.start()]
        clean_tweet = re.sub(r'[^a-zA-Z\d\s]', '', tweet)
        list_data.append([prev_city, clean_tweet, tweet, ''])
    prev_start = m.start()
    prev_city = m.group()
    prev_city = prev_city.replace(" ","")
    
# To store last row
tweet = clean_test[prev_start+len(prev_city)+1:len(clean_test)]
clean_tweet = re.sub(r'[^a-zA-Z\d\s]', '', tweet)
clean_tweet = clean_tweet.replace("\n"," ")
list_data.append([prev_city, clean_tweet, tweet, ''])
    
    
test_df = pd.DataFrame(list_data, columns=cols)

# Applying naive bayes to find the probablity of location given list of words and then returning the location having maximum probablity
for index, row in test_df.iterrows():
    wordList = row['clean_tweet'].lower().split(" ")
    probabilies_by_city = {}
    for city in location_counts.keys():
        prob = 1
        for word in wordList:
            try:
                # Naive bayes assumes that words are independent given location
                prob = prob * location_wise_data.get(city).get(word)
            except:
                # If a word is not found in the given location, allocate a lowest probability to that word
                prob = prob * 0.0000001
        # Probablity of any location is 1/length of cities
        probabilies_by_city[city] = prob * (1/len(location_wise_data))
    row['predicted'] = max(probabilies_by_city, key = probabilies_by_city.get)
 
# FInding accuracy of test data 
correct, wrong = 0, 0    
for index, row in test_df.iterrows():
    if(row['actual'] == row['predicted']):
        correct += 1
    else:
        wrong +=1    
print('Test Accuracy - ', correct/ (correct+wrong)*100) 

#Writing to Output
f = open(output_file, "w+")
for index, row in test_df.iterrows():
    # Actual tweet is used instead of cleaned tweet data
   f.write(row['predicted'] + " " + row['actual'] + " " + row['tweet'])
f.close()

#Printing Top 5 words associated with each location
location_with_top_words = {}
cities = []
top_words = []
for k,v in (location_wise_data.items()):
    li = []
    cities.append(k)
    for k2, v2 in v.most_common(5):
        li.append(k2)
    top_words.append(li)
    location_with_top_words[k] = li
    
# Used panda tables to display locations having top 5 words
Table = {"Location ":cities, "Top 5 words ":top_words}
TableDF = pd.DataFrame(Table)
print(TableDF)
