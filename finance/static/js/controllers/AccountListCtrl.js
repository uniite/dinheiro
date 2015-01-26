angular.module("Dinheiro").controller("AccountListCtrl", function ($location, $scope, Accounts, modelCache) {
    modelCache.getAll(Accounts).then(function(accounts) {
        $scope.accounts = accounts;

        $scope.viewAccount = function() {
            $location.path("/accounts/" + this.account.id);
        };

        $scope.onSelect = function(event) {
           var selected = event.detail.data;
           alert('Selected: ' + selected.name);
        };
    });
});
