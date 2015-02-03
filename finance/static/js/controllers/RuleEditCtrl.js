angular.module("Dinheiro").controller("RuleEditCtrl", function ($rootScope, $scope, $routeParams, Rules, modelCache, $http) {
    $scope.fields = [
        {name: "Date", value: "date"},
        {name: "Payee", value: "payee"},
        {name: "Type", value: "type"}
    ];
    $scope.types = [
        {name: "Contains", value: "contains"},
        {name: "Starts With", value: "startswith"},
        {name: "Ends With", value: "endswith"}
    ];

    var loadCategory = function() {
       $http.get("/finance/api/categories/" + $scope.rule.category).then(function(response) {
            $scope.category = response.data;
        });
    }

    // We're either editing an existing rule
    if ($routeParams.id) {
        $rootScope.title = "Edit Rule";
        $http.get("/finance/api/rules/" + $routeParams.id).then(function(response) {
            $scope.rule  = response.data;
            loadCategory();
        });
    // or a new rule
    } else {
        $rootScope.title = "New Rule";
        $scope.rule = {
            category: $routeParams.categoryID,
            type: "startswith",
            field: "payee",
            content: ""
        };
        loadCategory();
    }

    $scope.save = function() {
        var response;
        // Saving an existing rule
        if ($scope.rule.id) {
            response = $http.put("/finance/api/rules/" + $scope.rule.id, $scope.rule);
        // or a new rule
        } else {
            response = $http.post("/finance/api/rules", $scope.rule);
        }
        response.then(function() {
            window.history.back();
        }, apiErrorHandler);
    };
});
