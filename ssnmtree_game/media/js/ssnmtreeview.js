(function (jQuery) {
    var global = this;

    var SupportPerson = Backbone.Model.extend({
        defaults : {
            key : "", // for persistence
            name: "",
            disclosure : false,
            support : false
        },

        hasName: function (attrs) {
            return this.get("name").length > 0;
        }
    });

    var SupportPersonList = Backbone.Collection.extend({
        model : SupportPerson,
        isValid : function () {
            var valid = false;
            this.forEach(function (item) {
                if (item.hasName()) {
                    valid = true;
                    return;
                }
            });

            return valid;
        }
    });

    var SupportPersonView = Backbone.View.extend({
        events : {
            'click div.circle': 'onClick',
            'change input': 'onChangeName',
            'keypress input': 'onChangeName',
            'keyup input': 'onChangeName'
        },

        initialize: function (options) {
            _.bindAll(this, 'render', 'renderDisclosure', 'renderSupport', 'onClick', 'onChangeName');
            this.parent = options.parent;
            this.model.bind('change:disclosure', this.renderDisclosure);
            this.model.bind('change:support', this.renderSupport);
        },

        onChangeName: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            if (srcElement.value.length < 1) {
                this.model.set({"name": srcElement.value, "disclosure": false, "support": false });
            } else {
                this.model.set("name", srcElement.value);
            }
            this.model.save();
        },

        onClick: function (evt) {
            if (this.parent.edit_mode === "names") {
                return true; // do nothing
            }

            this.model.set(this.parent.edit_mode, !this.model.get(this.parent.edit_mode));
            this.model.save();
        },

        render: function () {
            jQuery("input", this.el).attr("value", this.model.get("name"));

            this.renderDisclosure();
            this.renderSupport();
        },

        renderDisclosure: function () {
            if (this.model.hasName() && this.model.get("disclosure")) {
                jQuery(".ripe", this.el).addClass('turned-on');
            } else {
                jQuery(".ripe", this.el).removeClass('turned-on');
            }
        },

        renderSupport: function () {
            if (this.model.hasName() && this.model.get("support")) {
                jQuery(".circle", this.el).addClass('turned-on');
            } else {
                jQuery(".circle", this.el).removeClass('turned-on');
            }
        }
    });

    var SupportPersonListView = Backbone.View.extend({
        edit_mode: 'names',

        events : {
            'click div#toggle-support-selection' : 'toggleSupportSelection',
            'click div#toggle-disclosure-selection' : 'toggleDisclosureSelection',
            'click div#top-nav-lateral a': 'saveState',
            'click div#bottom-nav-lateral a': 'saveState'
        },

        initialize : function (options) {
            _.bindAll(this, 'toggleSupportSelection', 'toggleDisclosureSelection', 'saveState', 'addPerson');
            this.collection = options.collection;
            this.collection.bind('add', this.addPerson);
        },

        addPerson : function (person) {
            new SupportPersonView({ model: person, el: jQuery("#" + person.get("key")), parent: this }).render();
        },

        toggleSupportSelection: function () {
            var self = this;
            self.edit_mode = "support";

            jQuery("div#toggle-support-selection").toggleClass('on off');

            if (jQuery("div#toggle-support-selection").hasClass('on')) {
                jQuery("div#toggle-disclosure-selection").removeClass('on');
                jQuery("div#toggle-disclosure-selection").addClass('off');
            }
        },

        toggleDisclosureSelection: function () {
            var self = this;
            self.edit_mode = "disclosure";

            jQuery("div#toggle-disclosure-selection").toggleClass('on off');

            if (jQuery("div#toggle-disclosure-selection").hasClass('on')) {
                jQuery("div#toggle-support-selection").removeClass('on');
                jQuery("div#toggle-support-selection").addClass('off');
            }
        },

        saveState: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            if (!this.collection.isValid()) {
                evt.preventDefault();
                alert('Please enter at least one name.');
            } else {
                // Initiate the ajax call to saveState
                global.Intervention.saveState(function (result) {
                    if (result.responseText !== "ok") {
                        alert("An error occurred while saving your information. Please try again.");
                    } else {
                        window.location = srcElement.href;
                    }
                });
            }
            return false;
        }
    });

    Backbone.sync = function (method, model, success, error) {
        // Save the results back to the game state
        // Don't do a full server-side save on every sync
        var game_state = global.Intervention.getGameVar('ssnmtree', {});
        var key = model.get("key");

        if (!_.has(game_state, key)) {
            game_state[key] = {};
        }

        game_state[key].name = model.get("name");
        game_state[key].support = model.get("support");
        game_state[key].disclosure = model.get("disclosure");
    };

    jQuery(document).ready(function () {
        var collection = new SupportPersonList();
        var ssnmTreeView = new SupportPersonListView({
            collection: collection,
            el: 'div#contentcontainer'
        });

        // Populate collection from the DOM & the game_state
        // As items are added to the collection, the ListView
        // will be signaled to create a new subview
        var game_state = global.Intervention.getGameVar('ssnmtree', {});

        jQuery("div.fruit").each(function () {
            var person = new SupportPerson();
            person.set("key", this.id);

            if (_.has(game_state, this.id)) {
                var val = game_state[this.id];

                person.set({
                    name: val.name,
                    disclosure: val.disclosure,
                    support: val.support
                });
            }

            collection.add(person);
        });
    });
}(jQuery));
