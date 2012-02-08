var M = MochiKit;

var buckets = {};
var pills = {};



/// THESE ARE CURRENTLY HARDWIRED.

var ax = -20;
var ay = 50;


var box_offset_from_pill_x = -40 - ax;
var box_offset_from_pill_y = -14 - ay;


var xoffset = -66 + ax; // where to start the first row and column
var yoffset = -92 + ay; //where to start the first row and column

var d = 4; // how many times we need to slice the board across and down
var xs = 110; // the width of each row
var ys = 110; // the height of each row

function setz(thing, z) {
    M.Style.setStyle(thing, {"z-index":  z});
  }

function viewing_print() {
  // Just a hack for now because I don't know enough about stylesheets to do it correctly.
  // Will fix once we get the thing to display correctly.
  return (M.Base.serializeJSON(M.Style.getStyle(M.DOM.getElement('night_pill_info_text'), 'font-family')).indexOf('Arial') === -1);
}

function tally_keys(object, key) {
    var tally = {};
    M.Base.map(function (a) {
        var newkey = object[a][key];
        if (newkey in tally) {
          tally[newkey] ++;
        } else {
          tally[newkey] = "1";
        }
      }, M.Base.keys(object));
    return tally;
  }

function add_print_med_div(info, how_many, where) {
    M.DOM.appendChildNodes(M.DOM.getElement(where),
                M.DOM.DIV({'class': 'asdasdas'}, info.pill_label + " " + how_many));
  }

function adjust_for_print() {
  if (!viewing_print()) { return; }
  var day_pill_tally = tally_keys(day_pills(), 'pill_type');
  var night_pill_tally = tally_keys(night_pills(), 'pill_type');
  M.Logging.logDebug("ADJUSTING STYLES FOR PRINT");
  M.Base.map(function (a) { }, M.DOM.getElementsByTagAndClassName('div', 'page_3_pill_info'));
  M.Base.map(function (a) { var p = pills[a]; if (p.still_in_box) { M.Style.hideElement(p.image); }}, M.Base.keys(pills));
  M.DOM.getElement('day_pill_info_text').innerHTML = "";
  M.DOM.getElement('night_pill_info_text').innerHTML = "";

  M.Base.map(function (a) {
    if (a.smart_id in day_pill_tally) {
      add_print_med_div(a, day_pill_tally[a.smart_id], 'day_pill_info_text');
    }
  }, M.Base.values(arv_pill_types)
  );

  M.Base.map(function (a) {
    if (a.smart_id in night_pill_tally) {
      add_print_med_div(a, night_pill_tally[a.smart_id], 'night_pill_info_text');
    }
  }, M.Base.values(arv_pill_types)
  );
}
function setpos(thing, x, y) {
    M.Style.setStyle(thing, { "left": (x) + 'px', "top": (y) + 'px', 'position': 'absolute' });
  }

function setposwrt(thing, x, y, wrt) { // with respect to wrt
    setpos(thing, x + M.Style.getElementPosition(wrt).x, y + M.Style.getElementPosition(wrt).y);
  }

/// more placing stuff:
function place_from_offset(item_id, image_to_place) {
    if (image_to_place === null) { image_to_place = item_id; }
    var background_id = M.DOM.getNodeAttribute(item_id, 'background');
    var x_offset_name = "x_offset_from_" + background_id;
    var y_offset_name = "y_offset_from_" + background_id;
    var x_offset_value =  parseInt(M.DOM.getNodeAttribute(item_id, x_offset_name), 10);
    var y_offset_value =  parseInt(M.DOM.getNodeAttribute(item_id, y_offset_name), 10);
    setposwrt(image_to_place, x_offset_value, y_offset_value, background_id);
  }

// This is a revised and somewhat hacked version of the grid function,
// better suited to actually displaying the actual graphics we're using.
// It can be rewritten but basically

function grid(board, n) {
    var w = M.Style.getElementDimensions(board).w; // width and height of the board
    var h = M.Style.getElementDimensions(board).h;
    var entiregrid = [];
    for (var yi = 1; yi  < d ; yi++) {
      //M.Logging.logDebug ("Starting line " + yi );
      var liney = yi *  ys;
      //M.Logging.logDebug ("Line will be at y " + liney);
      for (var xi = 1; xi < d; xi++) {
        var columnx = xi * xs;
        //M.Logging.logDebug ("Column is at x " + columnx);
        var coords = [columnx + xoffset, liney + yoffset];
        //M.Logging.logDebug ("which gives us " + coords);
        entiregrid.push(coords);
      }
    }
    return entiregrid.slice(0, n);
  }

