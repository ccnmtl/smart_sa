var brand_groups = {};
var group_by = 'group';
var M = MochiKit;
var global = this;

//TODO: un-hardcode this:
var image_path = '../../site_media/pill_game/images/';

function set_selected(div) {
  if (M.DOM.getElement(div) !== null) {
    M.DOM.addElementClass(div, 'page_2_selected_pill');
  }
}

function toggle_select(pill_smart_id) {
  M.DOM.toggleElementClass('page_2_selected_pill', pill_smart_id);
}

function save_state() {
  global.pill_game.game_state.selected_meds = M.Base.map(itemgetter('id'), M.DOM.getElementsByTagAndClassName(null, 'page_2_selected_pill'));
  Intervention.saveState();
}

function pill_clicked(pill) {
  toggle_select(pill.smart_id);
  save_state();
}

function pill_image_div(pill) {
  var img = M.DOM.IMG({src: image_path + pill.image},  null);
  return M.DOM.DIV({'class': 'pill_image_div'}, img);
}

function pill_fact_div(fact, pill) {
  return M.DOM.DIV({'class': 'pill_fact_div'}, pill[fact]);
}

function pill_mg_fact_div(fact, pill) {
  return M.DOM.DIV({'class': 'pill_fact_div mg_fact'}, pill[fact]);
}

function pill__label_fact_div(fact, pill) {
  return M.DOM.DIV({'class': 'pill_fact_div'}, pill[fact]);
}

function draw_pill(group_div, pill) {
  var attrs = {
    id: pill.smart_id,
    'class': 'page_2_pill'
  };

  var new_pill_div = M.DOM.DIV(attrs, pill_image_div(pill), pill__label_fact_div('pill_label', pill), pill_mg_fact_div('dose_mg', pill));
  M.DOM.appendChildNodes(group_div, new_pill_div);
  M.Signals.connect(new_pill_div, 'onclick', M.Base.partial(pill_clicked, pill));
}

function draw_group(group) {
  var group_label = group[0];
  var pills = group[1];
  var attrs = {
    id: 'container_for' + group_label,
    'class': 'page_2_pill_group'
  };
  var group_div = M.DOM.DIV(attrs, M.DOM.DIV(null, group_label));
  M.Iter.forEach(pills, M.Base.partial(draw_pill, group_div));
  M.DOM.appendChildNodes(group_div, M.DOM.BR({'clear': 'all'}));
  M.DOM.appendChildNodes(M.DOM.getElement('game-content'), group_div);
}

function draw_medicine_types(line) {
  var my_line = M.Base.filter(function (m) { return m.line === line; }, global.arv_pill_types);
  my_line.sort(keyComparator(group_by));
  var group_list =  groupby_as_array(my_line, itemgetter(group_by));
  M.Iter.forEach(group_list, draw_group);
}

function init() {
  global.pill_game.game_state = Intervention.getGameVar('pill_game_state',  global.pill_game.default_state);
  if (global.pill_game.game_state.treatment_line === null) {
    alert("Please go back to the previous page and choose your line of medication.");
    return;
  }
  draw_medicine_types(global.pill_game.game_state.treatment_line);
  if (global.pill_game.game_state.selected_meds !== null) {
    M.Base.map(set_selected, global.pill_game.game_state.selected_meds);
  }
}

M.DOM.addLoadEvent(init);

