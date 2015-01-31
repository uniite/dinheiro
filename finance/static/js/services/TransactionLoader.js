angular.module("Dinheiro").service("TransactionLoader", function(modelCache, Transactions) {
    var default_category = {id: 0, name: ""};

    this.load = function(transactions, categories) {
        modelCache.loadCustom(Transactions, transactions.map(function(t) {
            t.date = new Date(t.date);
            t.formatted_date = t.date.toLocaleDateString();

            var category_id = t.category;
            if (!categories) {
                t.category = default_category;
            }
            var matches = categories.filter(function(c) {
                return c.id == category_id;
            });
            if (matches.length == 0) {
                t.category = default_category;
            } else {
                t.category = matches[0];
            }

            return t;
        }));
    };
});
