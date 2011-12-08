/**************
InterventionSmart() sets itself to global object Intervention.
This will control the specific user object variables connected with
each activity/game, and the user's progress.

InterventionSmart DEPENDS ON MochiKit (more than Base?)
and EphemeralSession (e.g. local_session.js)

The user object will be organized as follows:
current_user = {
  ///used for client_login_confirm page
  'sessions_completed':1,

  ///session and activity keys are DB-related, not sequential
  ///no key/object exists until the client begins
  'sessions':
     {
        'session5':
           {
               'STATUS':'complete',
               'counselor_notes':'',
               'activity1':
                   {
                      ///NOTE:current ASSUMPTION: no other vars here
                      'STATUS':'complete'
                   }
           }
        'session7':
           {
               'STATUS':'inprogress',
               'counselor_notes':'',
               'activity3':
                   {
                      'STATUS':'complete'
                   }
               'activity6':
                   {
                      'STATUS':'inprogress'
                   }
           }
     },
  'games':
     {
        'game_var_blah':{'json':'objects are Okay',
                         //magic-but non-required field that can change
                         //the first page an activity starts on
                         //must equal one of the names that the task returns in pages()
                         //in the python model
                         'default_page':''
                        }
     }
  'timelog':
     {
       'DATE':[{'page':'foo.html','time':24}, //in seconds
               {'page':'grah.html','time':2000} //in seconds
              ]
     }
}
 */

