(function(jQuery) {
    var global = this;

    global.GameState = Backbone.View.extend({
        initialize: function(options) {
            var gameState = global.Intervention.getGameVar(options.game, {});
            var userState = this.el ? 'defaulter' : 'regular';

            if (!_.has(gameState, userState)) {
                if (!_.has(gameState, userState) &&
                    userState === 'defaulter' && _.has(gameState, 'regular')) {
                    gameState.defaulter = _.clone(gameState.regular);
                } else {
                    gameState[userState] = {};
                }
            }

            this.gameState = gameState[userState];
        },

        getKeys: function() {
            return _.keys(this.gameState);
        },

        getState: function(id) {
            return _.has(this.gameState, id) ? this.gameState[id] : null;
        },

        setState: function(id, obj) {
            this.gameState[id] = obj;
        }
    });

    jQuery('#breadcrumb-main a').on('click', function() {
        if(document.completeactivity) {
            document.completeactivity.next.value=this.href;
            document.completeactivity.submit();
            return false;
        }
    });

    jQuery('#breadcrumb a').on('click', function() {
        if(document.completeactivity) {
            document.completeactivity.next.value=this.href;
            document.completeactivity.submit();
            return false;
        }
    });
}(jQuery));
