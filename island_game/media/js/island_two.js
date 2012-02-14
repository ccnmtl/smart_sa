/*
    BANNER SAYS: With ARV's.
    the island is a HILL.
    HILL DOES NOT MOVE.
    VL and OI control water height. // no longer : these just follow adherence slider.
    CD 4 contains position of dude.
    He moves on a diagonal up the hill.
    His icon does change according to his altitude.

*/

(function () {
    var MI = MochiKit.Iter;
    var MD = MochiKit.DOM;
    var global = this;
    function init() {

      global.game_state = global.Intervention.getGameVar('island_game_state', global.default_state);

      MI.forEach(MD.getElementsByTagAndClassName('span', 'slider'),
        function (a) { new global.Slider(a); }
      );

      if (global.game_state.page_2_good !== null) {
        global.sliders.good.set(global.game_state.page_2_good);
      }

      global.sliders.good.draggable.options.onchange = recalc;
      var mystery_factor = 20; // where does this come from?
      global.bottom_of_game = MD.elementDimensions(MD.getElement('sky')).h  + MD.elementPosition(MD.getElement('sky')).y - mystery_factor;
      recalc();
    }


    function save_state() {
      global.game_state.page_2_good = global.sliders.good.get();
      global.Intervention.saveState();
    }

    function recalc() {
      var health = global.sliders.good.get();
      global.sliders.water.set(10 - health);
      global.sliders.bad1.set(10 - health);
      global.sliders.bad2.set(10 - health);
      global.sliders.dude.set(health);
      global.sliders.good2.set(health);
      MD.setStyle('dude_moving', {
        'height': '184px',
        'width': '110px'
      });
      //pick an image for the dude:

      var dude_images = (global.Intervention.current_user.gender === "M") ? global.man_images : global.woman_images;
      MD.getElement('dude_moving').src = global.pick_image(global.sliders.dude.getfraction(), dude_images);

      global.clip_image(MD.getElement('water_moving'), 600, global.bottom_of_game);
    }

    MD.addLoadEvent(init);

    //this function snaps the graphics back into place on browser window resize
    //from http://forums.port80.asn.au/archive/index.php/t-8475.html

    function reloadme() { //or whatver else you have
      save_state();
      setTimeout(function () { window.location.reload(); }, 1); //
    }

    window.onresize = reloadme;
    // connect(window, 'onbeforeunload', reloadme);

  }());
