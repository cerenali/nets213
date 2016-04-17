## Aggregation Module 1

This module takes the first HIT output, consisting of 7 label judgements for each tweet,
and takes majority vote to come up with the first- and second-place labels for each tweet.
Also aggregated for each tweet are the 7 'creative', or freeform entry, labels used to 
describe the tweet's social sphere.
  
majority_label.py
    USAGE: <labelled tweets>.csv | python2 majority_label.py > aggregate1_out.csv

