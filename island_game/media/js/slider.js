var M = MochiKit;

function setpos(thing, x, y) {
  M.Style.setStyle(thing,  { "left":  (x) + 'px', "top": (y) + 'px', 'position': 'absolute'});
}
var global = this;
global.sliders = {};

function Slider(settings) {
  //setup
  var its = M.Base.partial(M.DOM.getNodeAttribute, settings);
  var ints = function (n) {
    if (its(n) === null) {
      return null;
    }
    return parseInt(its(n), 10);
  };
  this.id = its('id');
  this.background_element_id = its("background_element_id");
  this.image_offset = {x: ints('image_offset_x'), y: ints('image_offset_y') };
  this.start_offset = {x: ints('start_offset_x'), y: ints('start_offset_y') };
  this.end_offset =   {x: ints('end_offset_x'),   y: ints('end_offset_y') };
  this.min_value = ints('min_value');
  this.max_value = ints('max_value');
  this.moving_image_path = its('moving_image_path');
  this.z_index = ints('z_index');
  this.starting_value = ints('starting_value');
  this.influence = ints('influence');
  this.moving = M.DOM.IMG({'src': this.moving_image_path, 'id': this.id + '_moving' });
  if (this.z_index !== null) {
    M.Logging.logDebug("Setting " + this.id + " to " + this.z_index);
    M.Style.setStyle(this.moving, {'z-index': this.z_index});
  }

  //register this slider
  global.sliders[this.id] = this;
  this.background_position = M.DOM.getElementPosition(this.background_element_id);

  //draw fixed and moving components:


  var doc = M.DOM.currentDocument();


  this.fixed_image_path = its('fixed_image_path');
  if (this.fixed_image_path !== null) {
    M.Logging.logDebug(this.id);
    this.fixed = M.DOM.IMG({'src': this.fixed_image_path, 'id': this.id + '_fixed', 'z-index': this.z_index});
    M.DOM.appendChildNodes(doc.body, this.fixed);
    setpos(this.fixed,
      this.image_offset.x + this.background_position.x,
      this.image_offset.y + this.background_position.y
    );

    M.Style.setStyle(this.fixed, {'z-index': this.z_index});
  }
  M.DOM.appendChildNodes(doc.body, this.moving);

  // precalculate some values:
  var range = this.max_value - this.min_value;
  this.unit = {
    x: (this.end_offset.x - this.start_offset.x) / range,
    y: (this.end_offset.y - this.start_offset.y) / range
  };


  this.draggable_by_user = (its("draggable_by_user") !== "false");
  if (this.draggable_by_user) {
    M.Logging.logDebug(this.id + "is draggable by user. Setting up draggable.");
    //set up our draggable:
    this.draggable = M.DragAndDrop.Draggable(this.moving, { snap : function (x, y) {
                        return global.sliders[this.slider_id].snap(x, y);
                      }
    });
    this.draggable.options.slider_id = this.id;
    this.onchange = this.draggable.options.onchange;
  }

  // set to requested starting value:
  this.set(this.starting_value);
  return true;
}

Slider.prototype.val = function (x, y) {
  // returns the value, with respect to the slider, of a pair of mouse coordinates.
  var v = 0;
  if (this.unit.x !== 0) {
    v =  (x - this.start_offset.x - this.background_position.x) / this.unit.x;
  } else {
    v = (y - this.start_offset.y - this.background_position.y) / this.unit.y;
  }
  if (v < this.min_value) { return this.min_value; }
  if (v > this.max_value) { return this.max_value; }
  return v;
};

Slider.prototype.pos = function (v) {
  // the position of the movable part of the slider when the slider is set to a given value.
  var x = this.start_offset.x +  this.background_position.x + this.unit.x * v;
  var y = this.start_offset.y +  this.background_position.y + this.unit.y * v;
  return [x, y];
};

Slider.prototype.set = function (value) {
  // programatically set the slider at a given value.
  var p = this.pos(value);
  setpos(this.moving, p[0], p[1]);
};

Slider.prototype.get = function () {
  // the current value of the slider
  return this.val(this.moving.x, this.moving.y);
};

Slider.prototype.getfraction = function () {
  // the current value of the slider as a fraction of its max setting.
  var diff = this.max_value - this.min_value;
  return (this.get() - this.min_value) / diff;
};


Slider.prototype.snap = function (x, y) {
  // where to show it
  return this.pos(this.val(x, y));
};

function pick_image(v, images) {
  var media_path = M.DOM.getElement('media-base').getAttribute('data-image-base');

  var n = images.length;
  //logDebug(images);
  if (v !== 0) {
    var a = Math.ceil(v * n) - 1;
    return media_path + images[a];
  }
  else {
    M.Logging.logDebug("yo");
  }
  return media_path + images[0];
}

/// Other common code:
global.man_images = [
  'images/man/xhosaman4.png',
  'images/man/xhosaman3.png',
  'images/man/xhosaman2.png',
  'images/man/xhosaman1.png',
  'images/man/xhosaman.png'
];


global.woman_images = [
  'images/woman/xhosawoman4.gif',
  'images/woman/xhosawoman3.gif',
  'images/woman/xhosawoman2.gif',
  'images/woman/xhosawoman1.gif',
  'images/woman/xhosawoman.gif'
];

global.default_state = {
  'page_1_bad1' : null,
  'page_1_bad2' : null,
  'page_1_good' : null,
  'page_2_good' : null
};

global.game_state;

function clip_image(image, width, floor) {
  // sets the 'clip' style on an image so that any portion of the image below y value 'floor' is hidden.
  var hide = floor - M.DOM.elementPosition(image).y;
  M.Style.setStyle(image, { 'clip': 'rect(0 ' + width + 'px ' + hide + 'px 0)' });
}

