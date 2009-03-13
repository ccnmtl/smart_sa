/*
  This leverages FIREFOX-ONLY security features
  Some documentation on UniversalBrowserWrite and other 'privileges' is at:
http://www.csie.ntu.edu.tw/~piaip/docs/CreateMozApp/mozilla-chp-12-sect-7.html

for encryption details see:
http://www.josh-davis.org/ecmascrypt
which will work with python version 
http://www.josh-davis.org/pythonAES

 */


///JS module pattern
(function() {
    var global = this;

    function UserAdmin() {
	try {
	    this.session = global.EphemeralSession;
	    if (!this.session.isAdmin()) {
		window.back();
		return;
	    }
	} catch(e) {/*never mind*/}
	connect(window,'onload',this,'onLoad');
    }
    
    UserAdmin.prototype.onLoad = function() {
    }

    UserAdmin.prototype.multi_user_add = function() {
	var self = this;
	var form_vals = formContents('mass_user_add')[1];
	var users = form_vals[0].split(/\n|\r/);
	forEach(users, function(user_line) {
	    var fields = user_line.split(/\s*,\s*/);
	    var user = {
		'firstname':fields[1],
		'fullname':fields[1]+' '+fields[0],
		'patientnumber':fields[2],
		'gender':String(fields[3]).toUpperCase().substr(0,1)
	    };
	    if (user.firstname && user.patientnumber) {
		self.session.createUser(user.firstname,user.patientnumber,user);
	    }
	});
	alert('The names are saved!');
    }
    UserAdmin.prototype.addUser = function() {
	var fields = formContents('single_user_add')[1];

	var user = {
	    'firstname':fields[0],
	    'fullname':fields[0]+' '+fields[1],
	    'patientnumber':fields[2],
	    'gender':String(fields[3]).toUpperCase().substr(0,1),
	};
	if (fields[4] && //is Admin
	    confirm('Are you sure you want this user to be a Intervention Administrator (with access to this page)?')) {
	    user['admin'] = fields[4];
	}
	var user_key = this.session.createUser(user.firstname,
	    user.patientnumber,user);
	if (user_key) {
	    $('single_user_add').reset();
	    this.showUser(user_key);
	}
    }
    UserAdmin.prototype.showUser = function(user_key) {
	var user = evalJSON(this.session.permStor[user_key].value);
	getElement('client-list').appendChild(LI(null,user.firstname,
						 SPAN(user.admin?' (ADMIN: Non-client) ':'')
						));
    }
    UserAdmin.prototype.showClients = function() {
	var self = this;
	removeElement('show_clients_button');
	for (a in self.session.permStor) {
	    if (RegExp('^'+self.session.nsUSER).test(a)) {
		this.showUser(a);
	    }
	}
    }

    /***********************
     BACKUP
     ***********************/
    UserAdmin.prototype.showRestorals = function() {
	var self = this;

	restorals = false;
	function makeRestoralLink(name,hilite) {
	    name = A({'id':name,'href':'#'+name+'','onclick':"UserAdmin.restore('"+name+"')"},name);
	    var attrs = null;
	    if (hilite) {
		//attrs = {'class':'hilite'};
		name = SPAN(null,SPAN(null,name),': Most recent backup that you loaded in to restore');
	    }
	    var r = LI(attrs,name);
	    getElement('restoral-list').appendChild(r);
	}
	if (hasAttr(self.session.permStor,self.session.RESTORE_KEY)) {
	    makeRestoralLink(self.session.permStor[self.session.RESTORE_KEY].value,true);
	}
	for (a in self.session.permStor) {
	    if (RegExp('^'+self.session.nsBACKUP).test(a)) {
		restorals = true;
		makeRestoralLink(a);
	    }
	}
	if (restorals) hideElement('no-restorals');
	showElement('restorals');
	hideElement('show_backups');
    }

    UserAdmin.prototype.backup_string = function() {
	var self = this;
	var the_object = self.session.permStor;
	var the_package = {};
	for (a in the_object) {
	    //only non-backup strings
	    if (RegExp('^'+self.session.nsUSER).test(a)) {
		the_package[a] = the_object[a].value;
	    }
	}
	var plaintext = serializeJSON(the_package);
	if (typeof(encrypt_key) == 'string') {
	    return self.encrypt(plaintext);
	}
	else return plaintext;
    }
    
    UserAdmin.prototype.cryptArgs = function() {
	///see http://www.josh-davis.org/ecmascrypt
	var mode = 0; //OFB
	var keysize = 32; //for 256
	var hexkey = global.encrypt_key;
	var iv_hexvalue = global.encrypt_iv;
	return [mode,ecmaScrypt.toNumbers(hexkey),keysize,ecmaScrypt.toNumbers(iv_hexvalue)];
    }

    UserAdmin.prototype.encrypt = function(plaintext) {
	var self = this;
	var crypt_args = self.cryptArgs();
	crypt_args.unshift(plaintext);

	var ciph = ecmaScrypt.encrypt.apply(ecmaScrypt,crypt_args);
	var outhex = '';
	for(var i = 0;i < ciph.cipher.length;i++) {
	    outhex += ecmaScrypt.toHex(ciph.cipher.charCodeAt(i));
	}
	return outhex;
    }    
    UserAdmin.prototype.decrypt = function(ciphtext) {
	var self = this;
	var crypt_args = self.cryptArgs();
	var innumbers = ecmaScrypt.toNumbers(ciphtext);
	var ciph_string = '';
	for(var i = 0;i < innumbers.length; i++) {
	    ciph_string += String.fromCharCode(innumbers[i]);
	}
	crypt_args.unshift(ciph_string,0);
	var plaintext = ecmaScrypt.decrypt.apply(ecmaScrypt,crypt_args);
	return plaintext;
    }
    ///whether from local file system or on the server, 
    ///backup the client data on the server
    UserAdmin.prototype.send_to_server = function() {
	var self = this;	
	self.destination = getElement('mother-server').innerHTML;
	var full_destination = 'http://'+self.destination+'/store_backup'

	var myXMLHTTPRequest = new XMLHttpRequest();

	var backup_string = self.backup_string();
	if (location.host != self.destination ) {
	    try {
		alert('You are about to be prompted for security access to the Internet, so we can backup the application data to the server.');
		netscape.security.PrivilegeManager.enablePrivilege( "UniversalBrowserRead" );

		///we have to do this here, because the request has to 
		///come from the same file that requests the privilege
		myXMLHTTPRequest.open("POST",full_destination , false);
		myXMLHTTPRequest.send(queryString({'backup':backup_string}));
		global.sky = myXMLHTTPRequest; //debug
	    } catch(e) {///*FAIL!!!
		alert('Unable to access the server for backup');
		logError(e);
		return;
	    }
	}
	else {
	    var d = doXHR(full_destination, 
		{
		    'method':'POST',
		    'sendContent':queryString({'backup':backup_string})
		});
	    global.sky = d; //debug
        }
    }
    
    UserAdmin.prototype.save_to_file = function() {
	var self = this;
	setTimeout(function() {
	    var nsBACKUP = self.session.nsBACKUP;

	    var backup_string = self.backup_string();
	    
	    var now = new Date();
	    var date_string = [now.getFullYear(),now.getMonth()+1,now.getDate(),now.getSeconds()].join('-');
	    //save it in session data -- who knows how useful this will be.
	    self.session.permStor[nsBACKUP+date_string] = backup_string;
	    function writeDocument(mydoc) {
		var my_filename = String(location.pathname).split('/').pop();
		///NOTE: this should mirror the content in intervention/templates/intervention/restore.html
		mydoc.write('<h2>Save this file</h2>');
		mydoc.write('<p>From the <b>File</b> menu, click <b>Save Page As</b> and make sure the file location is on your portable drive which you will upload from the computer with an Internet connection.  It will save as <b>'+my_filename+'</b> but you can change this to something else.</p>');
		mydoc.write('<p>If for some reason, you need to restore a backup, put this file in the My Documents folder naming it <b>restore.html</b>, and run the Restore shortcut from your Desktop.  Then you can go into the admin interface and restore from there.</p>');
		mydoc.write('<h2>Data</h2><div id="data">');
		mydoc.write(backup_string);
		mydoc.write('</div>');
		mydoc.write('<script type="text/javascript">globalStorage[location.hostname]["'+nsBACKUP+date_string+'"] = document.getElementById("data").innerHTML;globalStorage[location.hostname]["RESTORE"]="'+nsBACKUP+date_string+'";</script>');
		mydoc.close();
	    }
	    var doc;
	    try {
		doc = getElement('filebackup').contentDocument;
		netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
		writeDocument(doc);
		
		var filename = 'backup-'+date_string+'.html';
		
		///call to function in chrome://global/content/contentAreaUtils.js
		internalSave(doc.location.href, doc, null, 
			     'attachment; filename='+filename,
			     doc.contentType, false, null, null,
			     doc.referrer ? makeURI(doc.referrer) : null,
			     false);
	    } catch(e) {
		logError('cannot trigger SaveAs');
		doc = document;
		writeDocument(doc);
	    }
	},10);
    }

    UserAdmin.prototype.restore = function(backup_key) {
	var self = this;
	if(confirm('This will delete all current client/account data, \
                    and replace it with the restoring data. \
                    Are you sure?')) {
	    var backup_string = self.session.permStor[backup_key].value;
	    var plaintext = self.decrypt(backup_string);
	    var the_package = evalJSON(plaintext);
	    ///DELETE old data
	    for (a in self.session.permStor) {
		if (RegExp('^'+self.session.nsUSER).test(a)) {
		    delete self.session.permStor[a];
		}
	    }
	    ///RESTORE old data
	    for (a in the_package) {
		self.session.permStor[a] = the_package[a];
	    }
	}
    }

    /**************
     Init Global Instantiation
     **************/
    if (!hasAttr(global,'UserAdmin')) {
	global.UserAdmin = new UserAdmin();
    }
})();
