import csv
import sys
import operator
from collections import namedtuple


CFPair = namedtuple("CFPair", ["c", "f"])

output = csv.writer(open('aggregate2.csv', 'w'))
header = ['creative_label','set_label']
output.writerow(header)
input = sys.argv[1]

creative_to_final = {}
#pair count maps (creative, final) : count
pair_count = {}

with open(input) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		final_label = row['Answer.positive_label']
		for num in range(1, 7) :
			creative_label = row['Input.creative_label_'+str(num)]
			if creative_label == '' :
				continue
			pair = CFPair(c=creative_label, f=final_label)
			if pair not in pair_count :
				pair_count[pair] = 1
			else :
				pair_count[pair] = pair_count[pair]+ 1

pair_count_tuples = sorted(pair_count, key=pair_count.get, reverse=True)

print pair_count_tuples

for tup in pair_count_tuples :
	creative = tup.c
	if creative not in creative_to_final :
		creative_to_final[creative] = tup.f

print creative_to_final

for creative in creative_to_final.keys() :
	final = creative_to_final[creative]
	row = ["-","-"]
	row[0] = creative
	row[1] = final
	output.writerow(row)