// draws pills in the bins:
function pill_from_info(info) {
    var newpill = new Pill(info);
    newpill.still_in_box = false;

  }

function image_from_pill(smart_pill_id) {
  return M.Base.filter(function (a) { return a.smart_id === smart_pill_id; }, arv_pill_types)[0].image;
}

function build_pill(medication_label) {
    // M.Logging.logDebug ("Building a pill for " + medication_label);
    var new_settings = {
        id: medication_label,
        pill_type : medication_label,
        image_path : M.DOM.getElement('image_root').innerHTML + 'images/' +  image_from_pill(medication_label),
        offset_image :  M.DOM.getElement('pillbox').id
      };
    pills[medication_label] = new Pill(new_settings);
  }

function kill_pills() {
    if (pills !== null) {
      M.Base.map(function (x) { x.remove(); }, M.Base.values(pills));
      delete pills;
    }
  }

function draw_page() {
    //draw the page:
    place_from_offset('pillbox');
    place_from_offset(M.DOM.getElement('day').id, M.DOM.getElement('day').image);
    place_from_offset(M.DOM.getElement('night').id, M.DOM.getElement('night').image);
    place_from_offset('day_pills_time');
    setz(M.DOM.getElement('day_pills_time'), 1);
    place_from_offset('night_pills_time');
    setz(M.DOM.getElement('night_pills_time'), 1);


    //figure out where pills go in the box:
    var positions = grid(M.DOM.getElement('pillbox'), patient_meds.length);
    kill_pills();
    pills = {};

    //build pills in box:
    M.Iter.forEach(M.Iter.list(M.Iter.range(patient_meds.length)),
        function (a) { pillbox_grid_positions[patient_meds[a]] = positions[a]; }
    );
    M.Iter.forEach(patient_meds, build_pill);

    //build pills in bins:
    M.Iter.forEach(M.Base.values(game_state.day_pills), pill_from_info);
    M.Iter.forEach(M.Base.values(game_state.night_pills), pill_from_info);
    adjust_for_print();
  }

function save_state() {
    var day_pill_info = {};
    var night_pill_info = {};
    M.Iter.forEach(day_pills(),   function (pill) { day_pill_info[pill.id] =  pill.info(); });
    M.Iter.forEach(night_pills(), function (pill) { night_pill_info[pill.id] =  pill.info(); });
    game_state.day_pills = day_pill_info;
    game_state.night_pills = night_pill_info;
    game_state.day_pills_time_menu_selected_index = M.DOM.getElement('day_pills_time').selectedIndex;
    game_state.night_pills_time_menu_selected_index = M.DOM.getElement('night_pills_time').selectedIndex;
    Intervention.saveState();
  }

function time_menu_changed() {
    save_state();
  }

function set_time_menus() {
    if (game_state.day_pills_time_menu_selected_index !== null) {
      M.DOM.getElement('day_pills_time').selectedIndex = game_state.day_pills_time_menu_selected_index;
    }
    if (game_state.night_pills_time_menu_selected_index !== null) {
      M.DOM.getElement('night_pills_time').selectedIndex = game_state.night_pills_time_menu_selected_index;
    }
  }


function init() {
    if (typeof(Intervention) === "undefined") {
      alert("Log in as a client to play this game.");
      return;
    }
    M.Style.hideElement(M.DOM.getElement('image_root'));
    game_state = Intervention.getGameVar('pill_game_state',  default_state);
    patient_meds = game_state.selected_meds;
    M.Iter.forEach(M.DOM.getElementsByTagAndClassName('span', 'bucket'),
      function (a) { new Bucket(a); }
    );
    draw_page();
    M.Signals.connect('day_pills_time', 'onchange', time_menu_changed);
    M.Signals.connect('night_pills_time', 'onchange', time_menu_changed);
    // put pills from state into the buckets...
    set_time_menus();
    M.Signals.connect(window, "onresize", draw_page);
    //test();
  }

M.DOM.addLoadEvent(init);


