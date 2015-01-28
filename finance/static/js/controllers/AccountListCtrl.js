angular.module("Dinheiro").controller("AccountListCtrl", function ($location, $rootScope, $scope, Accounts, modelCache) {
    $rootScope.title = "Accounts";

    modelCache.getAll(Accounts).then(function(accounts) {
        $scope.accounts = accounts;

        $scope.viewAccount = function($event) {
            var account_id = $event.target.dataset.accountId;
            $location.path("/accounts/" + account_id);
        };

        $scope.onSelect = function(event) {
           var selected = event.detail.data;
           alert('Selected: ' + selected.name);
        };
    });
});
