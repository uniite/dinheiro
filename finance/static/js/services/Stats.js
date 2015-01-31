angular.module("Dinheiro").service("SummaryStats", function($http) {
    this.transactionTimeChart = function($chart, filters) {
        $http.get("/finance/api/summary_stats", filters).then(function (response) {
            var stats = response.data;
            function parseTimeSeries(data) {
                return data.map(function(point) {
                    return [
                        (new Date(point.day)).getTime(),
                        parseFloat(point.total_amount)
                    ];
                });
            }
            var oneDay = 24 * 3600 * 1000;
            var data = parseTimeSeries(stats.withdrawals);
            $chart.plot([
                    {
                        data: data,
                        color: "rgb(200, 20, 30)"
                    }
                ],
                {
                    bars: {
                        barWidth: oneDay * 0.6,
                        show: true
                    },
                    xaxis: {
                        mode: "time"
                    }
                }
            );
            console.log($chart.html());
            console.log(response.data);
        }, apiErrorHandler);
    };
});
