/**************
InterventionSmart() sets itself to global object Intervention.
This will control the specific user object variables connected with
each activity/game

InterventionSmart DEPENDS ON MochiKit (more than Base?)
and EphemeralSession (e.g. local_session.js)

The user object will be organized as follows:
current_user = {
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
}
 */

/*wrap code with module pattern*/
(function () {
  var global = this;
  var MD = MochiKit.DOM;
  var MB = MochiKit.Base;
  var ML = MochiKit.Logging;
  var MI = MochiKit.Iter;
  var MS = MochiKit.Signal;

  function InterventionSmart() {
    try {
      this.session = global.EphemeralSession;
      // TODO: need to change island_game to not rely on current_user.gender
      // before i can remove this
      this.current_user = global.EphemeralSession.currentUser();
    } catch (e) {
      /*never mind*/
    }
  }

  /*******************************************
  Game Variables
  *******************************************/
  InterventionSmart.prototype.getGameVar = function (key, default_value) {
    if (typeof(default_value) !== 'object') {
      ///this way we can return the pointer, and the original updates
      throw "devault_value required and must be an array or dictionary";
    }
    if (!window.hasAttr(window, 'ss_game_state')) {
      window.ss_game_state = {};
    }

    if (!window.hasAttr(window.ss_game_state, key)) {
      // note from Anders: I don't like that a "get" method
      // sets the default state, but this is the pattern that was here
      // so it should probably stay till we can audit all the game
      // code to make sure it is safe to change.
      window.ss_game_state[key] = default_value;
    }
    return window.ss_game_state[key];
  };
  InterventionSmart.prototype.resetGame = function () {
    // TODO: tweak ss_game_state instead.
    this.saveState();
  };
  InterventionSmart.prototype.saveState = function (callback) {
    var url = "/save_game_state/";
    var deferred = MochiKit.Async.doXHR(url, {'method' : 'POST', 'sendContent' : MB.serializeJSON(window.ss_game_state)});
    if (callback) {
      deferred.addCallback(callback);
    }
  };


  /**************
  INIT Global Instantiation
  **************/
  if (!window.hasAttr(global, 'Intervention')) {
    global.Intervention = new InterventionSmart();
  }
}());
