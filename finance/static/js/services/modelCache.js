angular.module("Dinheiro").service("modelCache", function($q) {
    var cache = {};
    var index = {};

    // It is important to push new items to our cache arrays so we don't break any bindings
    // (rather than just replacing them in the cache object)
    function addItems(model_name, items) {
        // Add them to the cache
        for (var i = 0; i < items.length; i++) {
            cache[model_name].push(items[i]);
            // Also add them to the index, just by ID for now
            index[model_name].byID[items[i].id] = items[i];
        }
    }

    function initModel(model) {
        cache[model.name] = cache[model.name] || [];
        index[model.name] = index[model.name] || { byID: {} };
    }

    function resetModel(model) {
        cache[model.name] = [];
        index[model.name] = { byID: {} };
    }

    function isLoaded(model) {
        return cache[model.name] && cache[model.name].length != 0;
    }

    // These should be automatically generated eventually
    return {
        loadModel: function(model) {
            initModel(model);
            return model.all().then(function (items) {
                cache[model.name].splice(0);
                addItems(model.name, items);
            }, apiErrorHandler);
        },
        loadCustom: function(model, items) {
            initModel(model);
            addItems(model.name, items);
            console.log(_.string.sprintf("Loaded %d items", items.length));
        },
        getCached: function(model) {
            return cache[model.name];
        },
        // Return a promise for these rather than the contents of the cache,
        // so we can automatically load the model when missing
        getAll: function(model) {
            var self = this;
            return $q(function(resolve, reject) {
                if (!isLoaded(model)) {
                    self.loadModel(model).then(function () {
                        self.getAll(model).then(resolve);
                    }, reject);
                } else {
                    resolve(cache[model.name]);
                }
            });
        },
        findByID: function(model, id) {
            var self = this;
            return $q(function(resolve, reject) {
               if (!isLoaded(model)) {
                    self.loadModel(model).then(function() {
                        self.findByID(model, id).then(resolve);
                    }, reject);
                } else {
                    resolve(index[model.name].byID[id]);
                }
            });
        },
        reset: function(model) {
            resetModel(model);
        }
    }
});
