var game_state;

function clear_pill_info() {
  MochiKit.Logging.logDebug("CLEARING");
  // erase all pill info every time a client switches lines -- otherwise stuff gets confusing.
  game_state.selected_meds  = [];
  delete game_state.night_pills;
  delete game_state.day_pills;
  delete game_state.day_pills_time_menu_selected_index;
  delete game_state.night_pills_time_menu_selected_index;
}


function select_line(new_line) {
  if (game_state.treatment_line  !== new_line) {
    //logDebug ("Changing.");
    clear_pill_info();
  }
  var line_to_select = (new_line === 1 ? 'select_line_1' : 'select_line_2');
  var line_to_unselect = (new_line === 1 ? 'select_line_2' : 'select_line_1');
  MochiKit.DOM.addElementClass(line_to_select, 'line_selected');
  MochiKit.DOM.removeElementClass(line_to_select, 'line_unselected');
  MochiKit.DOM.addElementClass(line_to_unselect, 'line_unselected');
  MochiKit.DOM.removeElementClass(line_to_unselect, 'line_selected');
  game_state.treatment_line = new_line;
  Intervention.saveState();
}

function init() {
  game_state = Intervention.getGameVar('pill_game_state',  default_state);
  if (game_state.treatment_line !== "") {
    select_line(game_state.treatment_line);
  }
  MochiKit.Signals.connect('select_line_1', 'onclick', MochiKit.Base.partial(select_line, 1));
  MochiKit.Signals.connect('select_line_2', 'onclick', MochiKit.Base.partial(select_line, 2));
}


MochiKit.DOM.addLoadEvent(init);
