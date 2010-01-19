/*************************
 * Depends on MochiKit/Base.js (for JSON)
 *
 *
 */


function hasAttr(obj,key) {
    try {
	return (typeof(obj[key]) != 'undefined');
    } catch(e) {return false;}
}

function NOT(bool) {
    return !bool;
}

/*wrap code with module pattern*/
(function() {
    var global = this;
    var M = MochiKit.Base;

    function GearsWrapper(stor) {
	var db = google.gears.factory.create('beta.database');
	db.open('database-smart');
	db.execute('create table if not exists Smart (Key text, Value text)');
	


    }

    function StorageWrapper(stor) {

	this.KEYS_KEY = 'KEYS';
	this.hasKey = function(key) {
	    return (stor.getItem(key) != null);
	}
	this.get = function(key,default_val) {
	    return (this.hasKey(key) ? stor.getItem(key) : default_val);
	}
	var key_dict = M.evalJSON(this.get(this.KEYS_KEY,'{}'));
	this.set = function(key,value) {
	    stor.setItem(key,value);
	    key_dict[key]=1;
	    stor.setItem(this.KEYS_KEY,M.serializeJSON(key_dict));
	}

	///actually returns a dict in the form {key1:1,key2:1,...}
	this.keyDict = function() {
	    return M.clone(key_dict);
	}
	this.del = function(key) {
	    delete stor[key];
	    delete key_dict[key];
	    stor.setItem(this.KEYS_KEY,M.serializeJSON(key_dict));
	}
    }

    function LocalFirefoxSession() {
	this.permStor = new StorageWrapper(hasAttr(global,'localStorage')?global.localStorage:global.globalStorage[location.hostname]);
	this.sessStor = new StorageWrapper(global.sessionStorage);
	this.nsUSER = 'USER_';
	this.nsBACKUP = 'BACKUP_';
	this.RESTORE_KEY = 'RESTORE';
    }
    /* @return
    */
    LocalFirefoxSession.prototype.login=function(username, credential, callback) {
	var self = this;
	var user_key = self.nsUSER + self.hash(username,credential);
	self.setAdmin(false);
	if (NOT(self.permStor.hasKey(user_key))) {
	    //LOGIN FAILED
	    logDebug('login failed', user_key);
	    if (typeof(callback) == 'function') callback(false);
	}
	else {
	    self.sessStor.set('user',user_key);
	    var user = self.currentUser();
	    if (typeof(callback) == 'function') callback(user);
	}
	return; //if you want something, use @arg callback
    }
    LocalFirefoxSession.prototype.logout=function(callback) {
	this.sessStor.del('user');
	this.sessStor.del('admin');
    }
    LocalFirefoxSession.prototype.isAdmin=function() {
	var is_admin = this.sessStor.get('admin');
	return (is_admin == 'true');
    }
    LocalFirefoxSession.prototype.setAdmin=function(is_admin) {
	this.sessStor.set('admin', (is_admin?'true':'') );
    }
    LocalFirefoxSession.prototype.hash=function() {
	var my_hash = 'HASH';
	for (var i=0; i < arguments.length; i++) {
	    my_hash += '__'+String(arguments[i]).toLowerCase();
	}
	return sha1Hash(my_hash);
    }
    LocalFirefoxSession.prototype.getUserData=function(user_key) {
	return M.evalJSON(this.permStor.get(user_key,'false'));
    }
    LocalFirefoxSession.prototype.userList=function() {
	var userkeys = {};
	for (a in this.permStor.keyDict()) {
	    if (RegExp('^'+this.nsUSER).test(a)) {
		userkeys[a]=1;
	    }
	}
	return userkeys;
    }
    LocalFirefoxSession.prototype.currentUserKey=function() {
	return this.sessStor.get('user',false);
    }
    LocalFirefoxSession.prototype.currentUser=function() {
	var userkey = this.currentUserKey();
	return this.getUserData(userkey);
    }	    
    LocalFirefoxSession.prototype.createUser=function(username, credential, more_info) {
	var self = this;
	var user_hash = this.hash(username, credential);
	var user_info = {};
	if (arguments.length > 2) {
	    update(user_info,more_info)
	}
	var user_key = this.nsUSER+user_hash;
	///only save if they don't already exist
	if (NOT(this.permStor.hasKey(user_key))) {
	    this.saveUser(user_info,false,user_key);
	}
	return user_key;
    }

    /*defaults to save user_info to current user*/
    LocalFirefoxSession.prototype.saveUser=function(user_info,/*optional:*/ callback, user_key) {
	var which_user = (user_key) ? user_key : this.currentUserKey();
	if (which_user) {
	    this.permStor.set(which_user, M.serializeJSON(user_info));
	}
	if (callback) {
	    var response = (which_user) ?  callback(user_info) : callback(false);
	}
    }
    //backup stuff
    LocalFirefoxSession.prototype.restoreKey=function(set_val) {
	return (set_val ? set_val : this.permStor.get(this.RESTORE_KEY,false));
    }

    LocalFirefoxSession.prototype.backupList=function() {
	var backupkeys = {};
	for (a in this.permStor.keyDict()) {
	    if (RegExp('^'+this.nsBACKUP).test(a)) {
		backupkeys[a]=1;
	    }
	}
	return backupkeys;
    }
    LocalFirefoxSession.prototype.backupObject=function() {
	var keystobackup = {};
	for (a in this.permStor.keyDict()) {
	    if (RegExp('^'+this.nsUSER).test(a)) {
		keystobackup[a]=this.permStor.get(a);
	    }
	}
	return keystobackup;
    }
    LocalFirefoxSession.prototype.backup=function(backupkey,backupJSONstring) {
	this.permStor.set(this.nsBACKUP+backupkey,backupJSONstring);
    }
    LocalFirefoxSession.prototype.getBackupString=function(backupkey) {
	return this.permStor.get(backupkey);
    }

    LocalFirefoxSession.prototype.restore=function(blob) {
	for (a in blob) {
	    this.permStor.set(a,blob[a]);
	}
    }

    LocalFirefoxSession.prototype.destroyAllUsers=function() {
	for (a in this.userList()) {
	    this.permStor.del(a);
	}
    }
    LocalFirefoxSession.prototype.destroyEverything=function() {
	var self = this;
	if (confirm('This will delete all data relating to clients and your own admin account.  Are you sure?')) {
	    for (a in self.sessStor.keyDict()) {
		self.sessStor.del(a);
	    }
	    for (a in self.permStor.keyDict()) {
		if ( NOT( RegExp('^'+self.nsBACKUP).test(a))) {
		    self.permStor.del(a);
		}
	    }
	}
    }

    if ( NOT( hasAttr(global,'EphemeralSession'))) {
	if (hasAttr(global,'sessionStorage')
	    && (hasAttr(global,'localStorage')
		|| hasAttr(global,'globalStorage'))
	   )
        {
	    if (location.hostname != '') {
		global.EphemeralSession = new LocalFirefoxSession();
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



    /*
      The sourcecode below is (c) 2002-2005 Chris Veness
      see http://www.movable-type.co.uk/scripts/sha1.html
      released under the LGPL: http://www.fsf.org/licensing/licenses/lgpl.html
      without any warranty express or implied
     */
    function sha1Hash(msg)
    {
	// constants [§4.2.1]
	var K = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6];
	

	// PREPROCESSING 
 
	msg += String.fromCharCode(0x80); // add trailing '1' bit to string [§5.1.1]
	
	// convert string msg into 512-bit/16-integer blocks arrays of ints [§5.2.1]
	var l = Math.ceil(msg.length/4) + 2;  // long enough to contain msg plus 2-word length
	var N = Math.ceil(l/16);              // in N 16-int blocks
	var M = new Array(N);
	for (var i=0; i<N; i++) {
            M[i] = new Array(16);
            for (var j=0; j<16; j++) {  // encode 4 chars per integer, big-endian encoding
		M[i][j] = (msg.charCodeAt(i*64+j*4)<<24) | (msg.charCodeAt(i*64+j*4+1)<<16) | 
                    (msg.charCodeAt(i*64+j*4+2)<<8) | (msg.charCodeAt(i*64+j*4+3));
            }
	}
	// add length (in bits) into final pair of 32-bit integers (big-endian) [5.1.1]
	// note: most significant word would be ((len-1)*8 >>> 32, but since JS converts
	// bitwise-op args to 32 bits, we need to simulate this by arithmetic operators
	M[N-1][14] = ((msg.length-1)*8) / Math.pow(2, 32); M[N-1][14] = Math.floor(M[N-1][14])
	M[N-1][15] = ((msg.length-1)*8) & 0xffffffff;
	
	// set initial hash value [§5.3.1]
	var H0 = 0x67452301;
	var H1 = 0xefcdab89;
	var H2 = 0x98badcfe;
	var H3 = 0x10325476;
	var H4 = 0xc3d2e1f0;

	// HASH COMPUTATION [§6.1.2]
	
	var W = new Array(80); var a, b, c, d, e;
	for (var i=0; i<N; i++) {
	    
            // 1 - prepare message schedule 'W'
            for (var t=0;  t<16; t++) W[t] = M[i][t];
            for (var t=16; t<80; t++) W[t] = ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16], 1);
	    
            // 2 - initialise five working variables a, b, c, d, e with previous hash value
            a = H0; b = H1; c = H2; d = H3; e = H4;
	    
            // 3 - main loop
            for (var t=0; t<80; t++) {
		var s = Math.floor(t/20); // seq for blocks of 'f' functions and 'K' constants
		var T = (ROTL(a,5) + f(s,b,c,d) + e + K[s] + W[t]) & 0xffffffff;
		e = d;
		d = c;
		c = ROTL(b, 30);
		b = a;
		a = T;
            }

            // 4 - compute the new intermediate hash value
            H0 = (H0+a) & 0xffffffff;  // note 'addition modulo 2^32'
            H1 = (H1+b) & 0xffffffff; 
            H2 = (H2+c) & 0xffffffff; 
            H3 = (H3+d) & 0xffffffff; 
            H4 = (H4+e) & 0xffffffff;
	}
	
	return H0.toHexStr() + H1.toHexStr() + H2.toHexStr() + H3.toHexStr() + H4.toHexStr();
    }

    //
    // function 'f' [§4.1.1]
    //
    function f(s, x, y, z) 
    {
	switch (s) {
	case 0: return (x & y) ^ (~x & z);           // Ch()
	case 1: return x ^ y ^ z;                    // Parity()
	case 2: return (x & y) ^ (x & z) ^ (y & z);  // Maj()
	case 3: return x ^ y ^ z;                    // Parity()
	}
    }
    
    //
    // rotate left (circular left shift) value x by n positions [§3.2.5]
    //
    function ROTL(x, n)
    {
	return (x<<n) | (x>>>(32-n));
    }

    //
    // extend Number class with a tailored hex-string method 
    //   (note toString(16) is implementation-dependant, and 
    //   in IE returns signed numbers when used on full words)
    //
    Number.prototype.toHexStr = function()
    {
	var s="", v;
	for (var i=7; i>=0; i--) { v = (this>>>(i*4)) & 0xf; s += v.toString(16); }
	return s;
    }


})();