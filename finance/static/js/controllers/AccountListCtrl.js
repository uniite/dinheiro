angular.module("Dinheiro").controller("AccountListCtrl", function ($scope, Accounts, modelCache) {
    modelCache.getAll(Accounts).then(function(accounts) {
        $scope.accounts = accounts;
    });
});
