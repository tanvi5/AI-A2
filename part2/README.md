# Assignment 2 tweet classification

Training data file contains locations which are read by regex (r'\w{4,},_\w+ ')

Training data is stored in a dictionary of dictionary in the format - 

Location : {word : probability}

For each location, I am collecting all the words by removing all the characters other than a-zA-Z, digits and spaces. 

I have used stop words as - 

['', '_', ',','\'','a','an','and','are','the','as', 'at', 'be' ,'by' ,'us','it','too','she' ,'for', 'from', 'has','he', 'in', 'yes','is', 'its', 'of', 'on', 'that', 'to', 'was', 'were', 'will', 'with','my','you','mine','yours','we','can','this','our','because','him','his','her']

Data is converted to lower case and these stop words are removed. 

For each word we have calculated the count of that word in given location 

Prior probabilities are calculated as P(word/location) = count of word in location / total number of words in location


Test data is stored in the data frame having columns predicted, actual, tweet and clean_tweet columns.
For each new tweet we are calculating probability of occurance in a location and finding a best location that gives maximum probability of all the words in tweet. 

According to naive bayes,

P(location / w1, w2, w3 ... ) proportional to P(w1/location) * P(w2/location) .. * P(location)

It makes an assumption that the words in location are independent given location. 

We have found that the training data has 88.5% accuracy and test data has 66.6% accuracy for given files
