APP=smart_sa
JS_FILES=media/js/gamestate.js \
	    media/assessmentquiz_task/js/ media/island_game/js/ media/lifegoal_task/js/ \
	    media/pill_game/js/ media/problemsolving_game/js/ media/ssnmtree_game/js/

all: jenkins

include *.mk
