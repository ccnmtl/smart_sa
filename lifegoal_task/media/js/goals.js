(function () {
  var global = this;
  var intervention = global.Intervention;
  var goal_state = intervention.getGameVar('lifegoals', {});

  var workform = null;

  function loadGoalTask() {
    workform = MochiKit.DOM.getElement('lifegoals');
    for (var a in goal_state) {
      if (hasAttr(workform.elements, a)) {
        workform.elements[a].value = goal_state[a];
      }
    }
    MochiKit.Signals.connect(workform, 'onchange', saveForm);
    MochiKit.Signals.connect(window, 'onunload', saveForm);
  }
  MochiKit.DOM.addLoadEvent(loadGoalTask);

  function saveForm() {
    MochiKit.Iter.forEach(workform.elements, function (elt) {
      goal_state[elt.name] = elt.value;
    });
    intervention.saveState();
  }
}());
