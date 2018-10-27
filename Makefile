APP=smart_sa
JS_FILES=media/js/gamestate.js \
	    media/assessmentquiz_task/js/ media/island_game/js/ media/lifegoal_task/js/ \
	    media/pill_game/js/ media/problemsolving_game/js/ media/ssnmtree_game/js/
MAX_COMPLEXITY=7
FLAKE8_IGNORE=W605

all: jenkins

include *.mk

harvest: $(PY_SENTINAL)
	$(MANAGE) harvest --settings=$(APP).settings_test --failfast -v 3 -a smart_sa.intervention,smart_sa.pill_game,smart_sa.lifegoal_task,smart_sa.assessmentquiz_task,smart_sa.problemsolving_game

harvest2: $(PY_SENTINAL)
	$(MANAGE) harvest --settings=$(APP).settings_test --failfast -v 3 -a smart_sa.ssnmtree_game
