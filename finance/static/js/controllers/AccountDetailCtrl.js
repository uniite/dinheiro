angular.module("Dinheiro").controller("AccountDetailCtrl", function ($controller, $scope, $routeParams, $location, $http, $q, Accounts, Categories, Transactions, modelCache, TransactionLoader, Stats) {
    $scope.account_id = $routeParams.id;

    modelCache.findByID(Accounts, $scope.account_id).then(function(account) {
        $scope.account = account;
    });

    // Let a separate controller handle transactions; we will handle
    // account-specific functionality
    $controller("TransactionListCtrl", {$scope: $scope});

    $scope.$watch('category', function(category) {
        console.log($scope.category);
        if (category) {
            $location.search({category: category.name});
        } else {
            $location.search({});
        }
    });


    // Setup click events
    // Sync: Synchronizes the account's transactions with the financial institution's data
    $scope.sync = function(account, event) {
        if (!$scope.account) return;
        // Disable the button while the sync runs
        var button = $(event.target)
        button.button("loading");
        var enableButton = function() {
            button.button("reset");
        };
        $scope.account.post("sync").then(function(update) {
            // This seems to be a fast way to extend the array (source: http://jsperf.com/angulararrays)
            //$scope.transactions = $scope.transactions.concat(new_transactions);
            $scope.account.balance = update.balance;
            TransactionLoader.load(update.transactions);
            enableButton();
        }, function(error) {
            enableButton();
            apiErrorHandler(error);
        });
    };
});
