angular.module("Dinheiro").service("Stats", function($http) {
    this.transactionTimeChart = function(filters) {
        $http.get("/finance/api/stats", filters).then(function (response) {
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
            var timeChart = $("#time-chart").plot([
                    {
                        data: parseTimeSeries(stats.withdrawals),
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
                });
        }, apiErrorHandler);
    };
});
