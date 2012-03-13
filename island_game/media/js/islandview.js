(function (jQuery) {
    var global = this;
    var M = MochiKit;
    
    var GameElement = Backbone.Model.extend({
        defaults: {
            name: "",
            clip_floor: 0,
            min_value : 0,
            max_value : 10,
            starting_value : 0,
            start_offset: { x: 0, y: 0 },
            end_offset: { x: 0, y: 0 },
            draggable: false,
            gender: "",
            enabled: true
        },
        
        initialize : function (options) {
            
        },
        
        unit: function () {
            var range = this.get("max_value") - this.get("min_value");
            return {
                x: (this.get("end_offset").x - this.get("start_offset").x) / range,
                y: (this.get("end_offset").y - this.get("start_offset").y) / range
            };
        }
    });
    
    var GameElementList = Backbone.Collection.extend({ model : GameElement });

    var SliderView = Backbone.View.extend({
        initialize : function (options) {
            _.bindAll(this, "val", "pos", "setValue", "getValue", "getfraction", "snap", "top", "render");
            var self = this;
            
            this.parent = options.parent;
            
            if (this.model.get("draggable")) {
                this.draggable = M.DragAndDrop.Draggable(this.el, {
                    snap : function (x, y) {
                        if (self.model.get("enabled")) {
                            return self.snap(x, y);
                        }
                    }
                });
                this.draggable.options.slider_id = this.el.id;
                this.draggable.options.onchange = function () {
                    if (self.model.get("enabled")) {
                        self.parent.trigger("render");
                    }
                };
            }

            // set to requested starting value:
            this.setValue(this.model.get("starting_value"));
            
            this.model.bind('change:enabled', this.render);
        },
        
        disable: function () {
            this.model.set("enabled", false);
        },
        
        enable: function () {
            this.model.set("enabled", true);
        },
        
        render: function () {
            if (this.model.get("enabled")) {
                jQuery("." + this.model.get("name")).css('opacity', 1);
            } else {
                jQuery("." + this.model.get("name")).css('opacity', 0.5);
            }
        },
        
        val: function (x, y) {
            // returns the value, with respect to the slider, of a pair of mouse coordinates.
            var v = 0;
            var unit = this.model.unit();
            if (unit.x !== 0) {
                v =  (x - this.model.get("start_offset").x) / unit.x;
            } else {
                v = (y - this.model.get("start_offset").y) / unit.y;
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
            var unit = this.model.unit();
            var x = this.model.get("start_offset").x + unit.x * v;
            var y = this.model.get("start_offset").y + unit.y * v;
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
    
    var FigureView = SliderView.extend({
        initialize : function (options) {
            _.bindAll(this, "update", "setValue");
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
        
        images: function () {
            return (this.model.get("gender") === "M") ? this.male_images : this.female_images;
        },
        
        selectImage: function (value) {
            var images = this.images();
            
            if (value === 0) {
                this.el.src = this.media_path + images[0];
            } else {
                var i = Math.ceil(value * images.length) - 1;
                this.el.src = this.media_path + images[i];
            }
        },
        
        setValue: function (value) {
            SliderView.prototype.setValue.call(this, value);
            this.selectImage(SliderView.prototype.getfraction.call(this));
        },
        
        update: function (altitude, top) {
            this.selectImage(altitude);
            jQuery(this.el).css("top", top + jQuery(this.el).height() / 4);
        }
    });
    
    var IslandGame = Backbone.Model.extend({
        defaults: {
            beforeMedication: true
        },
        
        initialize : function (options) {
        }
    });
    
    
    var IslandGameView = Backbone.View.extend({
        events: {
            'click img#right' : 'afterMedicationView',
            'click img#left': 'beforeMedicationView'
        },
        
        initialize : function (options) {
            _.bindAll(this, "render", "gameFloor", "addGameElement", "waterLevel", 'afterMedicationView', 'beforeMedicationView');
            _.extend(this, Backbone.Events);
            this.on("render", this.render);
            
            this.views = {};
            this.collection = options.collection;
            this.collection.bind('add', this.addGameElement);
            this.model.bind('change', this.render);
        },
        
        addGameElement: function (element) {
            var name = element.get("name");
            if (name === 'figure') {
                element.set("gender", this.model.get("gender"));
                this.views[name] = new FigureView({ model: element, el: jQuery("#" + name) });
            } else {
                this.views[name] = new SliderView({ model: element, el: jQuery("#" + name), parent: this });
            }
        },
        
        gameFloor: function () {
            // represents the bottom of the game. island & water are clipped as they slide.
            return jQuery(this.el).offset().top + jQuery(this.el).height();
        },
        
        waterLevel: function () {
            return (this.views.infection.getValue() + this.views.viral_load.getValue()) / 2;
        },
        
        beforeMedicationView: function () {
            jQuery("img#right").show();
            jQuery("img#left").hide();
            jQuery("span#island_view_label").html("BEFORE GOING ON ARVS");
            jQuery("img#island").attr("src", "/site_media/island_game/images/island_part1.png");
            
            jQuery("#adherence_label").hide();
            jQuery("#adherence_slider").hide();
            jQuery("#adherence").hide();
            
            jQuery("#figure").addClass("figure_one");
            jQuery("#figure").removeClass("figure_two");
            
            this.views.infection.enable();
            this.views.viral_load.enable();
            this.views.cd4_count.enable();
            
            var start_offset = { x: 21, y: 300 };
            var end_offset = { x: 21, y: 100 };
            this.views.figure.model.set("start_offset", start_offset);
            this.views.figure.model.set("end_offset", end_offset);
            
            this.views.infection.setValue(0);
            this.views.viral_load.setValue(0);
            this.views.cd4_count.setValue(10);
            this.model.set("beforeMedication", true);
        },
        
        afterMedicationView: function () {
            jQuery("img#right").hide();
            jQuery("img#left").show();
            jQuery("span#island_view_label").html("ON ARVS");
            jQuery("img#island").attr("src", "/site_media/island_game/images/island_part2.png");
            
            jQuery("#adherence_label").show();
            jQuery("#adherence_slider").show();
            jQuery("#adherence").show();
            
            jQuery("#figure").removeClass("figure_one");
            jQuery("#figure").addClass("figure_two");
            
            var start_offset = { x: 150, y: 200 };
            var end_offset = { x: 400, y: 125 };
            this.views.figure.model.set("start_offset", start_offset);
            this.views.figure.model.set("end_offset", end_offset);

            this.views.infection.disable();
            this.views.viral_load.disable();
            this.views.cd4_count.disable();
            
            this.views.adherence.setValue(10);
            this.views.infection.setValue(0);
            this.views.viral_load.setValue(0);
            this.views.cd4_count.setValue(10);

            this.model.set("beforeMedication", false);
        },
        
        render: function () {
            if (this.model.get("beforeMedication")) {
                this.views.water.setValue(this.waterLevel());
    
                var island_level = this.views.cd4_count.getValue();
                this.views.island.setValue(island_level);
                
                var altitude = 0.5 + (this.views.island.getfraction() - this.views.water.getfraction()) / 2;
                this.views.figure.update(altitude, this.views.island.top());
            } else {
                this.views.island.setValue(10);
                
                var health = this.views.adherence.getValue();
                this.views.water.setValue(10 - health);
                this.views.infection.setValue(10 - health);
                this.views.viral_load.setValue(10 - health);
                this.views.cd4_count.setValue(health);
                this.views.figure.setValue(health);
            }
        }
    });
    
    Backbone.sync = function (method, model, success, error) {

    };

    jQuery(document).ready(function () {
        var elements = new GameElementList();
        var islandView = new IslandGameView({
            model: new IslandGame(),
            collection: elements,
            el: 'div#island_container',
        });
        
        var model = new GameElement({
            name: "figure",
            starting_value: 10,
            gender: global.Intervention.current_user.gender
        });
        elements.add(model);
        
        model = new GameElement({
            name: "island",
            starting_value: 10,
            start_offset: { x: 21, y: 300 },
            end_offset: { x: 21, y: 100 },
            clip_floor: islandView.gameFloor()
        });
        elements.add(model);
        
        model = new GameElement({
            name: "water",
            starting_value: 0,
            start_offset: { x: 21, y: 400 },
            end_offset: { x: 21, y: 175 },
            clip_floor: islandView.gameFloor()
        });
        elements.add(model);
        
        model = new GameElement({
            name: "infection",
            starting_value: 0,
            start_offset: { x: 50, y: 245 },
            end_offset: { x: 50, y: 154 },
            draggable: true
        });
        elements.add(model);
                    
        model = new GameElement({
            name: "viral_load",
            starting_value: 0,
            start_offset: { x: 100, y: 245 },
            end_offset: { x: 100, y: 154 },
            draggable: true
        });
        elements.add(model);
        
        model = new GameElement({
            name: "cd4_count",
            starting_value: 10,
            start_offset: { x: 150, y: 245 },
            end_offset: { x: 150, y: 154 },
            draggable: true
        });
        elements.add(model);
        
        model = new GameElement({
            name: "adherence",
            starting_value: 10,
            start_offset: { x: 500, y: 245 },
            end_offset: { x: 500, y: 154 },
            draggable: true
        });
        elements.add(model);
        
        islandView.trigger("render");
    });
}(jQuery));