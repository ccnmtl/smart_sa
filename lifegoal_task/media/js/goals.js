(function() {
    var global = this;
    var intervention = global.Intervention;
    var goal_state = intervention.getGameVar('lifegoals', {});

    var workform = null;
    
    function loadGoalTask() {
	workform = $('lifegoals');
	for (a in goal_state) {
	    workform.elements[a].value = goal_state[a];
	}
	connect(workform,'onchange',saveForm);
	connect(window,'onunload',saveForm);
    }
    addLoadEvent(loadGoalTask);

    function saveForm() {
	forEach(workform.elements,function(elt) {
	    goal_state[elt.name] = elt.value
	});
	intervention.saveState();
    }

})();