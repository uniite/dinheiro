(function() {
    var app = angular.module("Dinheiro");

    app.factory("Accounts", function (Model) {
        return Model("accounts")
    });
    app.factory("Categories", function (Model) {
        return Model("categories")
    });
    app.factory("Rules", function (Model) {
        return Model("rules")
    });
    app.factory("Transactions", function (Model) {
        return Model("transactions")
    });

    app.factory("Model", function (Restangular) {
        return function (name) {
            return {
                "all": Restangular.all(name).getList,
                "create": Restangular.all(name).post,
                "get": function (id) {
                    return Restangular.one(name, id).get();
                },
                "name": name,
                "one": function (id) {
                    return Restangular.one(name, id);
                }
            };
        };
    });

})();
