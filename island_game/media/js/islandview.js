(function (jQuery) {
    var global = this;
    var M = MochiKit;
    
    var GameElement = Backbone.Model.extend({
        defaults: {
            name: "",
            influence: 0,
            clip_floor: 0,
            min_value : 0,
            max_value : 0,
            starting_value : 0,
            start_offset: { x: 0, y: 0 },
            end_offset: { x: 0, y: 0 },
            draggable: false
        },
        
        initialize : function (options) {
            var range = this.get("max_value") - this.get("min_value");
            this.set("unit", {
                x: (this.get("end_offset").x - this.get("start_offset").x) / range,
                y: (this.get("end_offset").y - this.get("start_offset").y) / range
            });
        }
    });
    
    var GameElementList = Backbone.Collection.extend({ model : GameElement });

    
    var FigureView = Backbone.View.extend({
        initialize : function (options) {
            _.bindAll(this, "selectFigure", "update");
            var self = this;
        },
        
        male_images: [
            'man/xhosaman4.png',
            'man/xhosaman3.png',
            'man/xhosaman2.png',
            'man/xhosaman1.png',
            'man/xhosaman.png'
        ],
        
        female_images: [
            'woman/xhosawoman4.gif',
            'woman/xhosawoman3.gif',
            'woman/xhosawoman2.gif',
            'woman/xhosawoman1.gif',
            'woman/xhosawoman.gif'
        ],
                  
        media_path: "/site_media/island_game/images/",
        
        selectFigure: function (altitude) {
            var images = (this.gender === "M") ? this.male_images : this.female_images;
          
            if (altitude !== 0) {
                var i = Math.ceil(altitude * images.length) - 1;
                this.el.src = this.media_path + images[i];
            }
        },
        
        update: function (altitude, top) {
            this.selectFigure(altitude);
            jQuery(this.el).css("top", top + jQuery(this.el).height() / 4);
        }
    });

    
    var SliderView = Backbone.View.extend({
        initialize : function (options) {
            _.bindAll(this, "val", "pos", "setValue", "getValue", "getfraction", "snap", "top");
            var self = this;
            
            this.parent = options.parent;
            
            if (this.model.get("draggable")) {
                this.draggable = M.DragAndDrop.Draggable(this.el, {
                    snap : function (x, y) {
                        return self.snap(x, y);
                    }
                });
                this.draggable.options.slider_id = this.el.id;
                this.draggable.options.onchange = function () { self.parent.trigger("recalc"); };
            }

            // set to requested starting value:
            this.setValue(this.model.get("starting_value"));
        },
        
        val: function (x, y) {
            // returns the value, with respect to the slider, of a pair of mouse coordinates.
            var v = 0;
            if (this.model.get("unit").x !== 0) {
                v =  (x - this.model.get("start_offset").x) / this.model.get("unit").x;
            } else {
                v = (y - this.model.get("start_offset").y) / this.model.get("unit").y;
            }
            if (v < this.model.get("min_value")) {
                return this.model.get("min_value");
            } else if (v > this.model.get("max_value")) {
                return this.model.get("max_value");
            } else {
                return v;
            }
        },

        pos: function (v) {
            // the position of the movable part of the slider when the slider is set to a given value.
            var x = this.model.get("start_offset").x + this.model.get("unit").x * v;
            var y = this.model.get("start_offset").y + this.model.get("unit").y * v;
            return [x, y];
        },

        setValue: function (value) {
            // programatically set the slider at a given value.
            var p = this.pos(value);
            jQuery(this.el).css({ "left":  (p[0]) + 'px', "top": (p[1]) + 'px' });
            
            this.clipImage();
        },

        getValue: function () {
            // the current value of the slider
            var pos = jQuery(this.el).position();
            return this.val(pos.left, pos.top);
        },

        getfraction: function () {
            // the current value of the slider as a fraction of its max setting.
            var diff = this.model.get("max_value") - this.model.get("min_value");
            return (this.getValue() - this.model.get("min_value")) / diff;
        },
        
        snap: function (x, y) {
            // where to show it
            return this.pos(this.val(x, y));
        },
        
        clipImage: function () {
            // sets the 'clip' style on an image so that any portion of the image below y value 'floor' is hidden.
            var floor = this.model.get("clip_floor");
            if (floor > 0) {
                var width = M.Style.getElementDimensions(this.el).w;
                var hide = this.model.get("clip_floor") - M.DOM.elementPosition(this.el).y;
                M.Style.setStyle(this.el, { 'clip': 'rect(0 ' + width + 'px ' + (hide - 10) + 'px 0)' });
            }
        },
        
        top: function (val) {
            if (val) {
                jQuery(this.el).css("top", val);
            } else {
                return jQuery(this.el).position().top;
            }
        }
    });
    
    
    var IslandGameView = Backbone.View.extend({
        events: {
        },

        initialize : function (options) {
            _.bindAll(this, "recalc", "gameFloor", "addGameElement", "waterLevel");
            _.extend(this, Backbone.Events);
            
            this.views = {};
            this.gender = options.gender;
            this.collection = options.collection;
            this.collection.bind('add', this.addGameElement);
            
            this.on("recalc", this.recalc);
        },
        
        addGameElement: function (element) {
            var name = element.get("name");
            if (name === 'figure') {
                this.views[name] = new FigureView({ model: element, el: jQuery("#" + name) });
            } else {
                this.views[name] = new SliderView({ model: element, el: jQuery("#" + name), parent: this }).render();
            }
        },
        
        gameFloor: function () {
            // represents the bottom of the game. island & water are clipped as they slide.
            return jQuery(this.el).offset().top + jQuery(this.el).height();
        },
        
        waterLevel: function () {
            return (this.views.infection.getValue() + this.views.viral_load.getValue()) / 2;
        },
        
        recalc: function (msg) {
            this.views.water.setValue(this.waterLevel());

            //adjust island level:
            var island_level = this.views.cd4_count.getValue();
            this.views.island.setValue(island_level);
            
            var altitude = 0.5 + (this.views.island.getfraction() - this.views.water.getfraction()) / 2;
            this.views.figure.update(altitude, this.views.island.top());
        }
    });
    
    Backbone.sync = function (method, model, success, error) {

    };

    jQuery(document).ready(function () {
        var elements = new GameElementList();
        var islandView = new IslandGameView({
            el: 'div#island_container',
            gender: global.Intervention.current_user.gender,
            collection: elements
        });
        
        var model = new GameElement({
            name: "figure",
            min_value: 0,
            max_value: 10,
            starting_value: 10,
            start_offset: { x: 21, y: 300 },
            end_offset: { x: 21, y: 100 }
        });
        elements.add(model);
        
        model = new GameElement({
            name: "island",
            min_value: 0,
            max_value: 10,
            starting_value: 10,
            start_offset: { x: 21, y: 300 },
            end_offset: { x: 21, y: 100 },
            clip_floor: islandView.gameFloor()
        });
        elements.add(model);
        
        model = new GameElement({
            name: "water",
            min_value: 0,
            max_value: 10,
            starting_value: 0,
            start_offset: { x: 21, y: 400 },
            end_offset: { x: 21, y: 200 },
            clip_floor: islandView.gameFloor()
        });
        elements.add(model);
        
        model = new GameElement({
            name: "infection",
            influence: 1.0,
            min_value: 0,
            max_value: 10,
            starting_value: 0,
            start_offset: { x: 50, y: 245 },
            end_offset: { x: 50, y: 154 },
            draggable: true
        });
        elements.add(model);
                    
        model = new GameElement({
            name: "viral_load",
            influence: 1.0,
            starting_value: 0,
            min_value: 0,
            max_value: 10,
            start_offset: { x: 100, y: 245 },
            end_offset: { x: 100, y: 154 },
            draggable: true
        });
        elements.add(model);
        
        model = new GameElement({
            name: "cd4_count",
            influence: 1.0,
            min_value: 0,
            max_value: 10,
            starting_value: 10,
            start_offset: { x: 150, y: 245 },
            end_offset: { x: 150, y: 154 },
            draggable: true
        });
        elements.add(model);
        
        model = new GameElement({
            name: "adherence",
            min_value: 0,
            max_value: 10,
            starting_value: 10,
            start_offset: { x: 500, y: 245 },
            end_offset: { x: 500, y: 154 },
            draggable: true
        });
        elements.add(model);
        
        islandView.trigger("recalc");
        
    });
}(jQuery));