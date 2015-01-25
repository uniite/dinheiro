angular.module("Dinheiro").controller("CategoryEditCtrl", function ($scope, $routeParams, $http, Categories, modelCache) {
    //var categoriesLoaded = modelCache.loadModel(Categories);
    //$scope.categories = modelCache.getCached(Categories);

    // We're either editing an existing category
    if ($routeParams.id) {
        $http.get("/finance/api/categories/" + $routeParams.id).then(function(response) {
            $scope.category = response.data;
        });
    // or a new category
    } else {
        $scope.category = {
            name: "",
            parent: null,
            rules: []
        };
    }

    $scope.deleteRule = function(rule) {
        $http.delete("/finance/api/rules/" + rule.id);
        $scope.category.rules.splice($scope.category.rules.indexOf(rule), 1);
    }

    $scope.save = function() {
        var response;
        // Saving an existing category
        if ($scope.category.id) {
        // or a new category
        } else {
            response = $http.post("/finance/api/categories", $scope.category);
        }
        response.then(function() {
            window.history.back();
        }, apiErrorHandler);
    };

});
