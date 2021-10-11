(function() {
    var global = this;
    var intervention = global.Intervention;
    var goal_state = null;
    var workform = null;

    function loadGoalTask() {
        goal_state = new global.GameState({
            game: 'lifegoals',
            el: 'div#defaulter'});

        workform = MochiKit.DOM.getElement('lifegoals');

        var keys = goal_state.getKeys();
        for (var i = 0; i < keys.length; i++) {
            if (window.hasAttr(workform.elements, keys[i])) {
                workform.elements[keys[i]].value = goal_state.getState(keys[i]);
            }
        }
        MochiKit.Signal.connect(workform, 'onchange', saveForm);
        MochiKit.Signal.connect(workform, 'onkeypress', saveForm);
        MochiKit.Signal.connect(workform, 'onkeyup', saveForm);
        MochiKit.Signal.connect(window, 'onunload', saveForm);
    }
    MochiKit.DOM.addLoadEvent(loadGoalTask);

    function saveForm() {
        MochiKit.Iter.forEach(workform.elements, function(elt) {
            goal_state.setState(elt.name, elt.value);
        });
        intervention.saveState();
    }
}());
