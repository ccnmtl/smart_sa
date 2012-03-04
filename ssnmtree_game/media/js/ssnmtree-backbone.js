(function(jQuery) {
    var global = this;
    
    Backbone.sync = function(method, model, success, error) {
        success();
    }

    var SupportPerson = Backbone.Model.extend( {
        defaults : {
            name: "",
            disclosure : false,
            support : false
        },
        
        validate: function(attrs) {
            return name.length > 0;
        }
    });
    
    
    var SupportPersonView = Backbone.View.extend( {
        events : {
            "click .fruit": "clickPerson"
        },
        
        initialize: function(options) {
            _.bindAll(this, 'render', 'clickPerson');
            this.parent = options.parent;
        },

        clickPerson: function(evt) {
            alert("clicked");
        }
    });
    
    var SupportPersonList = Backbone.Collection.extend( {
        model : SupportPerson
    });


    var SupportPersonListView = Backbone.View.extend( {
        game_state: null,
        edit_mode: 'names',
        
        events : {
            'click div#toggle-support-selection' : 'toggleSupportSelection',
            'click div#toggle-disclosure-selection' : 'toggleDisclosureSelection',
            'click a#complete': 'saveState'
        },

        initialize : function() {
            var self = this;
            
            _.bindAll(this, 'toggleSupportSelection', 'toggleDisclosureSelection', 'saveState');
            
            this.intervention = global.Intervention;
            this.game_state = this.intervention.getGameVar('ssnmtree', {});
            
            this.network = new SupportPersonList();
            
            if (_.isEmpty(this.game_state)) {
                // fill 'er up from the dom
            }  
            
            _.each(this.game_state, function(val, key) { 
                if (_.isObject(val)) {
                    var person = new SupportPerson();
                    person.set({
                        name: val.name,
                        disclosure: val.disclosure,
                        support: val.support,
                    });
                    
                    self.network.add(person);
                    new SupportPersonView({ model: person, el: key, parent: this });
                }
            });
        },
        
        toggleSupportSelection: function() {
            var self = this;
            self.edit_mode = "support";
            
            jQuery("div#toggle-support-selection").toggleClass('on off');
            
            if (jQuery("div#toggle-support-selection").hasClass('on')) {
                jQuery("div#toggle-disclosure-selection").removeClass('on');
                jQuery("div#toggle-disclosure-selection").addClass('off');
            }
        },
        
        toggleDisclosureSelection: function() {
            var self = this;
            self.edit_mode = "disclosure";
            
            jQuery("div#toggle-disclosure-selection").toggleClass('on off');
            
            if (jQuery("div#toggle-disclosure-selection").hasClass('on')) {
                jQuery("div#toggle-support-selection").removeClass('on');
                jQuery("div#toggle-support-selection").addClass('off');
            }        
        },
        
        saveState: function() {
            /**
            if (!self.anyNames()) {
                evt.stop();
                alert('Please enter at least one name.');
                return false;
            } else {
                self.intervention.saveState();
                return true;
            }
            **/
            self.intervention.saveState();
            return true;
        }
    });

/**    
    // Router
    var SSNMTreeRouter = Backbone.Router.extend({
     
        routes:{
            "":"tree",
        },
     
        tree:function () {
            this.wineList = new WineCollection();
            this.wineListView = new WineListView({model:this.wineList});
            this.wineList.fetch();
            $('#sidebar').html(this.wineListView.render().el);
        },
     
        wineDetails:function (id) {
            this.wine = this.wineList.get(id);
            this.wineView = new WineView({model:this.wine});
            $('#content').html(this.wineView.render().el);
        }
    });
     
    var app = new AppRouter();
**/
    jQuery(document).ready(function() {
        var ssnmTreeView = new SupportPersonListView({ el: 'div#contentcontainer' });
    });

})(jQuery);