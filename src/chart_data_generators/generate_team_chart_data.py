#! /usr/bin/python2

# input : one gold standard CSV file and three contributor CSV files (as 
#   command-line arguments)

# output : calculates the performance of the contributor
#   (by taking the number of labels that match the gold standard and
#   dividing by total number of labels) and prints the HTML for the
#   team performance chart to the console.

# example : python generate_team_chart_data.py <gold standard file> <alice file> <roger file> <john file> > <output file>

# example : python generate_team_chart_data.py ../../data/preliminary_analysis/gold_standard_annotations.csv ../../data/preliminary_analysis/alice_annotations.csv ../../data/preliminary_analysis/roger_annotations.csv ../../data/preliminary_analysis/john_annotations.csv > ../../results/charts/team_performance_chart.html

# author : a mysterious bumbledinger

import unicodecsv as csv
import sys
import collections

gold_file = csv.DictReader(open(sys.argv[1]))
contributor1_file = csv.DictReader(open(sys.argv[2]))
contributor2_file = csv.DictReader(open(sys.argv[3]))
contributor3_file = csv.DictReader(open(sys.argv[4]))

# dictionary that maps HIT id to the respective gold label
gold_pos_labels = {}
gold_neg_labels = {}

# fill gold_labels
for line in gold_file:
  hitId = line['HITId'].encode('UTF-8')
  gold_pos_labels[hitId] = line['positive_gold_label'].encode('UTF-8')
  gold_neg_labels[hitId] = line['negative_gold_label'].encode('UTF-8')

def calculate_percentage_matched(annotator_file):
  pos_matched = 0
  neg_matched = 0
  for line in annotator_file:
    hitId = line['HITId'].encode('UTF-8')
    positive = line['positive_label'].encode('UTF-8')
    negative = line['negative_label'].encode('UTF-8')

    if positive == gold_pos_labels[hitId]:
      pos_matched += 1

    if negative == gold_neg_labels[hitId]:
      neg_matched += 1

  return (float(pos_matched) / len(gold_pos_labels) * 100, float(neg_matched) / len(gold_neg_labels) * 100)


one_pos_correct, one_neg_correct = calculate_percentage_matched(contributor1_file)
two_pos_correct, two_neg_correct = calculate_percentage_matched(contributor2_file)
three_pos_correct, three_neg_correct = calculate_percentage_matched(contributor3_file)

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
          data.addColumn('number', 'Negative Label Accuracy');

          data.addRows([
"""

# the order is hardcoded because why not
html += "['Roger', " + str(two_pos_correct) + ", " + str(two_neg_correct) + "],"
html += "['Alice', " + str(one_pos_correct) + ", " + str(one_neg_correct) + "],"
html += "['John', " + str(three_pos_correct) + ", " + str(three_neg_correct) + "],"
html += "['Turker Majority', 67.91, 38.85],"
html += "['Plurality Label Baseline', 62.75, 43.13]"

html += """


          ]);

          var options = {
            title: 'Team Member Accuracy (compared against gold standard)',
            hAxis: {
              title: 'contributor'
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
    <div id="chart_div" style="width: 700px; height: 500px"></div>
  </body>
</html>
"""

print html

# fill in the name by hand 
# print "['', " + str(pos_correct) + ", " + str(neg_correct) + "],"
