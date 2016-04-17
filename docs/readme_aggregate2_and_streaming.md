## More Aggregation code

aggregate2/match_creative.py

	python match_creative.py arg1.csv

Takes the output file from aggregate1 module as input. Compiles the creative and given label responses from the tweets and matches creative labels to one of our given labels based on majority. The format of the output: creative_label, corresponding_set_label. 


## Python Streaming Code

twitter_stream/twitter_stream.py

	python twitter_stream.py -> outputfile.txt

Uses twitter streaming API with Tweepy to stream tweets in json format from twitter. This stream will only take tweets in English that are posted in the US. Writes to a specified output file. 


twitter_stream/json_tweet_parser.py

	python json_tweet_parser.py inputfile.txt

Takes in the text file created from twitter_stream.py and extracts the text of each tweet and its corresponding url from the json dump. Tweets from verified sources are filtered out. This is returned as the csv file specified in line 8: "output = csv.writer(open('parsed_tweets.csv', 'w'))". The format of the output is text, url. 
