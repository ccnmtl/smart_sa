var game_state;

addLoadEvent(init);

function select_line(which) {
   line_to_select = (which == 1 ? 'select_line_1' : 'select_line_2');
   line_to_unselect =  (which == 1 ? 'select_line_2' : 'select_line_1');
   addElementClass(line_to_select, 'line_selected');
   removeElementClass(line_to_select, 'line_unselected');
   addElementClass(line_to_unselect, 'line_unselected');
   removeElementClass(line_to_unselect, 'line_selected');
   
   game_state['treatment_line'] = which;
   Intervention.saveState();
}

function init() {
    game_state = Intervention.getGameVar('pill_game_state',  default_state);
    if (game_state['treatment_line'] != null ) {
        select_line(game_state['treatment_line'])
    }
    connect ('select_line_1', 'onclick', partial (select_line, 1));
    connect ('select_line_2', 'onclick', partial (select_line, 2));
}


