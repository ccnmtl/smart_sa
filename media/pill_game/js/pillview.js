(function (jQuery) {
    var M = MochiKit;
    var global = this;
    global.dropped = false;
    
    var ColorStack = Backbone.Model.extend({
        defaults: {
            colors: [ "#000", // black
                      "#F69E94", // salmon
                      "#964B00", // brown
                      "#FBFF00", // yellow
                      "#A020F0 ", // purple
                      "#FF7B00", // orange
                      "#FF1493", // deep pink
                      "#00FF00", // green
                      "#0000FF", // blue
                      "#FF0000" // red
                     ]
        },
        
        get: function () {
            return this.attributes.colors.pop();
        },
        
        put: function (color) {
            this.attributes.colors.push(color);
        },
        
        remove: function (color) {
            for (var i = 0; i < this.attributes.colors.length; i++) {
                if (this.attributes.colors[i] === color) {
                    this.attributes.colors.splice(i, 1);
                }
            }
        }
    });
    
    var Pill = Backbone.Model.extend({
        defaults: {
            id: null,
            name: "",
            mode: '',
            color: null
        },
        initialize: function (options) {
            if (options) {
                this.set('id', options.id);
                this.set('name', options.name);
                this.set('color', options.color);
            }
        },
        as_dict: function () {
            return {
                'id': this.get('id'),
                'name': this.get('name'),
                'color': this.get('color')
            };
        }
    });
    
    var PillList = Backbone.Collection.extend({
        model : Pill,
        as_array: function () {
            var archive = [];
            this.forEach(function (item) {
                archive.push(item.as_dict());
            });
            return archive;
        }
    });
    
    /*
     * Droppable Pill List Item
     */
    var PillView = Backbone.View.extend({
        events: {
            'click .pill-delete-image': 'onRemovePill',
            'click .pill-text span': 'onEdit',
            'blur .pill-text input': 'onReadOnly',
            'change .pill-text input': 'onChangeName',
            'keypress .pill-text input': 'onChangeName',
            'keyup .pill-text input': 'onChangeName'
        },
        template: _.template(' \
                <div id=<%= id %> class="pill <%= mode %>"> \
                    <div class="pill-delete"> \
                        <input id="delete" class="pill-delete-image" type="image" src="/site_media/pill_game/images/button-delete.2.png" name="image" width="16" height="16"/> \
                    </div> \
                    <div class="pill-image" \
                        style="background-image: -webkit-gradient(radial, 65% 35%, 1, center center, 30, from(#ffffff), to(<%= color %>)); \
                               filter: progid:DXImageTransform.Microsoft.gradient(startColorStr="#ffffff", EndColorStr="<%= color %>"); /* IE6,IE7 */ \
                               -ms-filter: progid:DXImageTransform.Microsoft.gradient(startColorStr="#ffffff", EndColorStr="<%= color %>"); /* IE8 */ \
                               background-image: -moz-radial-gradient(65% 35% 45deg, circle , #ffffff 1%, <%= color %> 100%); "> \
                        <span data-id="<%= id %>" class="draggable" \
                            style="background-image: -webkit-gradient(radial, 65% 35%, 1, center center, 30, from(#ffffff), to(<%= color %>)); \
                                   filter: progid:DXImageTransform.Microsoft.gradient(startColorStr="#ffffff", EndColorStr="<%= color %>"); /* IE6,IE7 */ \
                                   -ms-filter: progid:DXImageTransform.Microsoft.gradient(startColorStr="#ffffff", EndColorStr="<%= color %>"); /* IE8 */ \
                                   background-image: -moz-radial-gradient(65% 35% 45deg, circle , #ffffff 1%, <%= color %> 100%); "> \
                        </span> \
                    </div> \
                    <div class="pill-text"><span><%= name %></span><input type="text" value="<%= name %>"></input></div> \
                </div>'),

        initialize: function (options, render) {
            _.bindAll(this, "render", "unrender", "revertEffect", "onRemovePill", "onEdit", "onReadOnly", "onChangeName");
            this.gameView = options.gameView;
            this.model.bind("destroy", this.unrender);
            this.render();
        },
        focus: function () {
            jQuery(this.el).find(".pill-text input").focus();
        },
        render: function () {
            this.el.innerHTML = this.template(this.model.toJSON());
            
            if (this.model.get("name").length > 0) {
                jQuery(this.el).find(".pill-text input").hide();
            } else {
                jQuery(this.el).find(".pill-text span").hide();
            }

            var elt = jQuery(this.el).find("span.draggable")[0];
            this.draggable = new M.DragAndDrop.Draggable(elt, {
                revert: true,
                reverteffect: this.revertEffect
            });
        },
        unrender: function () {
            jQuery(this.el).remove();
            this.unbind();
            this.gameView.trigger("removePill", this.model.get("id"));
        },
        revertEffect: function (innerelement, top_offset, left_offset) {
            var dur = 0;
            if (!global.dropped) {
                dur = Math.sqrt(Math.abs(top_offset ^ 2) + Math.abs(left_offset ^ 2)) * 0.02;
            }
            
            global.dropped = false;
            return new (MochiKit.Visual.Move)(innerelement, {x: - left_offset, y: - top_offset, duration: dur});
        },
        onChangeName: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var val = jQuery(srcElement).val();
            this.model.set("name", val);
            this.gameView.trigger("save");
        },
        onEdit: function (evt) {
            if (this.model.get("mode") !== "practice") {
                var srcElement = evt.srcElement || evt.target || evt.originalTarget;
                jQuery(srcElement).next('input').show().focus();
                jQuery(srcElement).hide();
            }
        },
        onReadOnly: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var val = jQuery(srcElement).val();
            
            if (val.length) {
                jQuery(srcElement).prev('span').html(val).show();
                jQuery(srcElement).hide();
                return true;
            }
        },
        onRemovePill: function () {
            this.model.destroy();
        }
    });
    
    /*
     * Bucketed Pill View
     */
    var DroppedPillView = Backbone.View.extend({
        tagname: 'span',
        template: _.template(' \
            <span data-id="<%= id %>" id="<%= viewId %>" class="draggable trashable" \
                style="background-image: -webkit-gradient(radial, 65% 35%, 1, 50% 50%, 30, from(rgb(255, 255, 255)), to(<%= color %>)); \
                       background-image: -moz-radial-gradient(65% 35% 45deg, circle , #ffffff 1%, <%= color %> 100%); \
                       filter: progid:DXImageTransform.Microsoft.gradient(startColorStr="#ffffff", EndColorStr="<%= color %>"); /* IE6,IE7 */ \
                       -ms-filter: progid:DXImageTransform.Microsoft.gradient(startColorStr="#ffffff", EndColorStr="<%= color %>"); /* IE8 */ \
                       z-index: 1000; opacity: 1;"> \
            </span>'),
        initialize: function (options, render) {
            _.bindAll(this, "render", "unrender", "revertEffect", "as_dict");
            this.model.bind("destroy", this.unrender); // If a draggable pill is deleted by the user

            this.viewId = options.viewId || "view_" + (Math.random() + "").substring(2, 6);
            this.bucket = options.bucket;
            this.left = options.left;
            this.top = options.top;
            
            this.render();
        },
        render: function () {
            var json = this.model.toJSON();
            json.left = this.left;
            json.top = this.top;
            json.viewId = this.viewId;
            
            this.el.innerHTML = this.template(json);
            jQuery(this.el).css({ position: 'absolute', left: this.left, top: this.top });

            var elt = jQuery(this.el).find("span.draggable")[0];
            this.draggable = new M.DragAndDrop.Draggable(elt, {
                revert: true,
                reverteffect: this.revertEffect
            });
        },
        unrender: function () {
            this.remove();
            this.unbind();
            this.model.unbind("destroy", this.unrender);
            this.bucket.trigger("trashPill", this.viewId); // delete me
        },
        revertEffect: function (innerelement, top_offset, left_offset) {
            if (!global.dropped) {
                this.unrender();
            }
            global.dropped = false;
        },
        as_dict: function () {
            return {
                'pillId': this.model.get("id"),
                'left': jQuery(this.el).css("left"),
                'top': jQuery(this.el).css("top")
            };
        }
    });

    var BucketView = Backbone.View.extend({
        events: {
            'change select': 'onSelectTime'
        },
        
        initialize : function (options) {
            _.bindAll(this, "onSelectTime", "onTrashPill", "addPillView", "dropPill", "render", "as_dict");
            _.extend(this, Backbone.Events);
            this.on("trashPill", this.onTrashPill);
            this.gameView = options.gameView;
            this.pillViews = {};
            
            if (options.printContainer) {
                this.printEl = jQuery("<div class='medication_reminder_bucket'></div>")[0];
                options.printContainer.append(this.printEl);
                this.template = _.template(jQuery("#printable-bucket-template").html());
            }
            
            if (options.selected) {
                if (options.selected === "na") {
                    jQuery(this.el).find(".pill-bucket").addClass("disabled");
                }
                jQuery(this.el).find("select").val(options.selected);
            }
            
            for (var i = 0; options.views && i < options.views.length; i++) {
                this.addPillView(options.views[i]);
            }
            
            var self = this;
            this.droppable = new M.DragAndDrop.Droppable(this.el, {
                id: this.el.id,
                accept: ['draggable', 'trashable'],
                greedy: 'true',
                ondrop: this.dropPill
            });
        },
        
        addPillView: function (options) {
            var pill = this.gameView.pills.get(options.pillId);
            if (pill) {
                var view = new DroppedPillView({
                    bucket: this,
                    model: pill,
                    left: options.left,
                    top: options.top
                });
                
                jQuery(this.el).append(view.el);
                this.pillViews[view.viewId] = view;
            }
        },
        
        dropPill: function (element, onto, event) {
            if (jQuery(this.el).children(".pill-bucket").hasClass("disabled")) {
                return false; // Disabled
            }
            
            if (jQuery(element).hasClass("trashable") && _.has(this.pillViews, element.id)) {
                global.dropped = true;
            } else {
                var pillId = jQuery(element).data("id");
                var pill = this.gameView.pills.get(pillId);
                if (pill.get("name").length < 1) {
                    alert("Please enter a name for this medication before continuing, or delete the line by clicking the red x at the left.");
                    return false;
                }
                
                var elt = jQuery(element).offset();
                var me = jQuery(this.el).offset();
                
                this.addPillView({
                    'pillId': pillId,
                    'left': (elt.left - me.left) + "px",
                    'top': (elt.top - me.top) + "px"
                });
                global.dropped = !jQuery(element).hasClass("trashable");
            }
            this.render();
            this.gameView.trigger("save");
        },
        
        // triggered when a DroppedPillView is removed (unrendered)
        onTrashPill: function (viewId) {
            delete this.pillViews[viewId];
            this.render();
            this.gameView.trigger("save");
        },
        
        onSelectTime : function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var na = jQuery(srcElement).children("option:selected.na");
            if (na.length) {
                jQuery(srcElement).parent().prev(".pill-bucket").addClass("disabled");
                for (var viewId in this.pillViews) {
                    if (this.pillViews.hasOwnProperty(viewId)) {
                        this.pillViews[viewId].unrender();
                    }
                }
            } else {
                jQuery(srcElement).parent().prev(".pill-bucket").removeClass("disabled");
            }
            this.render();
            this.gameView.trigger("save");
        },
        
        render: function (evt) {
            if (this.printEl) {
                var context = { time: jQuery(this.el).find("select").val(), pills: {} };
                for (var viewId in this.pillViews) {
                    if (this.pillViews.hasOwnProperty(viewId)) {
                        var p = this.pillViews[viewId].model;
                        var name = p.get("name");
                        if (!_.has(context.pills, name)) {
                            context.pills[name] = { name: name, count: 0 };
                        }
                        context.pills[name].count++;
                    }
                }
                if (_.size(context.pills) > 0) {
                    this.printEl.innerHTML = this.template(context);
                } else {
                    this.printEl.innerHTML = "";
                }
            }
            
            // also update the time span for printing purposes
            var val = jQuery(this.el).find("select").val();
            var span = jQuery(this.el).find("span.timelabel")[0];
            jQuery(span).html("Take medication at: " + val);
        },
        
        as_dict: function () {
            var d = { id: this.el.id, views: [] };
            for (var viewId in this.pillViews) {
                if (this.pillViews.hasOwnProperty(viewId)) {
                    d.views.push(this.pillViews[viewId].as_dict());
                }
            }
            d.selected = jQuery(this.el).find("select").val();
            return d;
        }
    });

    var PillGameView = Backbone.View.extend({
        events: {
            'click .add-a-pill': 'onNewPill'
        },

        initialize: function (options) {
            _.bindAll(this, 'addPill', 'removePill', 'onNewPill', 'saveState');
            _.extend(this, Backbone.Events);
            var self = this;
            
            this.mode = options.mode;
            
            this.colorStack = new ColorStack();
            
            this.pills = options.pills;
            
            this.pills.bind("add", this.addPill);
            this.on("save", this.saveState);
            this.on("removePill", this.removePill);
            
            // pick up buckets from the DOM
            this.buckets = [];
        },
        
        addPill: function (pill) {
            var view = new PillView({ model: pill, gameView: this });
            this.colorStack.remove(pill.get("color"));
            jQuery("#pill-list").append(view.el);
            view.focus();
        },
        
        removePill: function (pillId) {
            var pill = this.pills.get(pillId);
            this.colorStack.put(pill.get("color"));
            this.pills.remove(pillId);
            this.trigger("save");
        },
        
        onNewPill: function (evt) {
            // Let's limit this to 10 pills
            if (this.pills.length >= 10) {
                alert("You can only enter 10 pills. Please delete one before continuing");
            } else {
                var rgb = this.colorStack.get();
                var pill = new Pill({ 'id': "pill_" + (Math.random() + "").substring(2, 6), 'color': rgb });
                this.pills.add(pill);
                this.trigger("save");
            }
        },
        
        saveState: function () {
            if (this.mode !== "practice") {
                global.pillRegimenState.setState("pills", this.pills.as_array());
                
                var buckets = [];
                for (var bucket in this.buckets) {
                    if (this.buckets.hasOwnProperty(bucket)) {
                        var view = this.buckets[bucket];
                        global.pillRegimenState.setState(view.el.id, view.as_dict());
                    }
                }
                
                // Initiate the ajax call to saveState
                global.Intervention.saveState(function (result) {
                    if (result.status !== 200) {
                        alert("An error occurred while saving your information. Please try again.");
                    }
                });
            }
        }
    });
    
    Backbone.sync = function (method, model, success, error) {
    };

    jQuery(document).ready(function () {
        var mode = jQuery("#mode").html();
        var pills = new PillList();
        
        global.pillRegimenState = new global.GameState({ game: 'pill_game', el: 'div#defaulter' });
        
        var pillGameView = new PillGameView({
            mode: mode,
            pills: pills,
            el: jQuery("div#contentcontainer")
        });
        
        if (mode === 'practice') {
            pills.add(new Pill({ id: 'tdf', name: 'Tenofovir (TDF)<br />1 pill in the evening', mode: 'practice', color: "red" }));
            pills.add(new Pill({ id: '3tc', name: 'Lamivudine (3TC)<br />1 pill in the evening', mode: 'practice', color: "blue" }));
            pills.add(new Pill({ id: 'efavirenz', name: 'Efavirennz (EFV)<br />1 pill in the evening', mode: 'practice', color: "green" }));
        } else {
            var savedPills = global.pillRegimenState.getState("pills");
            for (var i = 0; savedPills && i < savedPills.length; i++) {
                pills.add(new Pill(savedPills[i]));
            }
        }
        
        jQuery("div.pill-bucket-container").each(function () {
            var options;
            if (mode === 'practice') {
                options = { el: this, gameView: pillGameView };
            } else {
                options = global.pillRegimenState.getState(this.id) || {};
                options.el = this;
                options.gameView = pillGameView;
                options.printContainer = jQuery("#medication-reminder");
            }
            var bucketView = new BucketView(options);
            pillGameView.buckets.push(bucketView);
            bucketView.render();
        });

    });
}(jQuery));