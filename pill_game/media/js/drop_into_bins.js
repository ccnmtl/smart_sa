addLoadEvent(init);

buckets = {};
pills = {}



/// THESE ARE CURRENTLY HARDWIRED.

ax = -20;
ay = 50;


box_offset_from_pill_x = -40 - ax;
box_offset_from_pill_y = -14 - ay;


xoffset = -66 + ax; // where to start the first row and column
yoffset = -92 + ay; //where to start the first row and column

d = 4; // how many times we need to slice the board across and down
xs = 110; // the width of each row
ys = 110; // the height of each row
    

function init() {
    if (typeof (Intervention) == "undefined" ) {
        alert ("Log in as a client to play this game.");
        return;
    }
    hideElement($('image_root'));
    game_state = Intervention.getGameVar('pill_game_state',  default_state);
    patient_meds = game_state.selected_meds;
    forEach (getElementsByTagAndClassName('span', 'bucket'),
        function (a) { new Bucket (a) }
    );
    draw_page();
    connect ('day_pills_time', 'onchange', time_menu_changed);
    connect ('night_pills_time', 'onchange', time_menu_changed);
    // put pills from state into the buckets...
    set_time_menus();
    connect(window, "onresize", draw_page );
    //test();
}

function draw_page () {
    //draw the page:
    place_from_offset ('pillbox');
    place_from_offset ($('day').id, $('day').image);
    place_from_offset ($('night').id, $('night').image);
    place_from_offset ('day_pills_time');
    setz($('day_pills_time'), 1);
    place_from_offset ('night_pills_time');
    setz($('night_pills_time'), 1);
    
    
    //figure out where pills go in the box:
    positions = grid ($('pillbox'), patient_meds.length);
    kill_pills();
    pills = {};
    
    //build pills in box:
    forEach(list(range(patient_meds.length)),
        function (a) { pillbox_grid_positions [patient_meds[a]] = positions[a]; }     
    );
    forEach ( patient_meds, build_pill);
    
    //build pills in bins:
    forEach(values(game_state.day_pills), pill_from_info);
    forEach(values(game_state.night_pills), pill_from_info);
    adjust_for_print();   
}


function viewing_print () {
    // Just a hack for now because I don't know enough about stylesheets to do it correctly.
    // Will fix once we get the thing to display correctly.
    return (serializeJSON(getStyle($('night_pill_info_text'), 'font-family')).indexOf ('Arial') == -1)
}


function tally_keys (object, key) {
    tally = {};
    map (function (a) {
        newkey = object[a][key]
        if (newkey in  tally ) {
             tally [newkey] ++;
        } else {
            tally [newkey] = "1";
        }
    }, keys (object));
    return tally;
}

function adjust_for_print() {

    if (!viewing_print ()) return;
    
    day_pill_tally = tally_keys (day_pills(), 'pill_type');
    
    night_pill_tally = tally_keys (night_pills(), 'pill_type');

    logDebug ("ADJUSTING STYLES FOR PRINT");
    
    map(function (a) {
        }, getElementsByTagAndClassName('div', 'page_3_pill_info'));
    
        
        map (function (a) { p = pills[a]; if (p.still_in_box) hideElement(p.image) }, keys(pills));
        $('day_pill_info_text').innerHTML = "";
        $('night_pill_info_text').innerHTML = "";
        

        ///////////////
        map (
            function (a) {
                if (a.smart_id in day_pill_tally) {
                    add_print_med_div (a, day_pill_tally[a.smart_id], 'day_pill_info_text');
                }    
            }, values(arv_pill_types)
        );
        ///////////////
        
        map (
            function (a) {
                if (a.smart_id in night_pill_tally) {
                    add_print_med_div (a, night_pill_tally[a.smart_id], 'night_pill_info_text');
                }    
            }, values(arv_pill_types)
        );

        
}

function add_print_med_div(info, how_many, where) {
    appendChildNodes( $(where), 
                DIV ({class: 'asdasdas'}, info.pill_label + " " + how_many));
}

function kill_pills() {
    if (pills != null) {
        map (function(x){ x.remove()}, values(pills) );
        delete pills;
    }
}




