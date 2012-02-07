// how high  the guy is standing on the island
var guy_on_island_offset = 150;
var game_state;
var bottom_of_game;

var recalc = function () {
    //adjust water level:
    var water_level = (
        sliders.bad1.get() * sliders.bad1.influence +
        sliders.bad2.get() * sliders.bad2.influence) / 2;
    sliders.water.set(water_level);

    //adjust island level:
    var island_level = (sliders.good.get() * sliders.good.influence);
    sliders.island.set(island_level);
    var island_height = sliders.island.pos(sliders.island.get())[1];

    //pick an image for the dude:
    var dude_images = (Intervention.current_user.gender === "M") ? man_images : woman_images;
    var altitude = 0.5 + (sliders.island.getfraction() - sliders.water.getfraction()) / 2;
    $('dude').src = pick_image(altitude, dude_images);

    //adjust the dude
    setStyle('dude', {
        "left":  ($('dude').x) + 'px',
        "top" : (island_height - guy_on_island_offset) + 'px',
        'position': 'absolute',
        'height': '184px',
        'width': '110px'
      });

    clip_image($('island_moving'), 600, bottom_of_game);
    clip_image($('water_moving'), 600, bottom_of_game);
  };

function init() {
    game_state = Intervention.getGameVar('island_game_state', default_state);

    forEach(getElementsByTagAndClassName('span', 'slider'),
             function (a) { new Slider(a); }
    );

    logDebug(serializeJSON(game_state));
    logDebug(game_state.page_1_bad1);

    if (game_state.page_1_bad1 !== null) {
      logDebug("yo");
      sliders.bad1.set(game_state.page_1_bad1);
      sliders.bad2.set(game_state.page_1_bad2);
      sliders.good.set(game_state.page_1_good);
    }

    sliders.bad1.draggable.options.onchange = recalc;
    sliders.bad2.draggable.options.onchange = recalc;
    sliders.good.draggable.options.onchange = recalc;
    var mystery_factor = 20; // where does this come from?
    bottom_of_game = elementDimensions($('sky')).h  + elementPosition($('sky')).y - mystery_factor;
    recalc();
  }

function save_state() {
    game_state.page_1_bad1 = sliders.bad1.get();
    game_state.page_1_bad2 = sliders.bad2.get();
    game_state.page_1_good = sliders.good.get();
    Intervention.saveState();
  }


addLoadEvent(init);


//this function snaps the graphics back into place on browser window resize
//from http://forums.port80.asn.au/archive/index.php/t-8475.html

function reloadme() { //or whatver else you have
    save_state();
    setTimeout(function () { window.location.reload(); }, 1); //
  }
window.onresize = reloadme;
