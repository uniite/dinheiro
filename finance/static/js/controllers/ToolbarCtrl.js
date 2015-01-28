angular.module("Dinheiro").controller("ToolbarCtrl", function ($location, $rootScope, $scope) {
    $rootScope.$watch("title", function(title) {
        $scope.title = title;
    });

    $scope.showSearch = false;
    $scope.toggleSearch = function() {
        $scope.showSearch = !$scope.showSearch;
        $scope.toolbarClass = $scope.showSearch ? "show-search" : '';
    };

    $scope.$watch("searchText", function(text) {
        $rootScope.searchText = text;
    });
});
