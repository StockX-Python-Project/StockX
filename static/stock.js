var chart;
var intervalSelect = $('#interval-select');

function fetchStockData(interval) {
    $.ajax({
        url: '/get_chart_data',
        method: 'POST',
        data: { interval: interval },
        success: function (data) {
            var options = {
                chart: {
                    type: 'line',
                },
                title: {
                    text: 'Reliance Stock Price'
                },
                xAxis: {
                    type: 'datetime',
                },
                yAxis: {
                    title: {
                        text: 'Price'
                    }
                },
                series: [{
                    name: 'Reliance Price',
                    data: data,
                }]
            };
            chart = Highcharts.chart('stockChart', options);
        }
    });
}

intervalSelect.on('change', function () {
    var selectedInterval = $(this).val();
    fetchStockData(selectedInterval);
});

// Initial load
fetchStockData(intervalSelect.val());