#! /usr/bin/python2

# input : none (we are hardcoding in the values from results/50_heldout/50_held_out_results.txt)

# output : generates the HTML data for a chart of the classifer performance
#   across the different audience categories

# example : python generate_classifier_results_across_categories.py > ../../results/charts/final_classfier_performance_chart_across_categories.html

# author : a mysterious bumbledinger

import sys
import collections

html = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = new google.visualization.DataTable();
          data.addColumn('string', 'Category');
          data.addColumn('number', 'Positive Label Accuracy');

          data.addRows([
"""

# the order is hardcoded because why not
html += "['All', 70],"
html += "['Friends', 100],"
html += "['Family', 0],"
html += "['General Internet Community', 26.67],"
html += "['Coworkers', 0],"
html += "['Specific Organization', 0],"

html += """


          ]);

          var options = {
            title: 'Classifier Accuracy Across Categories',
            hAxis: {
              title: 'category'
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
