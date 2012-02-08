/*
games:{'ssnmtree':{
  '#firstfinished':false,
  '<div ID e.g. "bottom2-fruit">':{'name':'','disclosure':false,'support':false}
}}
*/
/*wrap code with module pattern*/
(function () {
    var global = this;
    var M = MochiKit;

    function SSNMTree() {
        this.game_state = null;
        this.edit_mode = 'view';/*view,support,disclosure,names*/
        this.game_edit_modemap = {
            'addnames': 'names',
            'editdisclosure': 'disclosure',
            'editsupport': 'support',
            'review': 'view'
          };
        this.__init__();
      }
    SSNMTree.prototype.__init__ = function () {
        this.intervention = global.Intervention;
        this.game_state = this.intervention.getGameVar('ssnmtree', {'#firstfinished': false});
        M.Signals.connect(window, 'onload', this, 'onLoad');
      };

    SSNMTree.prototype.onLoad = function () {
        var self = this;
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName(null, 'fruit', 'fruittree'), function (elt) {
            M.Signals.connect(elt, 'onclick', self, 'clickListener');
            var input = M.DOM.getFirstElementByTagAndClassName(input, null, elt);

            M.Signals.connect(input, 'onchange', self, 'namechangeListener');
            M.Signals.connect(input, 'onkeypress', self, 'namechangeListener');

            if (!hasAttr(self.game_state, elt.id)) {
              self.game_state[elt.id] = {'name': '', 'disclosure': false, 'support': false};
            }
            else {
              input.setAttribute('value', self.game_state[elt.id].name);
            }
          });
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName('input', 'editmode'), function (elt) {
            M.Signals.connect(elt, 'onchange', self, 'setEditMode');
          });

        M.Signals.connect('show-disclosure', 'onchange', self, 'showDisclosure');
        M.Signals.connect('show-support', 'onchange', self, 'showSupport');

        self.game_mode = M.DOM.getElement('game-mode').getAttribute('data-game-mode');
        self.setEditMode('view'); //default

        var first_finished = self.game_state['#firstfinished'];
        if (!first_finished) {

          self.setEditMode(self.game_edit_modemap[self.game_mode]);

          switch (self.game_mode) {
          case 'addnames':
            M.Style.hideElement('controls');
            break;
          case 'editdisclosure':
            M.Style.hideElement('support-controls', 'view-controls');
            self.showDisclosure();
            break;
          case 'editsupport':
            M.Style.hideElement('view-controls');
            self.showDisclosure();
            self.showSupport();
            break;
          case 'review':
            return; //skip last step!!!!
          }
          var complete_button = M.DOM.getElement('complete');
          if (complete_button) {
            M.Signals.connect(complete_button, 'onclick', self, 'firstComplete');
          }
        }
        $('next-game-part-link').onclick = function () {
            if (!self.anyNames()) {
              alert('Please enter at least one name.');
              return false;
            }
          };
      };
    SSNMTree.prototype.firstComplete = function (evt) {
        var self = this;
        self.game_state['#firstfinished'] = true;
        self.intervention.saveState();
      };
    SSNMTree.prototype.showDisclosure = function (evt) {
        var self = this;
        var show = (evt) ? evt.src().checked : true;
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName(null, 'fruit', 'fruittree'), function (elt) {
            var toggle_func = (show && self.game_state[elt.id].disclosure) ? M.DOM.addElementClass : M.DOM.removeElementClass;
            toggle_func(M.DOM.getFirstElementByTagAndClassName(null, 'ripe', elt), 'turned-on');
          });

        M.DOM.getElement('show-disclosure').checked = show;
        if (show) {
          M.Style.showElement('edit-disclosure');
        } else {
          M.Style.hideElement('edit-disclosure');
          if (M.DOM.getElement('edit-disclosure').checked) { self.setEditMode('view'); }
          M.DOM.getElement('edit-disclosure').checked = false;
        }
      };
    SSNMTree.prototype.showSupport = function (evt) {
        var self = this;
        var show = (evt) ? evt.src().checked : true;
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName(null, 'fruit', 'fruittree'), function (elt) {
            var toggle_func = (show && self.game_state[elt.id].support) ? M.DOM.addElementClass : M.DOM.removeElementClass;
            toggle_func(M.DOM.getFirstElementByTagAndClassName(null, 'circle', elt), 'turned-on');
          });
        M.DOM.getElement('show-support').checked = show;
        if (show) {
          M.Style.showElement('edit-support');
        } else {
          M.Style.hideElement('edit-support');
          if (M.DOM.getElement('edit-support').checked) { self.setEditMode('view'); }
          M.DOM.getElement('edit-support').checked = false;
        }
      };
    SSNMTree.prototype.setEditMode = function (mode_or_evt) {
        M.Logging.logDebug('setEditMode');
        var mode;
        if (typeof(mode_or_evt) === 'string') {
          mode = mode_or_evt;
        } else if (mode_or_evt.src().checked) {
          mode = mode_or_evt.src().value;
        } else {
          return;
        }
        this.edit_mode = mode;
        //disable/enable input boxes
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName('input', null, 'fruittree'), function (elt) {
            ///to make them read-only we make them buttons
            ///if we set disabled=true, then it drowns click events
            ///need to rewrite the value due to Firefox (SUX) weirdness
            var curvalue = elt.value;
            elt.type = (mode === 'names') ? 'text' : 'button';
            elt.value = curvalue;
          });
        M.DOM.getElement('edit-' + mode).checked = true;
      };

    SSNMTree.prototype.namechangeListener = function (evt) {
        M.Logging.logDebug('namechangeListener');
        var self = this;
        var input_elt = evt.src();
        var id = input_elt.parentNode.id;

        if (self.game_state[id].name !== input_elt.value) {
          self.game_state[id].name = input_elt.value;
          self.intervention.saveState();
        }
      };

    SSNMTree.prototype.anyNames = function () {
        for (var a in this.game_state) {
          if (typeof(this.game_state[a]) === 'object' && this.game_state[a].name) {
            return true;
          }
        }
        return false;
      };

    SSNMTree.prototype.clickListener = function (evt) {
        var self = this;
        var id = evt.src().id;
        var elt, turned_on;
        switch (self.edit_mode) {
        case 'view':
        case 'names':
          return; //DO nothing
        case 'support':
          elt = M.DOM.getFirstElementByTagAndClassName(null, 'circle', id);
          turned_on = self.game_state[id].support = !self.game_state[id].support;
          break;
        case 'disclosure':
          elt = M.DOM.getFirstElementByTagAndClassName(null, 'ripe', id);
          turned_on = self.game_state[id].disclosure = !self.game_state[id].disclosure;
          break;
        }
        self.intervention.saveState();
        if (turned_on) {
          M.DOM.addElementClass(elt, 'turned-on');
        } else {
          M.DOM.removeElementClass(elt, 'turned-on');
        }
      };

    if (!hasAttr(global, 'SSNMTree')) {
      global.SSNMTree = new SSNMTree();
    }

  })();
