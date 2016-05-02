#! /usr/bin/python2

# input : one gold standard CSV file and one quality control CSV file (passed in as
#   command line arguments; see example command)

# output : calculates the performance of the quality control workers (by taking 
#   the number of labels that match the gold standard and dividing by total 
#   number of labels), then prints the full HTML for the chart to the console.
#   (more likely than not, we will just take the calculated value for qc
#   performance and paste it into our existing gold standard chart.)

# example : python generate_team_qc_chart_data.py <gold standard file> <quality control file> > <output file>

# example : python generate_team_qc_chart_data.py ../../data/preliminary_analysis/50_tweet_gold_labels.csv ../../data/full_batch/quality_control_HIT_out.csv > ../../results/charts/gold_vs_qc_chart.html

# author : a mysterious bumbledinger

import unicodecsv as csv
import sys
from collections import defaultdict

gold_file = csv.DictReader(open(sys.argv[1]))
qc_file = csv.DictReader(open(sys.argv[2]))

# dictionary that maps tweet text to the respective gold label
gold_labels = {}

# fill gold_labels
for line in gold_file:
  tweet_text = line['Input.text'].encode('UTF-8').replace('\n', ' ').replace('_', ' ')
  gold_labels[tweet_text] = line['positive_gold_label'].encode('UTF-8')

qc_num_correct = 0
qc_total_done = 0
# compare to quality control
for line in qc_file:
  tweet_text = line['Input.text'].encode('UTF-8').replace('\n', ' ')
  if not tweet_text in gold_labels:
    continue
  qc_total_done += 1
  qc_label = line['Answer.positive_label'].encode('UTF-8').replace('_', ' ')
  if qc_label == gold_labels[tweet_text]:
    qc_num_correct += 1
  else:
    # tmp
    print '>>> mismatch: ' + qc_label + ' vs gold: ' + gold_labels[tweet_text]

qc_score = round(float(qc_num_correct) / qc_total_done * 100, 2)

print str(qc_score)

html = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = new google.visualization.DataTable();
          data.addColumn('string', 'Contributor');
          data.addColumn('number', 'Positive Label Accuracy');

          data.addRows([
"""

html += "['Quality Control Results', " + str(qc_score) + "]"

html += """
]);

          var options = {
            title: 'Worker Accuracy (compared against quality control results)',
            hAxis: {
              title: 'worker ID'
            },
            vAxis: {
              title: '% correct',
              viewWindow: {
                min: 0,
                max: 100
              }
            }
          };

          var chart = new google.visualization.ColumnChart(
            document.getElementById('chart_div'));

          chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 1200px; height: 500px"></div>
  </body>
</html>
"""


# print html
