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
    function init() {

      game_state = Intervention.getGameVar('island_game_state', default_state);

      MI.forEach(MD.getElementsByTagAndClassName('span', 'slider'),
        function (a) { new Slider(a); }
      );

      if (game_state.page_2_good !== null) {
        sliders.good.set(game_state.page_2_good);
      }

      sliders.good.draggable.options.onchange = recalc;
      var mystery_factor = 20; // where does this come from?
      bottom_of_game = MD.elementDimensions(MD.getElement('sky')).h  + MD.elementPosition(MD.getElement('sky')).y - mystery_factor;
      recalc();
    }


    function save_state() {
      game_state.page_2_good = sliders.good.get();
      Intervention.saveState();
    }

    function recalc() {
      var health = sliders.good.get();
      sliders.water.set(10 - health);
      sliders.bad1.set(10 - health);
      sliders.bad2.set(10 - health);
      sliders.dude.set(health);
      sliders.good2.set(health);
      MD.setStyle('dude_moving', {
        'height': '184px',
        'width': '110px'
      });
      //pick an image for the dude:

      var dude_images = (Intervention.current_user.gender === "M") ? man_images : woman_images;
      MD.getElement('dude_moving').src = pick_image(sliders.dude.getfraction(), dude_images);

      clip_image(MD.getElement('water_moving'), 600, bottom_of_game);
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

  })();
