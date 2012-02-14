// how high  the guy is standing on the island
var guy_on_island_offset = 150;
var M = MochiKit;
var global = this;

var recalc = function () {
    //adjust water level:
    var water_level = (
        global.sliders.bad1.get() * global.sliders.bad1.influence +
        global.sliders.bad2.get() * global.sliders.bad2.influence) / 2;
    global.sliders.water.set(water_level);

    //adjust island level:
    var island_level = (global.sliders.good.get() * global.sliders.good.influence);
    global.sliders.island.set(island_level);
    var island_height = global.sliders.island.pos(global.sliders.island.get())[1];

    //pick an image for the dude:
    var dude_images = (global.Intervention.current_user.gender === "M") ? global.man_images : global.woman_images;
    var altitude = 0.5 + (global.sliders.island.getfraction() - global.sliders.water.getfraction()) / 2;
    M.DOM.getElement('dude').src = global.pick_image(altitude, dude_images);

    //adjust the dude
    M.DOM.setStyle('dude', {
        "left":  (M.DOM.getElement('dude').x) + 'px',
        "top" : (island_height - guy_on_island_offset) + 'px',
        'position': 'absolute',
        'height': '184px',
        'width': '110px'
      });

    global.clip_image(M.DOM.getElement('island_moving'), 600, global.bottom_of_game);
    global.clip_image(M.DOM.getElement('water_moving'), 600, global.bottom_of_game);
  };

function init() {
    global.game_state = global.Intervention.getGameVar('island_game_state', global.default_state);

    M.Iter.forEach(MochiKit.D.getElementsByTagAndClassName('span', 'slider'),
             function (a) { new global.Slider(a); }
    );

    M.Logging.logDebug(M.Base.serializeJSON(global.game_state));
    M.Logging.logDebug(global.game_state.page_1_bad1);

    if (global.game_state.page_1_bad1 !== null) {
      M.Logging.logDebug("yo");
      global.sliders.bad1.set(global.game_state.page_1_bad1);
      global.sliders.bad2.set(global.game_state.page_1_bad2);
      global.sliders.good.set(global.game_state.page_1_good);
    }

    global.sliders.bad1.draggable.options.onchange = recalc;
    global.sliders.bad2.draggable.options.onchange = recalc;
    global.sliders.good.draggable.options.onchange = recalc;
    var mystery_factor = 20; // where does this come from?
    global.bottom_of_game = M.DOM.elementDimensions(M.DOM.getElement('sky')).h  + M.DOM.elementPosition(M.DOM.getElement('sky')).y - mystery_factor;
    recalc();
  }

function save_state() {
    global.game_state.page_1_bad1 = global.sliders.bad1.get();
    global.game_state.page_1_bad2 = global.sliders.bad2.get();
    global.game_state.page_1_good = global.sliders.good.get();
    global.Intervention.saveState();
  }


M.DOM.addLoadEvent(init);


//this function snaps the graphics back into place on browser window resize
//from http://forums.port80.asn.au/archive/index.php/t-8475.html

function reloadme() { //or whatver else you have
    save_state();
    setTimeout(function () { window.location.reload(); }, 1); //
  }
window.onresize = reloadme;
