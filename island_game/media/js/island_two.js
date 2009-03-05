/*
    BANNER SAYS: With ARV's.
    the island is a HILL.
    HILL DOES NOT MOVE.
    VL and OI control water height. // no longer : these just follow adherence slider.
    CD 4 contains position of dude.
    He moves on a diagonal up the hill.
    His icon does change according to his altitude.
    
*/


function init() {

    game_state = Intervention.getGameVar('island_game_state', default_state);

    forEach (getElementsByTagAndClassName('span', 'slider'),
        function (a) { new Slider (a) }
    );
    
    if (game_state.page_2_good != null) {
        sliders['good'].set( game_state.page_2_good);
    }
    
    /*
    sliders['bad1'].draggable.options.onchange = recalc ;
    sliders['bad2'].draggable.options.onchange = recalc ;
    sliders['good2'].draggable.options.onchange = recalc ;
    */
    sliders['good'].draggable.options.onchange = recalc ;
    mystery_factor = 20; // where does this come from?
    bottom_of_game = elementDimensions($('sky')).h  + elementPosition($('sky')).y - mystery_factor;
    recalc();
    
}


function save_state() {
    game_state.page_2_good = sliders['good'].get();
    Intervention.saveState();
}

function recalc() {
    health = sliders['good'].get()
    sliders['water'].set(10 - health);
    sliders['bad1'].set( 10 - health);
    sliders['bad2'].set( 10 - health);
    sliders['dude'].set(health);
    sliders['good2'].set( health);
    setStyle( 'dude_moving', {
        'height': '184px',
        'width': '110px'
    } );
    //pick an image for the dude:
    
    dude_images = (Intervention.current_user.gender == "M") ? man_images : woman_images;
    $('dude_moving').src = pick_image (sliders['dude'].getfraction(), dude_images);
    
    clip_image ($('water_moving'), 600, bottom_of_game);
}

addLoadEvent(init);

//this function snaps the graphics back into place on browser window resize
//from http://forums.port80.asn.au/archive/index.php/t-8475.html
window.onresize= reloadme;
// connect(window, 'onbeforeunload', reloadme);

function reloadme(){ //or whatver else you have
    save_state();
    setTimeout("window.location.reload()",1); //
}
