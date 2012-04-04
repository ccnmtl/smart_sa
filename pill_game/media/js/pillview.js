(function (jQuery) {
    var global = this;
    var M = MochiKit;
    
    global.dropped = false;
    global.golden_ratio_conjugate = 0.618033988749895;
    global.h = 0;
    
    function getHue() {
        if (global.h === 0)
            global.h = Math.random();
        global.h += golden_ratio_conjugate;
        global.h %= 1;
        return global.h;
    }
    
    var Pill = Backbone.Model.extend({
        defaults: {
            id: null,
            text: "",
            ordinal: 0,
            mode: '',
            color: null
        },

        /**
         * http://mjijackson.com/2008/02/rgb-to-hsl-and-rgb-to-hsv-color-model-conversion-algorithms-in-javascript
         * Converts an HSV color value to RGB. Conversion formula
         * adapted from http://en.wikipedia.org/wiki/HSV_color_space.
         * Assumes h, s, and v are contained in the set [0, 1] and
         * returns r, g, and b in the set [0, 255].
         *
         * @param   Number  h       The hue
         * @param   Number  s       The saturation
         * @param   Number  v       The value
         * @return  Array           The RGB representation
         */
        hsvToRgb: function(h, s, v){
            var r, g, b;

            var i = Math.floor(h * 6);
            var f = h * 6 - i;
            var p = v * (1 - s);
            var q = v * (1 - f * s);
            var t = v * (1 - (1 - f) * s);

            switch(i % 6){
                case 0: r = v; g = t; b = p; break;
                case 1: r = q; g = v; b = p; break;
                case 2: r = p; g = v; b = t; break;
                case 3: r = p; g = q; b = v; break;
                case 4: r = t; g = p; b = v; break;
                case 5: r = v; g = p; b = q; break;
            }

            return [Math.floor(r * 255), Math.floor(g * 255), Math.floor(b * 255)   ];
        },
        initialize: function() {
            if (this.get("color") === null) {
                var a = this.hsvToRgb(getHue(), 0.99, 0.99);
                this.set("color", "rgb(" + a[0] + "," + a[1] + "," + a[2] + ")");
            }
        }
    });
    
    var PillList = Backbone.Collection.extend({ 
        model : Pill,
        practiceList: function () {
            this.add(new Pill({ id: 'd4t', text: 'D4T<br />2 pills twice a day', ordinal: 1, mode: 'practice', color: "red" }));
            this.add(new Pill({ id: '3tc', text: '3TC<br />2 pills twice a day', ordinal: 2, mode: 'practice', color: "blue" }));
            this.add(new Pill({ id: 'efavirenz', text: 'Efavirenz<br />1 pill in the evening', ordinal: 3, mode: 'practice', color: "green" }));
        }
    });
    
    var DraggablePillView = Backbone.View.extend({
        initialize: function (options, render) {
            _.bindAll(this, "revertEffect");
            this.draggable = new Draggable(this.el, { 
                revert: true,
                reverteffect: this.revertEffect
            });
        },
        revertEffect: function (innerelement, top_offset, left_offset) {
            var dur = 0;
            if (!global.dropped) {
               dur = Math.sqrt(Math.abs(top_offset ^ 2) + Math.abs(left_offset ^ 2)) * 0.02;
            }
            
            global.dropped = false;
            return new (MochiKit.Visual.Move)(innerelement, {x: - left_offset, y: - top_offset, duration: dur});
        }
    });
    
    var TrashablePillView = Backbone.View.extend({
        initialize: function (options, render) {
            _.bindAll(this, "revertEffect");
            this.parent = options.parent;
            this.draggable = new Draggable(this.el, { 
                revert: true,
                reverteffect: this.revertEffect
            });
        },
        revertEffect: function (innerelement, top_offset, left_offset) {
            var rv;
            if (jQuery(innerelement).hasClass("trashable")) {
                if (!global.dropped) {
                    this.parent.trigger("trashPill", innerelement.id); // delete me
                }
            }
            global.dropped = false;
            return rv;
        }
    });

    var BucketView = Backbone.View.extend({
        events: {
          'change select': 'onSelectTime'   
        },
        
        initialize : function (options) {
            _.bindAll(this, "onSelectTime", "onTrashPill");
            _.extend(this, Backbone.Events);
            this.on("trashPill", this.onTrashPill);
            
            this.pillViews = {}; // keep track of anything dropped
            
            var self = this;
            this.droppable = new M.DragAndDrop.Droppable(this.el, {
                id: this.el.id,
                accept: ['draggable'],
                greedy: 'true',
                ondrop: function (element, onto, event) { 
                    if (jQuery(self.el).children(".pill-bucket").hasClass("disabled")) {
                        return false;
                    } else if (jQuery(element).hasClass("trashable")) {
                        newnode = element;
                    } else {
                        var newnode = element.cloneNode(true);
                        newnode.id = "pill_" + (Math.random() + "").substring(2, 6);
                        document.body.appendChild(newnode);
                        
                        jQuery(newnode).css({'float': 'none !important', 'margin': 'none', 'position': 'absolute', 'left': event._mouse.page.x - 18, 'top': event._mouse.page.y - 5, 'opacity': '1'});
                        jQuery(newnode).addClass("trashable");
                        
                        // @todo initialize with the model?
                        self.pillViews[newnode.id] = new TrashablePillView({el: newnode, parent: self});
                    }
                    global.dropped = true;
                }
            });
        },
        
        onTrashPill : function (pillId) {
            this.pillViews[pillId].remove();
            delete this.pillViews[pillId];
        },
        
        onSelectTime : function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var na = jQuery(srcElement).children("option:selected.na");
            if (na.length) {
                jQuery(srcElement).parent().prev(".pill-bucket").addClass("disabled");
                for (var id in this.pillViews) {
                    this.onTrashPill(id);
                }
            } else {
                jQuery(srcElement).parent().prev(".pill-bucket").removeClass("disabled");
            }
        }
    });

    var PillGameView = Backbone.View.extend({
        events: {
            'click .add-a-pill': 'onNewPill',
            'click .pill-text span': 'onEdit',
            'blur .pill-text input': 'onReadOnly'
        },

        initialize: function (options) {
            _.bindAll(this, 'addPill', 'onEdit', 'onReadOnly', 'onNewPill');
            
            this.pills = options.pills;
            this.pills.bind('add', this.addPill);
            
            // pick up buckets from the DOM
            jQuery("div.pill-bucket-container").each(function () {
                new BucketView({ el: this });
            });
        },
        
        addPill: function (pill) {
            var elt = jQuery(".pill-template").clone();
            
            jQuery(elt).attr("id", "pill_" + (Math.random() + "").substring(2, 6));
            jQuery(elt).removeClass('pill-template'); // visible
            jQuery(elt).addClass(pill.get("mode")); // practice || real
            
            var css = { 
               'background-image': '-webkit-gradient(radial, 65% 35%, 1, center center, 30, from(#ffffff), to(' + pill.get("color") + '))'
            };
            
            jQuery(elt).find(".pill-image").css(css);
            jQuery(elt).find(".draggable").css(css);
            jQuery(elt).find(".pill-text span").html(pill.get("text"));
            jQuery(elt).appendTo("#pill-list");
            
            new DraggablePillView({ model: pill, el: jQuery(elt).find('span.draggable') });  
        },
        
        onNewPill: function (evt) {
            this.pills.add(new Pill({ 'ordinal': this.pills.length + 1 }));
        },
        
        onRemovePill: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            
            // Remove this pill from view 
            
            // Tell the buckets to remove any views they have on this pill
        },
        
        onEdit: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).next('input').show().focus();
            jQuery(srcElement).hide();
        },
        
        onReadOnly: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var val = jQuery(srcElement).val();
            console.log(val);
            
            if (val.length) {
                jQuery(srcElement).prev('span').html(val).show();
                jQuery(srcElement).hide();
            }   
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
        var mode = jQuery("#mode").html();
        
        var pills = new PillList();
        var pillGameView = new PillGameView({
            mode: mode,
            el: 'div#contentcontainer',
            pills: pills
        });
        
        if (mode === 'practice') {
            pills.practiceList();
        } else {
            var game_state = global.Intervention.getGameVar('pillgame', {});
        }
    });
}(jQuery));