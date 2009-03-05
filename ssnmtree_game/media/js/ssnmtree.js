/*wrap code with module pattern*/
(function() {
    var global = this;

    function SSNMTree() {
	this.game_state = null;
	this.edit_mode = 'view';/*view,support,disclosure,names*/
	this.game_edit_modemap = {
	    'addnames':'names',
	    'editdisclosure':'disclosure',
	    'editsupport':'support',
	    'review':'view'
	}
	this.__init__();
    }
    SSNMTree.prototype.__init__ = function() {
	this.intervention = global.Intervention;
	this.game_state = this.intervention.getGameVar('ssnmtree',{'#firstfinished':false});
	connect(window,'onload',this,'onLoad');
    }

    SSNMTree.prototype.onLoad = function() {
	var self = this;
	forEach(getElementsByTagAndClassName(null,'fruit','fruittree'), function(elt) {
	    connect(elt,'onclick',self,'clickListener');
	    var input = getFirstElementByTagAndClassName(input,null,elt);

	    connect(input,'onchange',self,'namechangeListener');
	    connect(input,'onkeypress',self,'namechangeListener');

	    if (!hasAttr(self.game_state,elt.id)) {
		self.game_state[elt.id] = {'name':'','disclosure':false,'support':false};
	    }
	    else {
		input.setAttribute('value',self.game_state[elt.id].name);
	    }
	});
	forEach(getElementsByTagAndClassName('input','editmode'),function(elt) {
	    connect(elt,'onchange',self,'setEditMode');
	});

	connect('show-disclosure','onchange',self,'showDisclosure');
	connect('show-support','onchange',self,'showSupport');

	self.game_mode = getElement('game-mode').getAttribute('data-game-mode');
	self.setEditMode('view'); //default

	var first_finished = self.game_state['#firstfinished'];
	if (!first_finished) {

	    self.setEditMode(self.game_edit_modemap[self.game_mode]);

	    switch(self.game_mode) {
	    case 'addnames':
		hideElement('controls');
		break;
	    case 'editdisclosure':
		hideElement('support-controls','view-controls');
		self.showDisclosure();
		break;
	    case 'editsupport':
		hideElement('view-controls');
		self.showDisclosure();
		self.showSupport();
		break;
	    case 'review':
		return; //skip last step!!!!
	    }
	    var complete_button = getElement('complete');
	    if (complete_button) {
		connect(complete_button,'onclick',self,'firstComplete')
	    }
	}

    }
    SSNMTree.prototype.firstComplete = function(evt) {
	var self = this;
	self.game_state['#firstfinished'] = true;
	self.intervention.saveState();	
    }
    SSNMTree.prototype.showDisclosure = function(evt) {
	var self = this;
	var show = (evt)?evt.src().checked:true;
	forEach(getElementsByTagAndClassName(null,'fruit','fruittree'), function(elt) {
	    var toggle_func = (show&&self.game_state[elt.id].disclosure)?addElementClass:removeElementClass;
	    toggle_func(getFirstElementByTagAndClassName(null,'ripe',elt),'turned-on');
	});
	
	getElement('show-disclosure').checked=show;
	if (show) 
	    showElement('edit-disclosure');
	else {
	    hideElement('edit-disclosure');
	    if (getElement('edit-disclosure').checked) self.setEditMode('view');
	    getElement('edit-disclosure').checked = false;
	}
    }
    SSNMTree.prototype.showSupport = function(evt) {
	var self = this
	var show = (evt)?evt.src().checked:true;
	forEach(getElementsByTagAndClassName(null,'fruit','fruittree'), function(elt) {
	    var toggle_func = (show&&self.game_state[elt.id].support)?addElementClass:removeElementClass;
	    toggle_func(getFirstElementByTagAndClassName(null,'circle',elt),'turned-on');
	});
	getElement('show-support').checked=show;
	if (show) 
	    showElement('edit-support');
	else {
	    hideElement('edit-support');
	    if (getElement('edit-support').checked) self.setEditMode('view');
	    getElement('edit-support').checked = false;
	}
    }
    SSNMTree.prototype.setEditMode = function(mode_or_evt) {
	var mode;
	if (typeof(mode_or_evt)=='string') {
	    mode = mode_or_evt;
	} else if (mode_or_evt.src().checked) {
	    mode = mode_or_evt.src().value;
	} else {
	    return;
	}
	this.edit_mode = mode;
	//disable/enable input boxes
	forEach(getElementsByTagAndClassName('input',null,'fruittree'), function(elt) {
	    ///to make them read-only we make them buttons
	    ///if we set disabled=true, then it drowns click events
	    elt.type = (mode=='names')?'text':'button';
	});
	getElement('edit-'+mode).checked = true;
    }

    SSNMTree.prototype.namechangeListener = function(evt) {
	var self = this;
	var input_elt = evt.src();
	var id = input_elt.parentNode.id;

	if (self.game_state[id].name != input_elt.value) {
	    self.game_state[id].name = input_elt.value
	    self.intervention.saveState();
	}
    }

    SSNMTree.prototype.clickListener = function(evt) {
	var self = this;
	var id = evt.src().id;
	var elt, turned_on;
	switch(self.edit_mode) {
	case 'view':
	case 'names':
	    return; //DO nothing
	case 'support':
	    elt = getFirstElementByTagAndClassName(null,'circle',id);
	    turned_on = self.game_state[id].support = !self.game_state[id].support;
	    break;
	case 'disclosure':
	    elt = getFirstElementByTagAndClassName(null,'ripe',id);
	    turned_on = self.game_state[id].disclosure = !self.game_state[id].disclosure;
	    break;
	}
	self.intervention.saveState();
	(turned_on) ? addElementClass(elt,'turned-on') : removeElementClass(elt,'turned-on');
    }

    if (!hasAttr(global,'SSNMTree')) {
	global.SSNMTree = new SSNMTree();
    }

})();