function axe_state() {
    game_state.day_pills = {};
    game_state.night_pills = {};
    Intervention.saveState();
    window.location.reload();
  }

function pills_in_bucket(which) {
    return M.Base.filter(function (a) {return a.where === which; }, M.Base.values(pills));
  }

day_pills   = M.Base.partial(pills_in_bucket, "day");
night_pills  = M.Base.partial(pills_in_bucket, "night");





function pill_from_image(pill_image) {
    return pills[M.DOM.getElement(pill_image).pill_id];
  }

function pill_dropped(pill_image, where) {
    dragged_pill =  pill_from_image(pill_image);
    /// Create a new pill in the dropped position -- the user *thinks* this is the pill that was dragged.
    new_settings = {
        id:                 dragged_pill.pill_type + (Math.random() + "").substring(2, 6),
        pill_type :         dragged_pill.pill_type,
        image_path :        dragged_pill.image_path,
        offset_image :      where.id + "_image",
        x_offset :          M.DOM.elementPosition(pill_image, where.id + "_image").x,
        y_offset :          M.DOM.elementPosition(pill_image, where.id + "_image").y
      };
    var newpill = new Pill(new_settings);
    newpill.still_in_box = false;
    newpill.where = where.id;
    // If we dragged a pill out of the box, put it back where we started.
    if (dragged_pill.still_in_box) {
      dragged_pill.set_to_original_position();
    }
    // If we dragged a pill from a bin, remove the original pill.
    else {
      dragged_pill.remove();
    }
    save_state();
  }

function Bucket(settings) {
    var its = M.Base.partial(M.DOM.getNodeAttribute, settings);
    var ints = function (n) {
      if (its(n) === null) {
        return null;
      }
      return parseInt(its(n), 10);
    };
    this.id = its('id');
    this.image_path = its('image_path');
    this.image = M.DOM.IMG({'src': this.image_path, 'id': this.id + '_image' });
    M.DOM.appendChildNodes(M.DOM.currentDocument().body, this.image);
    place_from_offset(this.id, this.image);
    this.droppable = new M.DragAndDrop.Droppable(this.image, {
        id: this.id,
        accept: ['pill_image'],
        greedy: 'true',
        ondrop: function (e) { pill_dropped(e, this); }
      });
    buckets[this.id] = this;
    return true;
  }

function pill_dropped_outside_bin(pill_image) {
    dragged_pill = pill_from_image(pill_image);
    if (dragged_pill !== null) {
      //M.Logging.logDebug (dragged_pill.still_in_box);
      if (dragged_pill.still_in_box) {
        //M.Logging.logDebug ("Reverting normally");
        return true;
      } else {
        //M.Logging.logDebug ("Kill the pill.");
        dragged_pill.remove();
        save_state();
        return false;
      }
    }
    return true;
  }

function Pill(settings) {
    var its = function (a) { return settings[a]; };
    var ints = function (n) {
      if (its(n) === null) {
        return null;
      }
      return parseInt(its(n), 10);
    };
    this.id = its('id');
    this.x_offset = its('x_offset');
    this.y_offset = its('y_offset');
    this.pill_type = its('pill_type');
    this.where = its('where');
    this.offset_image = its('offset_image');
    this.image_path = its('image_path');
    this.image = M.DOM.IMG({'src': this.image_path, 'id': this.id + '_image', 'class': 'pill_image' });
    M.DOM.appendChildNodes(M.DOM.getElement('pill_images_container'), this.image);
    if (this.x_offset === null && this.y_offset === null) {
      //M.Logging.logDebug ("Setting to original position.");
      this.set_to_original_position();
      this.draw_box();
    } else {
      //M.Logging.logDebug ("In Pill constructor, setting to remembered position.");
      this.set_to_remembered_position();
    }

    setz(this.image, 3);
    this.draggable = new M.DragAndDrop.Draggable(this.image, { revert: pill_dropped_outside_bin });
    this.still_in_box = true;
    pills[this.id] = this;
    this.image.pill_id = this.id;
    return true;
  }

function update_keys(from_object, keys_to_update) {
    var to = {};
    M.Base.map(function (k) { to[k] = from_object[k]; }, keys_to_update);
    return to;
  }

Pill.prototype.info = function () {
    return update_keys(this, ['id', 'where', 'pill_type', 'image_path', 'offset_image', 'x_offset', 'y_offset']);
  };



