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


    $scope.sync = function() {
        if ($rootScope.sync_handler) {
            $("#sync_spinner").attr("active", "").removeClass("hidden");
            $(".refresh-button").hide();
            $rootScope.sync_handler().finally(function () {
                $("#sync_spinner").removeAttr("active");
                setTimeout(function () {
                    $("#sync_spinner").addClass("hidden");
                    $(".refresh-button").show();
                }, 500);
            });
        }
    };
});
