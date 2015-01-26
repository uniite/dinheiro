angular.module("Dinheiro").controller("NavigationCtrl", function ($location, $scope) {
    $scope.menuClick = function(event) {
        $location.path(event.target.attributes.href.value);
        document.querySelector('#drawer_panel').closeDrawer();
    };
});
