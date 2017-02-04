/**
 * Created by ruizhang on 1/27/17.
 */
// START CONFIGURATION
/**
 * Created by ruizhang on 2/2/17.
 */
$(document).ready(function() {
	$('#chart-container').highcharts({
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
		series: series
	});
});