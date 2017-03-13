APP=smart_sa
JS_FILES=media/js/gamestate.js \
	    media/assessmentquiz_task/js/ media/island_game/js/ media/lifegoal_task/js/ \
	    media/pill_game/js/ media/problemsolving_game/js/ media/ssnmtree_game/js/
MAX_COMPLEXITY=7

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
