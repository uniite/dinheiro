angular.module("Dinheiro").controller("StatsCtrl", function ($http, $rootScope, $scope) {
    $rootScope.title = "Stats";

    $http.get('/finance/api/stats').then(function(response) {
        $scope.months = response.data.months;
        $scope.table_data = response.data.table_data;
        $('#chart').highcharts({
            //colors: ['#dd7722', '#2288cc', '#dd3322', '#22aa99', '#bb4488', '#ddaa00', '#6655cc', '#99aa00'],
            chart: {
                type: 'column'
            },
            title: false,
            xAxis: {
                categories: response.data.months,
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'Dollars'
                }
            },
            tooltip: {
                shared: true,
                valueSuffix: ' USD'
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#666666'
                    }
                },
                line: {
                    lineColor: '#00cc33'
                }
            },
            series: response.data.series
        });
    });
});
