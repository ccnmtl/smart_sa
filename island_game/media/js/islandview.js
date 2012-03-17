(function (jQuery) {
    var global = this;
    var M = MochiKit;
    
    var GameElement = Backbone.Model.extend({
        defaults: {
            name: "",
            min_value : 0,
            max_value : 10,
            starting_value : 0,
            value: 0,
            start_offset: { x: 0, y: 0 },
            end_offset: { x: 0, y: 0 },
            draggable: false,
            gender: "",
            enabled: true,
            visible: true,
            horizontal_range: 0,
            vertical_range: 0
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

    var GameElementView = Backbone.View.extend({
        initialize : function (options) {
            _.bindAll(this, "val", "pos", "setValue", "getValue", "resetValue", "getFraction", "render");
            this.model.bind('change:value', this.render);
            this.model.bind('change:visible', this.render);
            
            this.parent = options.parent;
            this.offset = jQuery(this.parent.el).position();
            
            this.initializePosition();
            this.resetValue();
            this.render();
        },
        
        initializePosition: function () {
            var position = jQuery(this.el).position();
            var offset = this.offset;
            
            this.model.set("start_offset", { x: position.left + offset.left, y: position.top + offset.top + this.model.get("vertical_range") });
            this.model.set("end_offset", { x: position.left + offset.left + this.model.get("horizontal_range"), y: position.top + offset.top });
        },
        
        resetValue: function () {
            this.model.set("value", this.model.get("starting_value"));
        },
        
        setValue: function (value) {
            this.model.set("value", value);
        },
        
        hide: function () {
            this.model.set("visible", false);
        },
        
        show: function () {
            this.model.set("visible", true);
        },
        
        disable: function () {
            this.model.set("enabled", false);
        },
        
        enable: function () {
            this.model.set("enabled", true);
        },
        
        getValue: function () {
            // the current value of the slider
            var pos = jQuery(this.el).position();
            return this.val(pos.left, pos.top);
        },

        getFraction: function () {
            // the current value of the slider as a fraction of its max setting.
            var diff = this.model.get("max_value") - this.model.get("min_value");
            return (this.getValue() - this.model.get("min_value")) / diff;
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
        
        render: function () {
            if (this.model.get("visible")) {
                jQuery(this.el).show();
            } else {
                jQuery(this.el).hide();
            }
            
            // position the image properly at the given value
            var value = this.model.get("value");
            var p = this.pos(value);
            
            jQuery(this.el).css({ "left":  (p[0]) + 'px', "top": (p[1]) + 'px' });
        }
    });
    
    
    // Island & Water
    var SlidingElementView = GameElementView.extend({
        initialize : function (options) {
            _.bindAll(this, "render", "clipImage", "top");

            this.model.set("vertical_range", 225);
            
            GameElementView.prototype.initialize.call(this, options);
        },
    
        render: function () {
            GameElementView.prototype.render.call(this);
            this.clipImage();
        },
        
        clipImage: function () {
            // sets the 'clip' style on an image so that any portion of the image below y value 'floor' is hidden.
            var floor = this.parent.gameFloor();
            if (floor > 0) {
                var width = jQuery(this.el).width();
                var hide = floor - jQuery(this.el).offset().top;
                jQuery(this.el).css('clip', 'rect(0 ' + width + 'px ' + hide + 'px 0)');
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
    
    // Infection (oi), Viral Load, CD4 Count, Adherence
    var DraggableElementView = GameElementView.extend({
        initialize : function (options) {
            _.bindAll(this, "snap", "render");
            this.model.bind('change:enabled', this.render);
            this.model.set("vertical_range", 90);
            
            var self = this;
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
            
            GameElementView.prototype.initialize.call(this, options);
        },
        
        snap: function (x, y) {
            // where to show the slider value
            var val = GameElementView.prototype.val.call(this, x, y);
            return GameElementView.prototype.pos.call(this, val);
        },
        
        initializePosition: function () {
            // Set the start_offset & end_offset based on the sliders
            // initial left/top properties as specified in the .css
            // offset these positioning elements by the parent container
            // plus a "height" as specified in the model.
            // This properly specified in .css screwed things up.
            var position = jQuery(this.el).position();
            var offset = this.offset;
            
            // position labels & background images appropriately
            var slider = jQuery(this.el).siblings(".slider")[0];
            var sliderPos = jQuery(slider).position();
            jQuery(slider).css({ left: sliderPos.left + offset.left, top: sliderPos.top + offset.top });
            
            var label = jQuery(this.el).siblings(".slider_label")[0];
            var labelPos = jQuery(label).position();
            jQuery(label).css({ left: labelPos.left + offset.left, top: labelPos.top + offset.top });
            
            this.model.set("start_offset", { x: position.left + offset.left, y: position.top + offset.top + this.model.get("vertical_range") });
            this.model.set("end_offset", { x: position.left + offset.left, y: position.top + offset.top });
        },
        
        render: function () {
            if (this.model.get("enabled")) {
                jQuery("." + this.model.get("name")).css('opacity', 1);
            } else {
                jQuery("." + this.model.get("name")).css('opacity', 0.5);
            }
            
            if (this.model.get("visible")) {
                jQuery(this.el).siblings(".slider_label").show();
                jQuery(this.el).siblings(".slider").show();
            } else {
                jQuery(this.el).siblings(".slider_label").hide();
                jQuery(this.el).siblings(".slider").hide();
            }
            
            GameElementView.prototype.render.call(this);

        },
    });
    
    var FigureView = GameElementView.extend({
        initialize : function (options) {
            _.bindAll(this, "update", "selectImage", "render");
            
            GameElementView.prototype.initialize.call(this, options);
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
        
        selectImage: function (value) {
            var images = (this.model.get("gender") === "M") ? this.male_images : this.female_images;
            
            if (value === 0) {
                this.el.src = this.media_path + images[0];
            } else {
                var i = Math.ceil(value * images.length) - 1;
                if (i >= 0 && i <= images.length) {
                    this.el.src = this.media_path + images[i];
                }
            }
        },
        
        render: function () {
            GameElementView.prototype.render.call(this);
            this.selectImage(GameElementView.prototype.getFraction.call(this));
        },

        update: function (altitude, top) {
            this.selectImage(altitude);
            jQuery(this.el).css("top", top + jQuery(this.el).height() / 4);
        }
    });
    
    var IslandGame = Backbone.Model.extend({
        defaults: {
            beforeMedication: true
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
            
            this.model.set("floor", jQuery(this.el).offset().top + jQuery(this.el).height());
            this.model.bind('change', this.render);
            
            this.views = {};
            
            this.collection = new GameElementList();
            this.collection.bind('add', this.addGameElement);
            
            this.collection.add(new GameElement({ name: "figure1", starting_value: 10, gender: options.gender }));
            this.collection.add(new GameElement({ name: "figure2", starting_value: 10, horizontal_range: 250, vertical_range: 90, gender: options.gender, visible: false }));
            this.collection.add(new GameElement({ name: "island", vertical_range: 225, starting_value: 10 }));
            this.collection.add(new GameElement({ name: "water" }));
            this.collection.add(new GameElement({ name: "infection", draggable: true }));
            this.collection.add(new GameElement({ name: "viral_load", draggable: true }));
            this.collection.add(new GameElement({ name: "cd4_count", starting_value: 10, draggable: true }));
            this.collection.add(new GameElement({ name: "adherence", starting_value: 10, draggable: true, visible: false  }));
            
            this.render();
        },
        
        addGameElement: function (element) {
            var name = element.get("name");
            var opts = { model: element, el: jQuery("#" + name), parent: this};
            
            if (name === 'figure1' || name === 'figure2') {
                this.views[name] = new FigureView(opts);
            } else if (element.get("draggable")) {
                this.views[name] = new DraggableElementView(opts);
            } else {
                this.views[name] = new SlidingElementView(opts);
            }
        },
        
        gameFloor: function () {
            return this.model.get("floor");
        },
        
        waterLevel: function () {
            return (this.views.infection.getValue() + this.views.viral_load.getValue()) / 2;
        },
        
        beforeMedicationView: function () {
            this.views.infection.resetValue();
            this.views.viral_load.resetValue();
            this.views.cd4_count.resetValue();

            this.model.set("beforeMedication", true);
        },
        
        afterMedicationView: function () {
            this.views.adherence.resetValue();
            this.model.set("beforeMedication", false);
        },
        
        render: function () {
            if (this.model.get("beforeMedication")) {
                jQuery("img#right").show();
                jQuery("img#left").hide();
                jQuery("span#island_view_label").html("BEFORE GOING ON ARVS");
                jQuery("img#island").attr("src", "/site_media/island_game/images/island_part1.png");
                
                this.views.adherence.hide();
                this.views.infection.enable();
                this.views.viral_load.enable();
                this.views.cd4_count.enable();
                
                this.views.figure2.hide();
                this.views.figure1.show();

                this.views.water.setValue(this.waterLevel());
    
                var island_level = this.views.cd4_count.getValue();
                this.views.island.setValue(island_level);
                
                var altitude = 0.5 + (this.views.island.getFraction() - this.views.water.getFraction()) / 2;
                this.views.figure1.update(altitude, this.views.island.top());
            } else {
                jQuery("img#right").hide();
                jQuery("img#left").show();
                jQuery("span#island_view_label").html("ON ARVS");
                jQuery("img#island").attr("src", "/site_media/island_game/images/island_part2.png");
                
                this.views.figure1.hide();
                this.views.figure2.show();
                
                this.views.adherence.show();
                this.views.infection.disable();
                this.views.viral_load.disable();
                this.views.cd4_count.disable();
                this.views.island.setValue(10);
                
                var health = this.views.adherence.getValue();
                this.views.water.setValue(10 - health);
                this.views.infection.setValue(10 - health);
                this.views.viral_load.setValue(10 - health);
                this.views.cd4_count.setValue(health);
                this.views.figure2.setValue(health);
            }
        }
    });
    
    Backbone.sync = function (method, model, success, error) {
        // Island View State is not saved
    };

    jQuery(document).ready(function () {
        var islandView = new IslandGameView({
            model: new IslandGame({ beforeMedication: true }),
            el: 'div#island_container',
            gender: global.Intervention.current_user.gender
        });
    });
}(jQuery));