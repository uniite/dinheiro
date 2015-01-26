(function() {

    var app = angular.module("Dinheiro", ["mgcrea.ngStrap", "ngRoute", "ng-polymer-elements", "restangular"]);

    app.config(function(RestangularProvider) {
        RestangularProvider.setBaseUrl("/finance/api");
    });

    app.config(['$routeProvider', function($routeProvider) {
        $routeProvider.
          //when('/institutions', {templateUrl: '/static/partials/account-list.html',   controller: "InstitutionListCtrl"}).
          //when('/institutions/:id', {templateUrl: '/static/partials/account-list.html',   controller: "AccountListCtrl"}).
          when('/accounts', {templateUrl: '/static/partials/account-list.html', controller: "AccountListCtrl"}).
          when('/accounts/:id', {templateUrl: '/static/partials/account-detail.html', controller: "AccountDetailCtrl", reloadOnSearch: false}).
          when('/categories', {templateUrl: '/static/partials/category-list.html', controller: "CategoryListCtrl"}).
          when('/categories/new', {templateUrl: '/static/partials/category-new.html', controller: "CategoryEditCtrl"}).
          when('/categories/:id/edit', {templateUrl: '/static/partials/category-edit.html', controller: "CategoryEditCtrl"}).
          when('/categories/:categoryID/rules/new', {templateUrl: '/static/partials/category-rule-edit.html', controller: "RuleEditCtrl"}).
          when('/transactions', {templateUrl: '/static/partials/transaction-list.html', controller: "TransactionListCtrl", reloadOnSearch: false}).
          when('/rules/:id/edit', {templateUrl: '/static/partials/category-rule-edit.html', controller: "RuleEditCtrl"}).
          otherwise({redirectTo: '/accounts'});
    }]);
})();

function apiErrorHandler() {
    alert("Something broke!");
}
