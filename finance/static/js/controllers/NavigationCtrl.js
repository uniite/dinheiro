angular.module("Dinheiro").controller("NavigationCtrl", function ($location, $rootScope, $scope) {
    $scope.menuClick = function(event) {
        var item = event.target;
        $rootScope.title = item.innerHTML.trim();
        $location.path(item.attributes.href.value);
        document.querySelector('#drawer_panel').closeDrawer();
    };
});
