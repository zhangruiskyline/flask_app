## 1. Highchart usage

### In the HTML snippet above:

1.Include jQuery, Highcharts, and a Highcharts module’s Javascript code onto the page
2.Set up a div with a unique ID (in this case chart-container) which we will later pass Highcharts as the desired destination of our chart

### In the Javascript snippet:

1.Set some configuration vairables including the domain the dataset lives on, the dataset’s unique ID (aka “four by four”), the query string, and finallyt the title for the chart.

2. Inside jQuery’s .ready() callback, which is called once the HTML page and dependencies are fully loaded, we form a URL to query the dataset for the data we want and use the response to create the chart in the specified #chart-container div. You can learn more about how to create a chart using Highcharts and find links to their documentation here.

http://www.highcharts.com/docs/getting-started/your-first-chart
https://dev.socrata.com/blog/2015/03/30/create-a-column-chart-with-highcharts.html


Problem: navbar overlap with div

solution:
Use padding-top in body tag

<body style="padding-top:50px">
This is why beacuse the navbar is set to be fixed top, so it will stick at the top and overlaps the below divs
http://stackoverflow.com/questions/25600076/overlapping-divs-with-bootstrap-navbar
