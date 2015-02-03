angular.module("Dinheiro").service("TransactionLoader", function(modelCache, Transactions) {
    var default_category = {id: 0, name: ""};

    this.load = function(transactions, categories) {
        transactions = transactions.map(function(t) {
            // Format date
            t.date = new Date(t.date);
            t.formatted_date = moment(t.date).format("MMM D, YYYY");

            // Map category
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
        });
        modelCache.loadCustom(Transactions, transactions);

        // Setup groups on core-list (one per day_
        var list = $(".transaction-list").get(0);
        var counts = _.countBy(transactions, function(t) { return t.formatted_date; });
        list.groups = _.keys(counts).map(function(k) {
            return { length: counts[k], data: { date: k } };
        });
    };
});