/*wrap code with module pattern*/
(function() {
    var global = this;
    function InterventionSmart() {
	try {
	    this.session = global.EphemeralSession;
	    this.current_user = global.EphemeralSession.currentUser();
	    this.initTimeLog();
	    this.current_task = {};
	} catch(e) {/*never mind*/}
	  this.session_blueprint = function(){return {'STATUS':'inprogress',
						      'counselor_notes' : ''};}
	addLoadEvent(bind(this.onLoad,this));
    }
    InterventionSmart.prototype.onLoad = function() {
	this.showLoginInfo();
	if (location.protocol == 'file:') {
	    hideElement(getFirstElementByTagAndClassName(null,'loginlogout-remote'));
	    hideElement('home-remote');
	} else {
	    hideElement('home-desktop');
	}
    }

    InterventionSmart.prototype.showLoginInfo = function() {
	///Show login Info
	var displayed_user = getElement('username');
	var no_remote_user = (displayed_user && !/\w/.test(displayed_user.innerHTML));
	if (this.current_user && no_remote_user)
	{
	    displayed_user.innerHTML = this.current_user.firstname;
	    hideElement(getFirstElementByTagAndClassName(null,'loginlogout-remote'));
	    setDisplayForElement('inline',
				 getFirstElementByTagAndClassName(null,'loginlogout-local'));
	}
	if (this.current_user || !no_remote_user) {
	    setDisplayForElement('inline','logged-in-prefix');
	}
    }

    /*******************************************
     Login/logout
    *******************************************/
    InterventionSmart.prototype.login = function() {
	if (this.current_user) { this.logout(); }

	var form_vals = formContents('form_for_login')[1];
	//won't work if we reorder the fields

	//TEMPORARY FOR QA
	if (form_vals[0]=='admin' && form_vals[1]=='robertremien') {
	    this.jumpToAdmin();
	    return;
	}
	//DEMO USER
	if (form_vals[0]=='demo' && form_vals[1]=='demo') {
	    this.session.createUser('demo','demo',
				    {'firstname':'John',
				     'fullname':'John Smith',
				     'patientnumber':'demo',
				     'gender':'M'
				    });
	}
	this.session.login(form_vals[0],
			   form_vals[1],
			   bind(this.login_response,this));
	///NOTE: don't return anything here, since it seems
	///to break the form-submit
    }

    //callback for EphemeralSession.login()
    InterventionSmart.prototype.login_response = function(response) {
	var self = this;
	if (!response) {
	    alert('Login failed!');
	    return;
	}
	self.current_user = global.EphemeralSession.currentUser();
	if (hasAttr(self.current_user,'admin')
	    && self.current_user['admin']) {
	    logDebug('Admin Login');
	    self.jumpToAdmin();
	}
	else {
	    location = getElement('login_link').href;
	}
	/* we don't do the location explicitly, so
         * the static copy will still work (e.g. when '.html'
         * is appended.
         */
    }
    InterventionSmart.prototype.jumpToAdmin = function() {
	this.session.setAdmin(true);
	location = getElement('admin_link').href;
    }
    InterventionSmart.prototype.login_confirm = function() {
	if (hasAttr(this,'current_user')) {
	    for (key in this.current_user) {
		switch(key) {
		case 'firstname':
		    if (this.current_user['firstname']=='Test') {
			getElement('login').href = 'sessionNone_agenda';
		    }                //nobreak
		case 'fullname':     //nobreak
		case 'patientnumber':
		    getElement('user_'+key).innerHTML = this.current_user[key];
		    break;
		}
	    }
	    var session_count = 0;
	    if (typeof(this.current_user.sessions) == 'object') {
		for (a in this.current_user.sessions) {
		    if (hasAttr(this.current_user.sessions[a],'STATUS')
		       && this.current_user.sessions[a].STATUS =='complete') {
			++session_count;
		    }
		}
	    }
	    if (session_count) {
		getElement('user_sessions_completed').innerHTML = session_count;
		if (session_count==1) getElement('user_sessions_plural').innerHTML =''
	    }
	    else {
		getElement('user_has_completed').innerHTML = 'is just getting started!';
	    }
	}
    }
    InterventionSmart.prototype.logout = function() {
	this.logTime();
	this.session.logout();
	this.current_user = false;
    }
    /*******************************************
     Init Intervention/Session Pages
    *******************************************/
    InterventionSmart.prototype.init_intervention = function() {
	var self = this;
	if (!hasAttr(this.current_user, 'sessions')) {
	    this.current_user.sessions = {};
	    this.current_user.games = {};
	    this.session.saveUser(this.current_user);
	}
	self.init_subitems( function (session_id) {
	    return (hasAttr(self.current_user.sessions,session_id)
		    && self.current_user.sessions[session_id].STATUS == 'complete');
	});
    }

    InterventionSmart.prototype.init_session = function() {
	var self = this;
	if (!hasAttr(self.current_user,'sessions')) {
	    self.init_intervention();
	    //OK, since init_subitems() is run again for activities below
	}
	var user_sessions = self.current_user.sessions;
	var session_id = getFirstElementByTagAndClassName('h1','sessiontitle').id;
	if (!hasAttr(user_sessions, session_id)) {
	    user_sessions[session_id] = self.session_blueprint();
	    this.session.saveUser(this.current_user);
	}
	self.init_subitems( function(activity_id) {
	    return (hasAttr(self.current_user.sessions[session_id],activity_id)
		    && self.current_user.sessions[session_id][activity_id].STATUS == 'complete');
	});
    }

    InterventionSmart.prototype.current_activity = function() {
	var session_id = getFirstElementByTagAndClassName(null,'parentsession').id;
	var activity_id = getFirstElementByTagAndClassName(null,'activitytitle').id;
	if (!session_id || !activity_id) {
	    return false;
	}
	if (!hasAttr(this.current_user.sessions,session_id)) {
	    this.current_user.sessions[session_id] = this.session_blueprint();
	}
	if (!hasAttr(this.current_user.sessions[session_id],activity_id)) {
	    this.current_user.sessions[session_id][activity_id] = {};
	}
	return this.current_user.sessions[session_id][activity_id];

    }
    InterventionSmart.prototype.init_activity = function() {
	if (global.game_variables
	    && hasAttr(this.current_user.games,global.game_variables[0])
	    && hasAttr(this.current_user.games[global.game_variables[0]],'default_page'))
	{
	    var def_page = this.current_user.games[global.game_variables[0]].default_page;
	    var href = getElement('taskpage-'+def_page).href;
	    $('tasklink').href = href;
	}

    }

   InterventionSmart.prototype.init_notes = function() {
     	var notesTextArea = $('counselor-notes');
	if (notesTextArea) {
	  var session_id = getFirstElementByTagAndClassName(null,'parentsession').id;
	  var notes = this.current_user.sessions[session_id].counselor_notes;
	  notesTextArea.value = notes;
	}
   }

    InterventionSmart.prototype.init_subitems = function(subitem_complete) {
	var next_session = false; //will be DOM object
	forEach(
	    getElementsByTagAndClassName('a','subitem'),
	    function(elt) {
		var subitem_id = elt.id;
		var is_complete = subitem_complete(subitem_id);
		if (is_complete) {
		    addElementClass(elt,'session_complete');
		    removeElementClass(elt,'session_off');
		} else if (!next_session) {
		    next_session = elt;
		}
		return is_complete;
	    }
	);
	if (next_session) {
	    addElementClass(next_session,'session_next');
	    removeElementClass(next_session,'session_off');
	}
	return next_session;
    }

    /*******************************************
     Completion
    *******************************************/
    InterventionSmart.prototype.complete_session = function() {
	var session_id = getFirstElementByTagAndClassName('h1','sessiontitle').id;

	this.current_user.sessions[session_id].STATUS = 'complete';
	this.session.saveUser(this.current_user);
    }

    InterventionSmart.prototype.complete_activity = function(extra_data) {
	extra_data = (typeof(extra_data)=='object')?extra_data:{};
	extra_data['STATUS'] = 'complete';
	this.update_activity(extra_data);
    }

    InterventionSmart.prototype.update_activity = function(extra_data) {
	var activity_data = this.current_activity();
	if (activity_data && extra_data) {
	    update(activity_data,extra_data);
	    this.session.saveUser(this.current_user);
	}
    }

   InterventionSmart.prototype.saveCounselorNotes = function(notes) {
     var session_id = getFirstElementByTagAndClassName(null,'parentsession').id;
     this.current_user.sessions[session_id].counselor_notes = notes;
     this.session.saveUser(this.current_user);
   }

    /*******************************************
     Game Variables
    *******************************************/
    InterventionSmart.prototype.getGameVar = function(key,default_value) {
	if (typeof(default_value) != 'object') {
	    ///this way we can return the pointer, and the original updates
	    throw "devault_value required and must be an array or dictionary";
	}
	if (!hasAttr(this.current_user,'games')){this.current_user.games = {};}

	if (!hasAttr(this.current_user.games,key)) {
	    this.current_user.games[key] = default_value;
	}
	this.current_task[key] = default_value;
	return this.current_user.games[key];
    }
    InterventionSmart.prototype.resetGame = function() {
	for (key in this.current_task) {
	    this.current_user.games[key] = this.current_task[key];
	}
	this.saveState();
    }
    InterventionSmart.prototype.saveState = function() {
	this.session.saveUser(this.current_user);
    }

    /*******************************************
     Time Log
    *******************************************/
    InterventionSmart.prototype.initTimeLog = function() {
	var self = this;
	if (self.current_user) {
	    self.start_time = new Date();
	    connect(window,'onunload',self,'logTime');
	}
    }
    InterventionSmart.prototype.logTime = function() {
	if (!this.current_user) {return;} //logged out
	var now = new Date();
	var timespent = Math.round((now - this.start_time) / 1000);
	var date_string = [now.getFullYear(),now.getMonth()+1,now.getDate()].join('-');
	var file_name = location.pathname.split('/').pop().split('.html').shift()

	if (!hasAttr(this.current_user, 'timelog')) {
	    this.current_user['timelog'] = {};
	}
	if (!hasAttr(this.current_user.timelog, date_string)) {
	    this.current_user.timelog[date_string] = [];
	}
	this.current_user.timelog[date_string].push({'page':file_name,
						     'time':timespent
						    });
	this.saveState();
    }


    /**************
     INIT Global Instantiation
     **************/
    if (!hasAttr(global,'Intervention')) {
	global.Intervention = new InterventionSmart();
    }
})();
