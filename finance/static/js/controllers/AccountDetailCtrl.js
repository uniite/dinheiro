angular.module("Dinheiro").controller("AccountDetailCtrl", function ($controller, $rootScope, $scope, $routeParams, $location, $http, $q, Accounts, Categories, TransactionLoader, modelCache) {

    $scope.account_id = $routeParams.id;

    // https://stackoverflow.com/questions/5043650/how-can-i-correctly-format-currency-using-jquery
    var formatCurrency = function(amount) {
        return "$" + parseFloat(amount, 10).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, "$1,").toString();
    };

    modelCache.findByID(Accounts, $scope.account_id).then(function(account) {
        if (!account) {
            console.warn("Bad account");
            return;
        }
        account.usd_balance = formatCurrency(Math.abs(account.balance));
        $scope.account = account;
        $rootScope.title = $scope.account.name + " " + $scope.account.censored_account_number;
    });

    // Let a separate controller handle transactions; we will handle
    // account-specific functionality
    $controller("TransactionListCtrl", {$scope: $scope});

    $scope.$watch('category', function(category) {
        if (category) {
            $location.search({category: category.name});
        } else {
            $location.search({});
        }
    });


    // Setup click events
    // Sync: Synchronizes the account's transactions with the financial institution's data
    $rootScope.sync_handler = function() {
        var deferred = $q.defer();

        if (!$scope.account) return;
        $scope.account.post("sync").then(function(update) {
            // This seems to be a fast way to extend the array (source: http://jsperf.com/angulararrays)
            //$scope.transactions = $scope.transactions.concat(new_transactions);
            $scope.account.balance = update.balance;
            modelCache.getAll(Categories).then(function(categories) {
                TransactionLoader.load(update.transactions);
            });
            deferred.resolve();
        }, function(error) {
            apiErrorHandler(error);
            deferred.fail();
        });

        return deferred.promise;
    };
});
