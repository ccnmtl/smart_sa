var game_state;

var brand_groups = {};
var group_by = 'group';

//TODO: un-hardcode this:
var image_path = '../../site_media/pill_game/images/';

function set_selected(div) {
  if ($(div) !== null) {
    addElementClass(div, 'page_2_selected_pill');
  }
}

function toggle_select(pill_smart_id) {
  toggleElementClass('page_2_selected_pill', pill_smart_id);
}

function save_state() {
  game_state.selected_meds = map(itemgetter('id'), getElementsByTagAndClassName(null, 'page_2_selected_pill'));
  Intervention.saveState();
}

function pill_clicked(pill) {
  toggle_select(pill.smart_id);
  save_state();
}

function pill_image_div(pill) {
  img = IMG({src: image_path + pill.image},  null);
  return DIV({class: 'pill_image_div'}, img);
}

function pill_fact_div(fact, pill) {
  return DIV({class: 'pill_fact_div'}, pill[fact]);
}

function pill_mg_fact_div(fact, pill) {
  return DIV({class: 'pill_fact_div mg_fact'}, pill[fact]);
}

function pill__label_fact_div(fact, pill) {
  return DIV({class: 'pill_fact_div'}, pill[fact]);
}

function draw_pill(group_div, pill) {
  attrs = {
    id: pill.smart_id,
    'class': 'page_2_pill'
  };

  new_pill_div = DIV(attrs, pill_image_div(pill), pill__label_fact_div('pill_label', pill), pill_mg_fact_div('dose_mg', pill));
  appendChildNodes(group_div, new_pill_div);
  connect(new_pill_div, 'onclick', partial(pill_clicked, pill));
}

function draw_group(group) {
  group_label = group[0];
  pills = group[1];
  attrs = {
    id: 'container_for' + group_label,
    'class': 'page_2_pill_group'
  };
  var group_div = DIV(attrs, DIV(null, group_label));
  forEach(pills, partial(draw_pill, group_div));
  appendChildNodes(group_div, BR({'clear': 'all'}));
  appendChildNodes($('game-content'), group_div);
}

function draw_medicine_types(line) {
  my_line = filter(function (m) { return m.line === line; }, arv_pill_types);
  my_line.sort(keyComparator(group_by));
  group_list =  groupby_as_array(my_line, itemgetter(group_by));
  forEach(group_list, draw_group);
}

function init() {
  game_state = Intervention.getGameVar('pill_game_state',  default_state);
  if (game_state.treatment_line === null) {
    alert("Please go back to the previous page and choose your line of medication.");
    return;
  }
  draw_medicine_types(game_state.treatment_line);
  if (game_state.selected_meds !== null) {
    map(set_selected, game_state.selected_meds);
  }
}

addLoadEvent(init);

