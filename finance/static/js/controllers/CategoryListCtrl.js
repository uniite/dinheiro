angular.module("Dinheiro").controller("CategoryListCtrl", function ($rootScope, $scope, $routeParams, $http, Categories, modelCache) {
    $rootScope.title = "Categories";

    modelCache.getAll(Categories).then(function(categories) {
        $scope.categories = categories;
    });

    $scope.delete = function(category) {
        $http.delete("/finance/api/categories/" + category.id);
        $scope.categories.splice($scope.categories.indexOf(category), 1);
    };
});