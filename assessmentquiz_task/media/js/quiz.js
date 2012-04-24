(function () {
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
    var MB = MochiKit.Base;

    function loadGoalTask() {
        workform = MD.getElement('assessmentquiz');
        MS.connect(workform, 'onchange', enableRevealScore);
        MS.connect('reveal_score', 'onclick', revealScore);
        MS.connect(window, 'onunload', saveForm);
        
        section = workform.elements.section.value;
        

        if (window.hasAttr(goal_state, section)) {
            for (var a in goal_state[section]) {
                if (goal_state[section].hasOwnProperty(a)) {
                    if (a === 'total') {
                        showTotal(goal_state[section][a]);
                        continue;
                    }
                    var form_elt = workform.elements[a];
                    if (!form_elt) {
                        continue;
                    }

                    if (window.hasAttr(form_elt, 'type')) {
                        if (form_elt.type !== 'checkbox') {
                            workform.elements[a].checked = goal_state[section][a] === workform.elements[a].value;
                        } else {
                            workform.elements[a].value = goal_state[section][a];
                        }
                    } else {///radio -- TODO:might need to do the same for <select>
                        ML.logDebug(form_elt, a);
                        MI.forEach(form_elt, function (selection) {
                            if (selection.value === goal_state[section][a]) {
                                selection.checked = true;
                            }
                        });
                    }
                }
            }
        }
    }
    MD.addLoadEvent(loadGoalTask);
    
    function enableRevealScore() {
        if (saveForm()) {
            MD.removeElementClass("reveal_score", "inactive");
        } else {
            MD.addElementClass("reveal_score", "inactive");
            document.getElementById("interpretation").style.display = "none";
        }
    }
    
    function revealScore() {
        if (MD.hasElementClass("reveal_score", "inactive")) {
            alert("Please answer all the questions before checking your score");
            return false;
        } else {
            showTotal();
            return true;
        }
    }

    function saveForm() {
        if (!window.hasAttr(goal_state, section)) {
            goal_state[section] = {};
        }
        var all_form_fields = {};
        var total = 0;
        MI.forEach(workform.elements, function (elt) {
            if (elt.type !== 'radio' || elt.checked) {
                goal_state[section][elt.name] = elt.value;
                all_form_fields[elt.name] = true;
                total += parseInt(elt.value, 10) || 0; //in case NaN
            } else if (!window.hasAttr(all_form_fields, elt.name)) {
                all_form_fields[elt.name] = false;
            }
        });
        var all_done = true;
        for (var a in all_form_fields) {
            if (all_form_fields.hasOwnProperty(a)) {
                all_done &= all_form_fields[a];
            }
        }
        
        var gs = goal_state[section];
        if (section === 'audit' && !all_done) {
            all_done = ((gs.q1 === "0" || 1 * gs.q2 + 1 * gs.q3 === 0) && window.hasAttr(gs, 'q9') && window.hasAttr(gs, 'q10'));
        }
        if (all_done) {
            if (section === 'drugaudit') {
                // Respondent screens positive if response to question 1 or 2 ³ 3,
                // or response to question 3 or 4 ³ 1.
                // Question 5 is not scored.
                goal_state[section].total = (gs.q1 >= 3 || gs.q2 >= 3 || gs.q3 >= 1 || gs.q4 >= 1) ? 1 : 0;
            } else {
                goal_state[section].total = total;
            }
        }

        intervention.saveState();
        
        return all_done;
    }

    function showTotal() {
        document.getElementById("interpretation").style.display = "block";
        MD.removeElementClass("reveal_score", "inactive");

        var total = goal_state[section].total;
        ML.logDebug('showTotal', total);
        var ranges = MI.list(MD.getElement('interpretation_range').getElementsByTagName('li'));
        var i = ranges.length;
        var found = false;
        while (--i >= 0) {
            var range = parseInt(ranges[i].id.substr(1), 10);
            if (!isNaN(range)) {
                if (total >= range && !found) {
                    found = true;
                    MD.addElementClass(ranges[i], 'inrange');
                    MD.removeElementClass(ranges[i], 'outofrange');
                } else {
                    MD.removeElementClass(ranges[i], 'inrange');
                    MD.addElementClass(ranges[i], 'outofrange');
                }
            }
        }
    }

}());
