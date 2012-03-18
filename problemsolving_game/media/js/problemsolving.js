/* game_state['problemsolving'] = {
     'my_issues':{
         KEY-ISSUETEXT:{
            FIELDNAMES(from forms):"VALUE",
            FIELDNAMES(from forms):"VALUE",
         },
         KEY-ISSUETEXT:{},
     },
     'chosen-issue':"TEXT OF CHOSEN ISSUE"
   }
 */

(function () {
    var M = MochiKit;
    var global = this;
    var custom_elts = 0;
    function ProblemSolveGame() {
        this.game_state = null;
        this.__init__();
        this.field_phases = [];
    }

    ProblemSolveGame.prototype.__init__ = function () {
        this.intervention = global.Intervention;
        this.game_state = this.intervention.getGameVar('problemsolving', { 'my_issues': {} });
        M.Signal.connect(window, 'onload', this, 'onLoad');
    };
    ProblemSolveGame.prototype.onLoad = function () {
        var self = this;
        var mode = M.DOM.getElement('gamephase').className;

        var start_at_choose_one = false;
        //which ones picked
        for (var a in self.game_state.my_issues) {
            if (self.game_state.my_issues.hasOwnProperty(a)) {
                var issue = self.getIssueByText(a);
                if (issue) {
                    M.DOM.addElementClass(issue, 'picked');
                    if (mode === 'choose_one') {
                        start_at_choose_one = true;
                        var filled_out_form = false;
                        for (var b in self.game_state.my_issues[a]) {
                            if (self.game_state.my_issues[a].hasOwnProperty(b)) {
                                filled_out_form = true;
                                break;//not empty dict
                            }
                        }
                        if (filled_out_form) {
                            M.DOM.addElementClass(issue, 'completed');
                        } else {
                            M.DOM.removeElementClass(issue, 'completed');
                        }
                        M.Signal.connect(issue, 'onclick', M.Base.bind(self.chooseOneIssue, self, null, issue, filled_out_form));
                    }
                }
            }
        }
        if (start_at_choose_one) {
            self.game_state.default_page = 'choose_one';
            self.intervention.saveState();
        }

        if (mode === 'my_issues') {
            M.DOM.getElement('next-game-part-link').onclick = function () {
                if (!self.anyIssues()) {
                    alert('Please go back and select at least one issue');
                    return false;
                }
            };
        }
        if (mode === 'choose_one') {
            if (!window.hasAttr(self.game_state, 'chosen-issue')) {
                M.DOM.getElement('next-game-part-link').onclick = function () {
                    if (!self.game_state['chosen-issue']) {
                        alert('Please select an issue to problem solve.');
                        return false;
                    }
                };
            }
        }

        if (mode === 'problemsolve_one') {
            var workthrough_form = document.forms.workthrough_form;
            if (window.hasAttr(self.game_state, 'chosen-issue')) {
                var problemsolve_state = self.game_state.my_issues[self.game_state['chosen-issue']];
                for (var field in problemsolve_state) {
                    if (problemsolve_state.hasOwnProperty(field)) {
                        workthrough_form.elements[field].value = problemsolve_state[field];
                    }
                }
            }

            M.Signal.connect(workthrough_form, 'onchange', self, 'saveProblemSolveForm');

            self.resizeTextAreas();
            M.Iter.forEach(M.DOM.getElementsByTagAndClassName('textarea'), function (elt) {
                M.Signal.connect(elt, 'onchange', self, 'resizeTextAreas');
            });

            ///field phase framework
            var continue_link = M.DOM.getElement('form-continue');
            continue_link.setAttribute('onclick', 'return false;');//disable the href
            M.Signal.connect(continue_link, 'onclick', self, 'nextField');

            M.Iter.forEach(M.DOM.getElementsByTagAndClassName('div', 'problemsolve-field', workthrough_form),
                    function (elt) {
                self.field_phases.push(elt.id);
            });
            self.field_phases.push('gamephase');//final summary
            switch (location.hash) {
            case '':
            case '#gamephase':
                self.nextField();
            }
        }

        if (window.hasAttr(self.game_state, 'chosen-issue')) {
            var issue2 = self.getIssueByText(self.game_state['chosen-issue']);
            self.chooseOneIssue(null, issue2);
        }
    };
    ProblemSolveGame.prototype.previousIssue = function () {
        var cur_issue = M.DOM.getFirstElementByTagAndClassName(null, 'currentissue', 'issue-list');
        function getPreviousIssue(cur_issue) {
            var prev_issue = cur_issue.previousSibling;
            while (prev_issue !== null) {
                if (prev_issue.nodeType === 1) {
                    break;//we found the next issue
                }
                prev_issue = prev_issue.previousSibling;
            }
            return prev_issue;
        }
        var prev_issue = getPreviousIssue(cur_issue);
        if (prev_issue !== null) {
            M.DOM.removeElementClass(cur_issue, 'currentissue');
            M.DOM.addElementClass(prev_issue, 'currentissue');
            if (getPreviousIssue(prev_issue) === null) {
                M.DOM.hideElement('prev-issue-link');
            }
        } else {
            M.DOM.hideElement('prev-issue-link');
        }
        return false;
    };

    ProblemSolveGame.prototype.answerIssue = function (is_an_issue) {
        var self = this;
        var cur_issue = M.DOM.getFirstElementByTagAndClassName(null, 'currentissue', 'issue-list');

        var issue_text = self.getIssueText(cur_issue);
        if (is_an_issue && issue_text) {
            //if already there, leave it alone:
            if (!window.hasAttr(self.game_state.my_issues, issue_text)) {
                self.game_state.my_issues[issue_text] = {};
            }
        } else {
            delete self.game_state.my_issues[issue_text];
        }
        self.intervention.saveState();

        var next_issue = cur_issue.nextSibling;
        while (next_issue !== null) {
            if (next_issue.nodeType === 1) {
                break;//we found the next issue
            }
            next_issue = next_issue.nextSibling;
        }
        if (next_issue !== null) {
            M.DOM.removeElementClass(cur_issue, 'currentissue');
            M.DOM.addElementClass(next_issue, 'currentissue');
            M.DOM.showElement('prev-issue-link');
        } else {
            location.assign(M.DOM.getElement("next-game-part-link").href);
        }
    };

    ProblemSolveGame.prototype.getIssueByText = function (text) {
        var self = this;
        var issues = M.DOM.getElementsByTagAndClassName(null, 'issue', 'issue-list');
        var other = M.DOM.getFirstElementByTagAndClassName(null, 'editable-issue', 'issue-list');
        var rv = false;
        M.Iter.forEach(issues, function (elt) {
            if (self.getIssueText(elt) === text) {
                rv = elt;
            }
        });

        if (!rv) {
            ++custom_elts;
            if (custom_elts > 1) {
                other = other.cloneNode(true);
                M.DOM.appendChildNodes('issue-list', other);
            }
            var custom_elt = M.DOM.getFirstElementByTagAndClassName(null, 'issuetext', other);
            custom_elt.value = text;
            rv = other;
        }
        return rv;
    };
    ProblemSolveGame.prototype.anyIssues = function () {
        for (var a in this.game_state.my_issues) {
            if (this.game_state.my_issues.hasOwnProperty(a)) {
                return true;
            }
        }
        return false;
    };
    ProblemSolveGame.prototype.getIssueText = function (issue) {
        var text_dom = M.DOM.getFirstElementByTagAndClassName(null, 'issuetext', issue);
        var issue_text = (String(text_dom.tagName).toLowerCase() in {'input': 1, 'textarea': 1}) ? text_dom.value : text_dom.innerHTML;
        return issue_text;
    };
    ProblemSolveGame.prototype.nextField = function (evt) {
        var hash = String(global.location.hash).substr(1);
        var index = M.Base.findValue(this.field_phases, hash);
        var next = this.field_phases[index + 1];
        if (next) {
            global.location = '#' + next;
        }
        //new value
        hash = String(global.location.hash).substr(1);
        ///switch out video after we have these
        var video_href = M.DOM.getFirstElementByTagAndClassName('a', 'videolink', hash).href;

        M.DOM.getElement('video_src').setAttribute('value', video_href);
        M.DOM.getElement('video_embed').setAttribute('src', video_href);
        /*//explicit use of QT calls alternative
     video_embed.SetURL(video_href);
     video_embed.SetRectangle('0,0,320,196');
     video_embed.SetControllerVisible(true);
         */

        if (hash === 'gamephase') {
            M.DOM.addElementClass('gamephase', 'general');
        } else {
            M.DOM.removeElementClass('gamephase', 'general');
        }
        this.resizeTextAreas();
    };

    ProblemSolveGame.prototype.resizeTextAreas = function () {
        if (!M.DOM.hasElementClass('gamephase', 'general')) { return; }
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName('textarea'), function (src) {
            //var src = evt.src();
            var lines_array = String(src.value).match(/\n/g);
            if (lines_array) {
                src.rows = lines_array.length + 1;
            }
        });
    };
    ProblemSolveGame.prototype.saveProblemSolveForm = function (evt) {
        var self = this;
        var problemsolve_state = self.game_state.my_issues[self.game_state['chosen-issue']];

        M.Iter.forEach(document.forms.workthrough_form.elements, function (elt) {
            problemsolve_state[elt.name] = elt.value;
        });
        self.intervention.saveState();
    };
    ProblemSolveGame.prototype.chooseOneIssue = function (evt, issue, immediately_advance) {
        var self = this;
        issue = (issue) ? issue : evt.src();
        var cur_chosen = M.DOM.getFirstElementByTagAndClassName(null, 'chosen-issue', 'issue-list');
        if (cur_chosen) {
            M.DOM.removeElementClass(cur_chosen, 'chosen-issue');
        }

        M.DOM.addElementClass(issue, 'chosen-issue');
        var issue_text = self.getIssueText(issue);

        self.game_state['chosen-issue'] = issue_text;
        self.intervention.saveState();

        if (immediately_advance) {
            global.location = M.DOM.getElement('next-game-part-link').href + "#gamephase";
        }
    };

    global.ProblemSolveGame = new ProblemSolveGame();
}());