function image_from_pill (smart_pill_id) {
    return filter ( function(a) { return a.smart_id == smart_pill_id}, arv_pill_types)[0].image;
}

function set_time_menus() {
    if (game_state.day_pills_time_menu_selected_index != null) {
        $('day_pills_time').selectedIndex = game_state.day_pills_time_menu_selected_index;
    }
    if (game_state.night_pills_time_menu_selected_index != null) {
        $('night_pills_time').selectedIndex = game_state.night_pills_time_menu_selected_index;
    }
}

function time_menu_changed ()  {
    save_state();
}

function axe_state() {
    game_state.day_pills = {};
    game_state.night_pills = {};
    Intervention.saveState();
    window.location.reload()
}

function save_state() {
    day_pill_info = {};
    night_pill_info = {};
    forEach (day_pills(),   function (pill) { day_pill_info   [pill.id] =  pill.info() }); 
    forEach (night_pills(), function (pill) { night_pill_info [pill.id] =  pill.info() });
    game_state.day_pills = day_pill_info;
    game_state.night_pills = night_pill_info;
    game_state.day_pills_time_menu_selected_index = $('day_pills_time').selectedIndex;
    game_state.night_pills_time_menu_selected_index = $('night_pills_time').selectedIndex;
    Intervention.saveState();
}

function build_pill (medication_label) {
   // logDebug ("Building a pill for " + medication_label);
   new_settings = {
        id: medication_label,
        pill_type : medication_label,
        image_path : $('image_root').innerHTML + 'images/' +  image_from_pill(medication_label),
        offset_image :  $('pillbox').id
    }
    pills [medication_label] = new Pill(new_settings);
}


function pills_in_bucket(which) {
    return filter (function (a) {return a.where == which; }, values(pills));
}
day_pills   = partial(pills_in_bucket, "day");
night_pills  = partial(pills_in_bucket, "night");


function Bucket (settings) {
    its = partial (getNodeAttribute, settings);
    ints = function (n) {if (its(n) == null) return null; return parseInt (its(n)) };
    this.id = its('id');
    this.image_path = its('image_path');
    this.image = IMG({'src': this.image_path, 'id': this.id + '_image', });
    appendChildNodes(currentDocument().body, this.image);
    place_from_offset (this.id, this.image);
    this.droppable = new Droppable(this.image, {
        id:this.id,
        accept: ['pill_image'],
        greedy:'true',
        ondrop:function(e){pill_dropped(e, this)},
    });
    buckets [this.id] = this;
    return true;
}

function Pill (settings) {
    its = function (a) { return settings[a]; }
    ints = function (n) {if (its(n) == null) return null; return parseInt (its(n)) };
    this.id = its('id');
    this.x_offset = its('x_offset');
    this.y_offset = its('y_offset');
    this.pill_type = its('pill_type');
    this.where = its('where');
    this.offset_image = its('offset_image');
    this.image_path = its('image_path');
    this.image = IMG({'src': this.image_path, 'id': this.id + '_image', 'class': 'pill_image' });
    appendChildNodes($('pill_images_container'), this.image);
    if (this.x_offset == null && this.y_offset == null) {
        //logDebug ("Setting to original position.");
        this.set_to_original_position();
        this.draw_box();
    } else {
        //logDebug ("In Pill constructor, setting to remembered position.");
        this.set_to_remembered_position();
    }
    
    setz(this.image, 3);
    this.draggable = new Draggable (this.image, { revert: pill_dropped_outside_bin });
    this.still_in_box = true;
    pills [this.id] = this;
    this.image.pill_id = this.id
    return true;
}

Pill.prototype.info = function() {
    return update_keys (this, ['id', 'where', 'pill_type', 'image_path', 'offset_image', 'x_offset', 'y_offset']);
}

function update_keys (from_object, keys_to_update) {
    to = {};
    map ( function (k) { to[k] = from_object[k]; }, keys_to_update)
    return to;
}

// draws pills in the bins:
function pill_from_info (info) {
    newpill = new Pill (info);
    newpill.still_in_box = false;

}

Pill.prototype.remove = function() {
    removeElement(this.image);
    delete pills[this.id];
    return;
}


