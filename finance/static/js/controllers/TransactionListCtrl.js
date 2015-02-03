angular.module("Dinheiro").controller("TransactionListCtrl", function ($rootScope, $scope, $routeParams, $templateCache, $location, $http, $q, Categories, Transactions, modelCache, TransactionLoader, SummaryStats) {
    $rootScope.title = "Transactions";

    $scope.sort_field = "-date";
    $templateCache.removeAll();

    // If there is a parent controller (ie. AccountDetailCtrl), we may have to filter by account ID
    var chart_filter = {};
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
    $scope.all_transactions = modelCache.getCached(Transactions);
    $scope.transactions = $scope.all_transactions;
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
        $("#list_loading").addClass("hidden");
        $(".transaction-list").removeClass("hidden");

    }, apiErrorHandler);


    var searchTextFilter = function(transaction) {
        var search_text = $rootScope.searchText;
        if (search_text && search_text.trim() != "") {
            search_text = search_text.toLowerCase();
            return transaction.payee.toLowerCase().indexOf(search_text) != -1
        } else {
            console.log("filter t");
            return true;
        }
    };

    // Category filter function (used on transaction list/table)
    var categoryFilter = function(transaction) {
        // All categories (unfiltered)
        if ($scope.category == null) {
            return true;
        // Must match selected category
        } else {
            return transaction.category.id === $scope.category.id;
        }
    };

    var filter_transactions = function() {
        if ($scope.all_transactions.length > 0) {
            $scope.transactions = $scope.all_transactions.filter(function (trx) {
                return searchTextFilter(trx) && categoryFilter(trx);
            });
        }
    };
    $scope.$watch("category", filter_transactions);
    $rootScope.$watch("searchText", filter_transactions);

    // Render the transaction time-chart
    if ($scope.account_id) {
        $scope.$on("$includeContentLoaded", function () {
            SummaryStats.transactionTimeChart($("#time-chart"), chart_filter);
        });
    } else {
        SummaryStats.transactionTimeChart($("#time-chart"), chart_filter);
    }

});
