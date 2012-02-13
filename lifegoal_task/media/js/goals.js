(function () {
  var global = this;
  var intervention = global.Intervention;
  var goal_state = intervention.getGameVar('lifegoals', {});

  var workform = null;

  function loadGoalTask() {
    workform = MochiKit.DOM.getElement('lifegoals');
    for (var a in goal_state) {
      if (window.hasAttr(workform.elements, a)) {
        workform.elements[a].value = goal_state[a];
      }
    }
    MochiKit.Signal.connect(workform, 'onchange', saveForm);
    MochiKit.Signal.connect(window, 'onunload', saveForm);
  }
  MochiKit.DOM.addLoadEvent(loadGoalTask);

  function saveForm() {
    MochiKit.Iter.forEach(workform.elements, function (elt) {
      goal_state[elt.name] = elt.value;
    });
    intervention.saveState();
  }
}());