Pill.prototype.remove = function () {
    M.DOM.removeElement(this.image);
    delete pills[this.id];
    return;
  };


Pill.prototype.arv_info = function () {
    var me = this;
    return M.Base.filter(function (a) { return a.smart_id === me.pill_type; }, arv_pill_types)[0];
  };




pillbox_grid_positions = {};


function nbs(n) {
  // the smallest number b for which b^2 > n.
  return  Math.ceil(Math.sqrt(n)) + 1;
}





function setpos_center(thing, x, y) {
    /// this positions the thing so its CENTER rather than its TOP LEFT is at the specified coordinates.
    setpos(thing,
        x - (M.Style.getElementDimensions(thing).w / 2),
        y - (M.Style.getElementDimensions(thing).h / 2)
    );
  }


///wrt is the id of either the pillbox, the day or the night bin IMAGE.
Pill.prototype.set_wrt = function (x, y, wrt) {
    setposwrt(this.image, x, y, wrt);
    return;
  };

/// set the offset image to be wrt, so that set_wrt can be called later on and the image
// will be properly position with respect to wrt, regardless of wrt's current position on the page.
Pill.prototype.remember_position = function (wrt) {
  this.x_offset = M.DOM.elementPosition(this.image, wrt).x;
  this.y_offset = M.DOM.elementPosition(this.image, wrt).y;
  this.offset_image = wrt;
  return;
};

Pill.prototype.set_to_remembered_position = function () {
    this.set_wrt(this.x_offset, this.y_offset, this.offset_image);
    return;
  };

Pill.prototype.set_to_original_position = function () {
    var x = pillbox_grid_positions[this.pill_type][0];
    var y = pillbox_grid_positions[this.pill_type][1];
    // TODO: use set_wrt  ?
    //setposwrt (this.image, x, y, this.offset_image);
    setposwrt(this.image, x, y, this.offset_image);

    return;
  };


Pill.prototype.draw_box = function () {
    var pill_id = this.id;
    var this_pill_info = M.Base.filter(function (a) {return a.smart_id === pill_id; }, arv_pill_types)[0];

    //TODO:
    // THESE NEED TO BE MOVED TO CSS BUT FOR NOW WE ARE PUTTING THEM HERE.

    /// END FAKE CSS

    var group_div_attrs = {
        id: 'box_behind_' + this.id,
        'class': 'page_3_pill_info'
      };
    var mg_fact_div_attrs = {
        id: 'mg_box_for' + this.id,
        'class': 'page_3_pill_info_fact mg_fact'
      };
    var hrs_fact_div_attrs = {
        id: 'mg_box_for' + this.id,
        'class': 'page_3_pill_info_fact hrs_fact'
      };

    // draw outer box around pill:
    var box_for_pill_div = M.DOM.DIV(group_div_attrs, this_pill_info.pill_label);
    M.DOM.appendChildNodes(M.DOM.getElement('game-content'), box_for_pill_div);
    setposwrt(box_for_pill_div, box_offset_from_pill_x, box_offset_from_pill_y, this.image);

    // draw "600 mg" box:
    var mg_fact_div = M.DOM.DIV(mg_fact_div_attrs, this_pill_info.dose_mg);
    M.DOM.appendChildNodes(box_for_pill_div, mg_fact_div);

    return;
  };


// not used, but keeping around in case it proves useful in the future:
function setpos_center_wrt(thing, x, y, wrt) {
    /// this positions the thing so its CENTER rather than its TOP LEFT is at the specified coordinates.
    setpos(thing,
        M.DOM.getElement(wrt).x + x - (M.Style.getElementDimensions(thing).w / 2),
        M.DOM.getElement(wrt).y + y - (M.Style.getElementDimensions(thing).h / 2)
    );
  }





//this function snaps the graphics back into place on browser window resize
//from http://forums.port80.asn.au/archive/index.php/t-8475.html
function reloadme() { //or whatver else you have
  setTimeout(function () { window.location.reload(); }, 1); //
}
window.onresize = reloadme;



function getActiveStyleSheet() {
  var i, a;
  for (i = 0; (a = document.getElementsByTagName("link")[i]); i++) {
    if (a.getAttribute("rel").indexOf("style") !== -1 && !a.disabled) {
      return a.getAttribute("title");
    }
  }
  return null;
}


