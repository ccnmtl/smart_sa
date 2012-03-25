(function (jQuery) {
    var global = this;
    var M = MochiKit;
    
    var Pill = Backbone.Model.extend({
        defaults: {
            name: "" 
        }
    });
    
    var PillList = Backbone.Collection.extend({ model : Pill });
    
    var PillView = Backbone.View.extend({
        initialize: function (options) {
            _.bindAll(this);
            this.parent = options.parent;
            this.ordinal = options.ordinal;
            this.dropped = false;
            this.draggable = new Draggable(this.el, { 
                revert: true,
                reverteffect: this.parent.revertEffect
            });
        },
        
        render: function () {
        }
    });
    
    var Bucket = Backbone.Model.extend({
        defaults: {
            type: "" // day or night
        }
    });
    
    var BucketList = Backbone.Collection.extend({ model : Bucket });
    
    var BucketView = Backbone.View.extend({
        
        initialize : function (options) {
            _.bindAll(this);
            this.parent = options.parent;
            
            var self = this;
            this.droppable = new M.DragAndDrop.Droppable(this.el, {
                id: this.el.id,
                accept: ['draggable'],
                greedy: 'true',
                ondrop: function (element, onto, event) { 
                    self.parent.pillDropped(element, onto, event); 
                }
            });
        }
        
    });

    var PillGameView = Backbone.View.extend({
        events: {},
        
        dropped: false,

        initialize: function (options) {
            _.bindAll(this, 'render', 'pillDropped', 'revertEffect');
            var self = this;
            
            this.pillViews = [];
            this.bucketViews = [];
            
            // pickup the pills from the DOM or the gameState
            if (options.mode == "practice") {
                jQuery("div.pill").each(function () {
                    var pill = new Pill({
                        name: jQuery(this).children("pill-text").html()
                    });
                    
                    self.pillViews.push(new PillView({ 
                        model: pill, 
                        el: jQuery(this).find(".draggable")[0], 
                        ordinal: self.pillViews.length,
                        parent: self
                    }));
                });
            } else {
            }
            
            // pick up all buckets from the DOM
            jQuery("div.pill-bucket").each(function () {
                var bucket = new Bucket({});
                
                self.bucketViews.push(new BucketView({ 
                    model: bucket, 
                    el: this,
                    parent: self
                }));
            });
        },
        
        pillDropped: function (element, onto, event) {
            var newnode;
            if (jQuery(element).hasClass("trashable")) {
                newnode = element;
            } else {
                newnode = element.cloneNode(true);
                newnode.id = "pill_" + (Math.random() + "").substring(2, 6);
                document.body.appendChild(newnode);
                jQuery(newnode).css({'float': 'none !important', 'margin': 'none', 'position': 'absolute', 'left': event._mouse.page.x - 18, 'top': event._mouse.page.y - 5, 'opacity': '1'});
                jQuery(newnode).addClass("trashable");
                new PillView({el: newnode, parent: this});
            }
            
            this.dropped = true;
        },
        
        revertEffect: function (innerelement, top_offset, left_offset) {
            var rv;
            if (jQuery(innerelement).hasClass("trashable")) {
                if (!this.dropped) {
                    document.body.removeChild(innerelement);
                }
            } else {
                var dur = 0;
                if (!this.dropped) {
                   dur = Math.sqrt(Math.abs(top_offset ^ 2) + Math.abs(left_offset ^ 2)) * 0.02;
                }
                 
                rv = new (MochiKit.Visual.Move)(innerelement, {x: - left_offset, y: - top_offset, duration: dur});
            }
            this.dropped = false;
            return rv;
        },

        
        saveState: function (evt) {
            if (!this.collection.isValid()) {
                evt.preventDefault();
                alert('Please enter at least one name.');
            } else {
                // Initiate the ajax call to saveState
                global.Intervention.saveState(function (result) {
                    if (result.response !== "ok") {
                        alert("An error occurred while saving your information. Please try again.");
                    } else {
                        window.location = evt.srcElement.href;
                    }
                });
            }
            return false;
        }
    });
    
    Backbone.sync = function (method, model, success, error) {
        // Save the results back to the game state
        // Don't do a full server-side save on every sync
        var game_state = global.Intervention.getGameVar('pillgame', {});
        var key = model.get("key");
        
        if (!_.has(game_state, key)) {
            game_state[key] = {};
        }
    };

    jQuery(document).ready(function () {
        // pick up all pills from the game state or the DOM
        var mode = jQuery("#mode").html();
        
        var pillGameView = new PillGameView({
            mode: mode,
            el: 'div#contentcontainer'
        });
        
        // Populate collection from the DOM & the game_state
        // As items are added to the collection, the ListView
        // will be signaled to create a new subview
        var game_state = global.Intervention.getGameVar('pillgame', {});

    });
}(jQuery));