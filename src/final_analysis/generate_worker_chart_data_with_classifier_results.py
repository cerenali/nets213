#! /usr/bin/python2

# input : one gold standard CSV file and one worker CSV file (passed in as
#   command line arguments; see example command)

# output : calculates the performance of each worker, as well as the workers
#   as a whole (by taking the number of labels that match the gold standard and
#   dividing by total number of labels), then prints the full HTML for the
#   team performance chart to the console.

# example : python generate_worker_chart_data_with_classifier_results.py ../../data/preliminary_analysis/50_tweet_gold_labels.csv ../../data/preliminary_analysis/turkers_50_annotations.csv > ../../results/charts/final_worker_performance_chart_with_classifier.html

# author : a mysterious bumbledinger

import unicodecsv as csv
import sys
from collections import defaultdict

gold_file = csv.DictReader(open(sys.argv[1]))
worker_file = csv.DictReader(open(sys.argv[2]))

# dictionary that maps HIT ID to the respective gold label
gold_pos_labels = {}

# fill gold_labels
for line in gold_file:
  hitId = line['HITId'].encode('UTF-8')
  gold_pos_labels[hitId] = line['positive_gold_label'].encode('UTF-8')

# dictionaries that maps worker ID to a list of [num_pos_correct, num_completed]
worker_scores = defaultdict(lambda: [0, 0])

# aggregated over all workers
majority_pos_score = 0
total_completed = 0

# fill worker score dictionaries
for line in worker_file:
  hitId = line['HITId'].encode('UTF-8')
  workerId = line['WorkerId'].encode('UTF-8')
  positive = line['Answer.positive_label'].encode('UTF-8')

  # increment num_completed
  worker_scores[workerId][1] += 1
  total_completed += 1

  if positive == gold_pos_labels[hitId]:
    worker_scores[workerId][0] += 1
    majority_pos_score += 1

# calculate actual percentages (both positive and negative) for workers
for worker in worker_scores:
  divisor = worker_scores[worker][1]
  worker_scores[worker][0] = round(float(worker_scores[worker][0]) / divisor * 100, 2)

majority_pos_score = round(float(majority_pos_score) / total_completed * 100, 2)


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

html += "['Majority', " + str(majority_pos_score) + "],"

# print output for chart data
for worker in sorted(worker_scores, key=lambda x : worker_scores[x][0], reverse=True):
  # filter out workers who only did 1 HIT
  if worker_scores[worker][1] == 1:
    continue

  # truncate printing of worker ID for brevity + a modicum of privacy
  html += "['" + "" + "', " + str(worker_scores[worker][0]) + "],"

html += "['Classifier', 70],"
html += "['Baseline', 62],"
html = html[:-1] # truncate last comma

html += """
]);

          var options = {
            title: 'Worker Accuracy (compared against gold standard)',
            hAxis: {
              title: 'contributor',
              slantedText: true, 
              slantedTextAngle: 90
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


print html
