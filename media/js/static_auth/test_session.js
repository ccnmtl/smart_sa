/*************************
 *  TestSession available externally as 'EphemeralSession'
 * Does not save state across sessions (no memory)
 * Intended for testing purposes
 *
 * Depends on MochiKit/Base.js (for JSON)
 */


function hasAttr(obj,key) {
    try {
	return (typeof(obj[key]) != 'undefined');
    } catch(e) {return false;}
}

/*wrap code with module pattern*/
(function() {
    var global = this;
    var M = MochiKit.Base;

    function TestSession() {
	this.permStor = global.globalStorage[location.hostname];
	this.sessStor = global.sessionStorage;
	this.nsUSER = 'USER_';
	this.nsBACKUP = 'BACKUP_';
	this.RESTORE_KEY = 'RESTORE';
	if (!hasAttr(this.sessStor,this.nsUSER)) {
	    this.sessStor[this.nsUSER] = '{}';
	}
    }
    TestSession.prototype.currentUser=function() {
	if (hasAttr(this.sessStor,this.nsUSER)) {
	    return M.evalJSON(this.sessStor[this.nsUSER].value);
	} else {
	    this.sessStor[this.nsUSER] = '{}';
	    return {};
	}
    }
    TestSession.prototype.saveUser=function(user_info,/*optional:*/ callback, user_key) {
	this.sessStor[this.nsUSER] = M.serializeJSON(user_info);
	if (callback) {
	    var response = callback(user_info);
	}
    }
    
    /*
       DOESN"T WORK YET!
 
    TestSession.prototype.login=function(username, credential, callback) {
	var self = this;
	var user_key = self.nsUSER + self.hash(username,credential);
	self.setAdmin(false);

	if (!hasAttr(self.permStor,user_key)) {
	    //LOGIN FAILED
	    logDebug('login failed', user_key);
	    if (typeof(callback) == 'function') callback(false);
	}
	else {
	    self.sessStor.user = user_key;
	    var user = self.currentUser();
	    if (typeof(callback) == 'function') callback(user);
	}
	return; //if you want something, use @arg callback
    }
    TestSession.prototype.logout=function(callback) {
	delete this.sessStor.user;
	delete this.sessStor.admin;
    }
    TestSession.prototype.isAdmin=function() {
	return (hasAttr(this.sessStor,'admin') &&this.sessStor['admin'].value);
    }
    TestSession.prototype.setAdmin=function(is_admin) {
	this.sessStor['admin'] = (is_admin)?'true':'';
    }
    TestSession.prototype.createUser=function(username, credential, more_info) {
	var self = this;
	var user_hash = this.hash(username, credential);
	var user_info = {};
	if (arguments.length > 2) {
	    update(user_info,more_info)
	}
	var user_key = this.nsUSER+user_hash;
	///only save if they don't already exist
	if (!hasAttr(this.permStor,user_key)) {
	    this.saveUser(user_info,false,user_key);
	}
	return user_key;
    }
    TestSession.prototype.destroyEverything=function() {
	var self = this;
	if (confirm('This will delete all data relating to clients and your own admin account.  Are you sure?')) {
	    for (a in self.sessStor) {
		delete self.sessStor[a];
	    }
	    for (a in self.permStor) {
		if (!RegExp('^'+self.nsBACKUP).test(a)) {
		    delete self.permStor[a];
		}
	    }
	}
    }
    */
    if (!hasAttr(global,'EphemeralSession')) {
	if (hasAttr(global,'sessionStorage')
	    && hasAttr(global,'globalStorage')) 
        {
	    if (location.hostname != '') {
		global.EphemeralSession = new TestSession();
		//for easy debug access
		global.e = global.EphemeralSession;
	    } else {
		throw "We need a hostname, if on local file system, then go to the same url, but start it with file://localhost/ instead of file:/// after restarting the browser.";
	    }
	}
        else {
	    throw "No Firefox, and no support for other browsers (yet)!";
	}
    }
})();