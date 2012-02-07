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
    TestSession.prototype.currentUser = function() {
        if (hasAttr(this.sessStor,this.nsUSER)) {
            return M.evalJSON(this.sessStor[this.nsUSER].value);
        } else {
            this.sessStor[this.nsUSER] = '{}';
            return {};
        }
    };
    TestSession.prototype.saveUser = function(user_info,/*optional:*/ callback, user_key) {
        this.sessStor[this.nsUSER] = M.serializeJSON(user_info);
        if (callback) {
            var response = callback(user_info);
        }
    };

    if (!hasAttr(global,'EphemeralSession')) {
        if (hasAttr(global,'sessionStorage') && hasAttr(global,'globalStorage'))
        {
            if (location.hostname !== '') {
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
