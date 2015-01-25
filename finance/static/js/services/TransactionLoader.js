angular.module("Dinheiro").service("TransactionLoader", function(modelCache, Transactions) {
    this.load = function(transactions, categories) {
        modelCache.loadCustom(Transactions, transactions.map(function(t) {
            t.date = new Date(t.date);
            t.formatted_date = t.date.toLocaleDateString();
            var category_id = t.category;
            t.category = function() {
                var default_category = {id: 0, name: ""};

                if (!categories) {
                    return default_category;
                }

                var matches = categories.filter(function(c) {
                    return c.id == category_id;
                });

                if (matches.length == 0)
                    return default_category;

                return matches[0];
            }
            return t;
        }));
    };
});