Pill.prototype.arv_info = function() {
    me = this;
    return  filter ( function(a) { return a.smart_id == me.pill_type}, arv_pill_types)[0];
}

function pill_dropped_outside_bin (pill_image) {
    dragged_pill = pill_from_image(pill_image);
    if (dragged_pill != null ) {
        //logDebug (dragged_pill.still_in_box);
        if (dragged_pill.still_in_box) {
            //logDebug ("Reverting normally");
            return true;
        } else {
            //logDebug ("Kill the pill.");
            dragged_pill.remove();
            save_state();
            return false;
        }
    } else {
        //logDebug ("Dragged pill was null.");
    }
    return true;
}

function pill_from_image (pill_image) {
    return pills[$(pill_image).pill_id];
}

function pill_dropped(pill_image, where) {
    dragged_pill =  pill_from_image (pill_image);
    /// Create a new pill in the dropped position -- the user *thinks* this is the pill that was dragged.
    new_settings = {
        id:                 dragged_pill.pill_type + (Math.random() + "").substring(2,6),
        pill_type :         dragged_pill.pill_type,
        image_path :        dragged_pill.image_path,
        offset_image :      where.id + "_image",
        x_offset :          elementPosition (pill_image, where.id + "_image").x,
        y_offset :          elementPosition (pill_image, where.id + "_image").y,
    }
    newpill = new Pill (new_settings);
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

pillbox_grid_positions = {}
/*
function grid (board, n) {
    w = getElementDimensions(board).w; // width and height of the board
    h = getElementDimensions(board).h;
    d = nbs (n); // how many times we need to slice the board across and down
    logDebug (d);
    xs = Math.floor(w / d); // the width of each slice
    ys = Math.floor(h / d); // the height of each slice
    logDebug (xs);
    logDebug (ys);
    entiregrid = []
    for (yi = 1; yi  < d; yi++) {
        logDebug ("Starting line " + yi );
        liney = yi *  ys;
        
        logDebug ("Line will be at y " + liney);
        for (xi = 1; xi < d; xi++) {
            columnx = xi * xs;
            
            logDebug ("Column is at x " + columnx);
            coords = [columnx, liney];
            logDebug ("which gives us " + coords);
            entiregrid.push (coords);
        }
    }
    return entiregrid.slice (0,n);
}
*/


// This is a revised and somewhat hacked version of the grid function,
// better suited to actually displaying the actual graphics we're using.
// It can be rewritten but basically

function grid (board, n) {
    w = getElementDimensions(board).w; // width and height of the board
    h = getElementDimensions(board).h;
    /*
    /// THESE ARE CURRENTLY HARDWIRED.
    d = 4; // how many times we need to slice the board across and down
    xs = 110; // the width of each slice
    ys = 110; // the height of each slice
    xoffset = 0;
    yoffset = 0;
    */
    entiregrid = []
    for (yi = 1; yi  < d ; yi++) {
        //logDebug ("Starting line " + yi );
        liney = yi *  ys;
        //logDebug ("Line will be at y " + liney);
        for (xi = 1; xi < d; xi++) {
            columnx = xi * xs;
            //logDebug ("Column is at x " + columnx);
            coords = [columnx + xoffset, liney + yoffset];
            //logDebug ("which gives us " + coords);
            entiregrid.push (coords);
        }
    }
    return entiregrid.slice (0,n);
}

function nbs (n) {
    // the smallest number b for which b^2 > n.
    return  Math.ceil (Math.sqrt(n)) + 1
}

/// more placing stuff:
function place_from_offset (item_id, image_to_place) {
    if (image_to_place == null) { image_to_place = item_id; }
    background_id = getNodeAttribute(item_id, 'background');
    x_offset_name = "x_offset_from_" + background_id ;
    y_offset_name = "y_offset_from_" + background_id ;
    x_offset_value =  parseInt(getNodeAttribute (item_id, x_offset_name));
    y_offset_value =  parseInt(getNodeAttribute (item_id, y_offset_name));
    setposwrt (image_to_place, x_offset_value, y_offset_value, background_id);
}


function setpos (thing, x, y) {
    setStyle( thing,  { "left":  ( x  ) + 'px', "top" : ( y ) + 'px', 'position':'absolute' } );
}

function setpos_center( thing, x, y ) {
    /// this positions the thing so its CENTER rather than its TOP LEFT is at the specified coordinates.
    setpos ( thing,
        x - (getElementDimensions(thing).w / 2),
        y - (getElementDimensions(thing).h / 2)
    );
}

function setposwrt (thing, x, y, wrt) { // with respect to wrt
    setpos ( thing,    x +  getElementPosition(wrt).x,    y +  getElementPosition(wrt).y    );
}

///wrt is the id of either the pillbox, the day or the night bin IMAGE.
Pill.prototype.set_wrt = function(x, y, wrt) {
    setposwrt (this.image, x, y, wrt);
    return;
}

/// set the offset image to be wrt, so that set_wrt can be called later on and the image
// will be properly position with respect to wrt, regardless of wrt's current position on the page.
Pill.prototype.remember_position = function(wrt) {
    this.x_offset = elementPosition (this.image, wrt).x
    this.y_offset = elementPosition (this.image, wrt).y
    this.offset_image = wrt;
    return;
}

Pill.prototype.set_to_remembered_position = function() {
    this.set_wrt (this.x_offset, this.y_offset, this.offset_image);
    return;
}

Pill.prototype.set_to_original_position = function() {
    x = pillbox_grid_positions[this.pill_type][0];
    y = pillbox_grid_positions[this.pill_type][1];
    // TODO: use set_wrt  ?
    //setposwrt (this.image, x, y, this.offset_image);
    setposwrt (this.image, x, y, this.offset_image);
    
    return;
}


Pill.prototype.draw_box = function() {
    pill_id = this.id
    this_pill_info = filter (function(a) {return a.smart_id == pill_id }, arv_pill_types)[0];
    
    //TODO:
    // THESE NEED TO BE MOVED TO CSS BUT FOR NOW WE ARE PUTTING THEM HERE.
    
    /// END FAKE CSS
    
    group_div_attrs = {
        id:'box_behind_' + this.id,
        class:'page_3_pill_info'
    }
    mg_fact_div_attrs = {
        id:'mg_box_for' + this.id,
        class:'page_3_pill_info_fact mg_fact'
    }
    hrs_fact_div_attrs = {
        id:'mg_box_for' + this.id,
        class:'page_3_pill_info_fact hrs_fact'
    }
    
    // draw outer box around pill:
    box_for_pill_div =  DIV(group_div_attrs, this_pill_info.pill_label);
    appendChildNodes($('game-content'),box_for_pill_div);
    setposwrt(box_for_pill_div, box_offset_from_pill_x, box_offset_from_pill_y, this.image);
    
    // draw "600 mg" box:
    mg_fact_div = DIV ( mg_fact_div_attrs, this_pill_info.dose_mg );
    appendChildNodes(box_for_pill_div,mg_fact_div);
    
    // draw "Every 24 hours" box:
    /*
    hrs_fact_div = DIV (hrs_fact_div_attrs, this_pill_info.every_x_hrs);
    appendChildNodes(box_for_pill_div,hrs_fact_div);
    */
    return;
}


// not used, but keeping around in case it proves useful in the future:
function setpos_center_wrt( thing, x, y, wrt ) {
    /// this positions the thing so its CENTER rather than its TOP LEFT is at the specified coordinates.
    setpos ( thing,
        $(wrt).x +  x - (getElementDimensions(thing).w / 2),
        $(wrt).y + y - (getElementDimensions(thing).h / 2)
    );
}

function setz (thing, z) {
    setStyle( thing,  { "z-index":  z} );
}




//this function snaps the graphics back into place on browser window resize
//from http://forums.port80.asn.au/archive/index.php/t-8475.html
window.onresize= reloadme;
function reloadme(){ //or whatver else you have
setTimeout("window.location.reload()",1); //
}


 
function getActiveStyleSheet() {
var i, a;
 for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
  if(a.getAttribute("rel").indexOf("style") != -1
//  && a.getAttribute("title")
  && !a.disabled) return a.getAttribute("title");
  }
  return null;
}


