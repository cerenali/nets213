import sys
import csv
import json
import string
from datetime import datetime 

#This will open a new csv file to which you will write your output
output = csv.writer(open('parsed_tweets3.csv', 'w'))

#These are the column names your csv file will contain
headers = ['text', 'url']
output.writerow(headers)
json_input = sys.argv[1]
row = ["-","-"]
tweets_file = open(json_input).readlines()
count = 0
for line in tweets_file:
	#sys.stderr.write("%s" % line)
	try:
		tweet_dict = json.loads(line)
		#sys.stderr.write("%s\n" % (tweet_dict['text']))
		count +=1
		#sys.stderr.write("%s\n" % count)
		#sys.stderr.write("%s\n" % ('twitter.com/anyuser/status/' + tweet_dict['id_str']))
		isVerified = tweet_dict['user']['verified']
		if isVerified == 'true' :
			continue
		text = tweet_dict['text']
		url = "twitter.com/anyuser/status/" + tweet_dict['id_str']
		row[0] = text
		row[1] = url
		output.writerow(row)
	except:
		continue