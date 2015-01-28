angular.module("Dinheiro").controller("NavigationCtrl", function ($location, $rootScope, $scope) {
    // When a nav button is clicked, change the route and close the drawer (if using nav on mobile)
    $scope.menuClick = function(event) {
        var item = event.target;
        $rootScope.title = item.innerHTML.trim();
        $location.path(item.attributes.href.value);
        document.querySelector('#drawer_panel').closeDrawer();
    };
});
