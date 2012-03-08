(function () {
    var global = this;
    var M = MochiKit;

    function SSNMTree() {
        this.game_state = null;
        this.edit_mode = 'names';
        this.__init__();
    }
    
    SSNMTree.prototype.__init__ = function () {
        this.intervention = global.Intervention;
        this.game_state = this.intervention.getGameVar('ssnmtree', {});
        M.Signal.connect(window, 'onload', this, 'onLoad');
    };

    SSNMTree.prototype.onLoad = function () {
        var self = this;
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName('div', 'circle'), function (elt) {
            M.Signal.connect(elt, 'onclick', self, 'clickListener');
            
            var input = M.DOM.getFirstElementByTagAndClassName(input, null, elt.parentNode);

            M.Signal.connect(input, 'onchange', self, 'namechangeListener');
            M.Signal.connect(input, 'onkeypress', self, 'namechangeListener');
            M.Signal.connect(input, 'onkeyup', self, 'namechangeListener');

            if (!window.hasAttr(self.game_state, elt.parentNode.id)) {
                self.game_state[elt.parentNode.id] = {'name': ''};
            } else {
                input.setAttribute('value', self.game_state[elt.parentNode.id].name);
            }
        });

        self.showDisclosure();
        self.showSupport();
     
        var elt = M.DOM.getElement('complete');
        if (elt)
            M.Signal.connect(elt, 'onclick', self, 'saveState');
        
        elt = M.DOM.getElement('toggle-support-selection');
        if (elt)
            M.Signal.connect(elt, 'onclick', self, 'toggleSupportSelection');
        
        elt = M.DOM.getElement('toggle-disclosure-selection');
        if (elt)
            M.Signal.connect(elt, 'onclick', self, 'toggleDisclosureSelection');
    };
    
    SSNMTree.prototype.saveState = function (evt) {
        var self = this;
        
        if (!self.anyNames()) {
            evt.stop();
            alert('Please enter at least one name.');
            return false;
        } else {
            self.intervention.saveState();
            return true;
        }
    };
    
    SSNMTree.prototype.toggleSupportSelection = function() {
        var self = this;
        self.edit_mode = "support";
        
        var elt = M.DOM.getElement('toggle-support-selection');
        M.DOM.toggleElementClass("on", elt);
        M.DOM.toggleElementClass("off", elt);
        
        elt = M.DOM.getElement('toggle-disclosure-selection');
        M.DOM.removeElementClass(elt, "on");
        M.DOM.addElementClass(elt, "off");
    };
    
    SSNMTree.prototype.toggleDisclosureSelection = function() {
        var self = this;
        self.edit_mode = "disclosure";
        
        var elt = M.DOM.getElement('toggle-disclosure-selection');
        M.DOM.toggleElementClass("on", elt);
        M.DOM.toggleElementClass("off", elt);
        
        elt = M.DOM.getElement('toggle-support-selection');
        M.DOM.removeElementClass(elt, "on");
        M.DOM.addElementClass(elt, "off");
    };
    
    SSNMTree.prototype.showDisclosure = function (evt) {
        var self = this;
        var show = (evt) ? evt.src().checked : true;
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName('div', 'fruit', 'fruittree'), function (elt) {
            var toggle_func = (show && self.game_state[elt.id].disclosure) ? M.DOM.addElementClass : M.DOM.removeElementClass;
            toggle_func(M.DOM.getFirstElementByTagAndClassName(null, 'ripe', elt), 'turned-on');
        });
    };
    
    SSNMTree.prototype.showSupport = function (evt) {
        var self = this;
        var show = (evt) ? evt.src().checked : true;
        M.Iter.forEach(M.DOM.getElementsByTagAndClassName('div', 'fruit', 'fruittree'), function (elt) {
            var toggle_func = (show && self.game_state[elt.id].support) ? M.DOM.addElementClass : M.DOM.removeElementClass;
            toggle_func(M.DOM.getFirstElementByTagAndClassName('div', 'circle', elt), 'turned-on');
        });
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
          if (typeof(this.game_state[a]) === 'object' && this.game_state[a].name && this.game_state[a].name.length > 0) {
            return true;
          }
        }
        return false;
    };
      
    SSNMTree.prototype.clickListener = function (evt) {
        var self = this;
        var id = evt.src().parentNode.id;
        var elt, turned_on;
        
        switch (self.edit_mode) {
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

    if (!window.hasAttr(global, 'SSNMTree')) {
        global.SSNMTree = new SSNMTree();
    }

  }());
