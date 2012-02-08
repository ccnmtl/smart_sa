(function() {
    /* two special values: 'section' and 'total'
     * 'section' MUST NOT have any numbers in it
     * 'total' is the summary of all the values
     */

    var global = this;
    var intervention = global.Intervention;
    var goal_state = intervention.getGameVar('assessmentquiz', {});

    var workform = null;
    var section = '';

   var MD = MochiKit.DOM;
   var MS = MochiKit.Signal;
   var ML = MochiKit.Logging;
   var MI = MochiKit.Iter;

    function loadGoalTask() {
	workform = MD.getElement('assessmentquiz');
	section = workform.elements['section'].value;
	MS.connect(workform,'onchange',saveForm);
	MS.connect(window,'onunload',saveForm);

	if (hasAttr(goal_state,section)) {
	    for (a in goal_state[section]) {
		if (a === 'total') {
		    showTotal(goal_state[section][a]);
		    continue;
		}
		var form_elt = workform.elements[a];
		if (!form_elt) continue;

		if (hasAttr(form_elt,'type')) {
		    if (form_elt.type != 'checkbox') {
			workform.elements[a].checked = goal_state[section][a]==workform.elements[a].value;
		    } else {
			workform.elements[a].value = goal_state[section][a];
		    }
		} else {///radio -- TODO:might need to do the same for <select>
		    ML.logDebug(form_elt,a);
		    MI.forEach(form_elt, function(selection) {
			if (selection.value == goal_state[section][a]) {
			    selection.checked = true;
			}
		    });
		}
	    }
	}
    }
    MD.addLoadEvent(loadGoalTask);

    function saveForm() {
	if (!hasAttr(goal_state,section)) {
	    goal_state[section] = {};
	}
	var all_form_fields = {};
	var total = 0;
	MI.forEach(workform.elements,function(elt) {
	    if (elt.type != 'radio' || elt.checked) {
		goal_state[section][elt.name] = elt.value;
		all_form_fields[elt.name] = true;
                total += parseInt(elt.value,10)||0; //in case NaN
	    } else if (!hasAttr(all_form_fields,elt.name)) {
		all_form_fields[elt.name] = false;
	    }
	});
	var all_done = true;
	for (a in all_form_fields) {
	    all_done &= all_form_fields[a];
	}
	if (section == 'audit' && !all_done) {
	    var gs = goal_state[section];
	    all_done = ((gs['q1'] == 0
			 || 1*gs['q2'] + 1*gs['q3'] == 0
			) && hasAttr(gs,'q9') && hasAttr(gs,'q10')
			);
	    ML.logDebug(gs['q1'] == 0, 1*gs['q2'] + 1*gs['q3'] == 0, hasAttr(gs,'q9'), hasAttr(gs,'q10'));
	    ML.logDebug(all_done);
	}
	if (all_done) {
	    goal_state[section]['total'] = total;
	    showTotal(total);
	}
	intervention.saveState();
    }

    function showTotal(total) {
	ML.logDebug('showTotal',total);
	var ranges = list(MD.getElement('interpretation_range').getElementsByTagName('li'));
	var i = ranges.length;
	var found = false;
	while (--i >= 0) {
	    var range = parseInt(ranges[i].id.substr(1));
	    if (total >= range && !found) {
		found = true;
		MD.addElementClass(ranges[i],'inrange');
	    } else MD.removeElementClass(ranges[i],'inrange');
	}
    }

})();
