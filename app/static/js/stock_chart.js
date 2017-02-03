/**
 * Created by ruizhang on 1/27/17.
 */
// START CONFIGURATION
/**
 * Created by ruizhang on 2/2/17.
 */
$(document).ready(function () {
    $('#chart-container').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Stock chart'
        },
        xAxis: {
            categories: ['Market Cap', 'Margin']
        },
        yAxis: {
            title: {
                text: 'Normalized'
            }
        },
        series: [{
            name: 'AAPL',
            data: [1, 0, 4]
        }, {
            name: 'QCOM',
            data: [5, 7, 3]
        }]
    });
});