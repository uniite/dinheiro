angular.module("Dinheiro").controller("NavigationCtrl", function ($location, $rootScope, $scope) {
    // When a nav button is clicked, change the route and close the drawer (if using nav on mobile)
    $scope.menuClick = function(event) {
        var item = event.target;
        var href = item.attributes.href.value;

        if (href) {
            // Close the drawer menu (if applicable)
            document.querySelector('#drawer_panel').closeDrawer();
            // Grab the menu item clicked
            // Set the page title based on it
            $rootScope.title = $(item).text().trim();
            // Either process a direct link (eg. logout)
            if (href.indexOf('^') == 0) {
                location.href = href.replace(/^\^/, '');
            // Or an angular/relative link
            } else {
                $location.path(item.attributes.href.value);
            }
        }
    };
});
