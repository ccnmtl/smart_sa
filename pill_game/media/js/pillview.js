(function (jQuery) {
    var M = MochiKit;
    var global = this;
    global.dropped = false;
    
    var RandomColorGenerator = Backbone.Model.extend({
        defaults: {
            golden_ratio_conjugate: 0.618033988749895,
            h: Math.random()
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
        hsvToRgb: function (h, s, v) {
            var r, g, b;

            var i = Math.floor(h * 6);
            var f = h * 6 - i;
            var p = v * (1 - s);
            var q = v * (1 - f * s);
            var t = v * (1 - (1 - f) * s);

            switch (i % 6) {
            case 0:
                r = v;
                g = t;
                b = p;
                break;
            case 1:
                r = q;
                g = v;
                b = p;
                break;
            case 2:
                r = p;
                g = v;
                b = t;
                break;
            case 3:
                r = p;
                g = q;
                b = v;
                break;
            case 4:
                r = t;
                g = p;
                b = v;
                break;
            case 5:
                r = v;
                g = p;
                b = q;
                break;
            }

            return [Math.floor(r * 255), Math.floor(g * 255), Math.floor(b * 255)   ];
        },
        
        hue: function () {
            var h = this.get("h");
            h += this.get("golden_ratio_conjugate");
            h %= 1;
            this.set("h", h);
            return h;
        },
        
        rgb: function () {
            var a = this.hsvToRgb(this.hue(), 0.99, 0.99);
            return "rgb(" + a[0] + "," + a[1] + "," + a[2] + ")";
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
                        style="background-image: -webkit-gradient(radial, 65% 35%, 1, center center, 30, from(#ffffff), to(<%= color %>))"> \
                        <span data-id="<%= id %>" class="draggable" \
                            style="background-image: -webkit-gradient(radial, 65% 35%, 1, center center, 30, from(#ffffff), to(<%= color %>))"> \
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
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).next('input').show().focus();
            jQuery(srcElement).hide();
        },
        onReadOnly: function (evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var val = jQuery(srcElement).val();
            
            if (val.length) {
                jQuery(srcElement).prev('span').html(val).show();
                jQuery(srcElement).hide();
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
                z-index: 1000; position: absolute; left: <%= left %>; top: <%= top %>; opacity: 1;"> \
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
                'left': jQuery("#" + this.viewId).css("left"),
                'top': jQuery("#" + this.viewId).css("top")
            };
        }
    });

    var BucketView = Backbone.View.extend({
        events: {
            'change select': 'onSelectTime'
        },
        
        initialize : function (options) {
            _.bindAll(this, "onSelectTime", "onTrashPill", "addPillView", "dropPill", "as_dict");
            _.extend(this, Backbone.Events);
            this.on("trashPill", this.onTrashPill);
            this.gameView = options.gameView;
            this.pillViews = {};
            
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
                
                document.body.appendChild(view.el);
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
                var offset = jQuery(element).offset();
                this.addPillView({
                    'pillId': jQuery(element).data("id"),
                    'left': offset.left + "px",
                    'top': offset.top + 5 + "px"
                });
                global.dropped = !jQuery(element).hasClass("trashable");
            }
            this.gameView.trigger("save");
        },
        
        // triggered when a DroppedPillView is removed (unrendered)
        onTrashPill: function (viewId) {
            delete this.pillViews[viewId];
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
            this.gameView.trigger("save");
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
            
            this.colorGenerator = new RandomColorGenerator();
            
            this.pills = options.pills;
            
            this.pills.bind("add", this.addPill);
            this.on("save", this.saveState);
            this.on("removePill", this.removePill);
            
            // pick up buckets from the DOM
            this.buckets = [];
        },
        
        addPill: function (pill) {
            var view = new PillView({ model: pill, gameView: this });
            jQuery("#pill-list").append(view.el);
            view.focus();
        },
        
        removePill: function (pillId) {
            this.pills.remove(pillId);
            this.trigger("save");
        },
        
        onNewPill: function (evt) {
            var rgb = this.colorGenerator.rgb();
            var pill = new Pill({ 'id': "pill_" + (Math.random() + "").substring(2, 6), 'color': rgb });
            this.pills.add(pill);
            this.trigger("save");
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
                    if (result.responseText !== "ok") {
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
            pills.add(new Pill({ id: 'd4t', name: 'D4T<br />2 pills twice a day', mode: 'practice', color: "red" }));
            pills.add(new Pill({ id: '3tc', name: '3TC<br />2 pills twice a day', mode: 'practice', color: "blue" }));
            pills.add(new Pill({ id: 'efavirenz', name: 'Efavirenz<br />1 pill in the evening', mode: 'practice', color: "green" }));
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
            }
            pillGameView.buckets.push(new BucketView(options));
        });

    });
}(jQuery));