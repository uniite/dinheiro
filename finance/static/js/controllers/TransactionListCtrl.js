angular.module("Dinheiro").controller("TransactionListCtrl", function ($scope, $routeParams, $location, $http, $q, Categories, Transactions, modelCache, TransactionLoader, Stats) {
    $scope.sort_field = "-date";

    // If there is a parent controller (ie. AccountDetailCtrl), we may have to filter by account ID
    var chart_filter = {}
    var transactions_promise;
    if ($scope.account_id) {
        chart_filter.account = $scope.account_id;
        transactions_promise = $http.get(_.string.sprintf("/finance/api/accounts/%s/transactions", $scope.account_id));
    // Otherwise, just get all transactions
    } else {
        transactions_promise = $http.get(_.string.sprintf("/finance/api/transactions"));
    }

    // Category and Transaction loading
    modelCache.reset(Transactions);
    $scope.transactions = modelCache.getCached(Transactions);
    // Need both categories and transactions loaded before processing transactions,
    // so use $q to wait for both requests/promises to resolve
    $q.all([
        $http.get("/finance/api/categories").then(function(response) {
            $scope.categories = response.data;
            $scope.categories.unshift({id: 0, name: "(uncategorized)"});
        }, apiErrorHandler),
        transactions_promise

    ]).then(function(responses) {
        var transactions = responses[1].data;
        TransactionLoader.load(transactions, $scope.categories);

    }, apiErrorHandler);

    // Render the transaction time-chart
    Stats.transactionTimeChart($("#time-chart"), chart_filter);

    // Category filter function (used on transaction list/table)
    $scope.categoryFilter = function(transaction) {
        // All categories (unfiltered)
        if ($scope.category == null) {
            return true;
        // Must match selected category
        } else {
            return transaction.category().id === $scope.category.id;
        }
    };
});
