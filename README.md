[![Actions Status](https://github.com/ccnmtl/smart_sa/workflows/build-and-test/badge.svg)](https://github.com/ccnmtl/smart_sa/actions)

0. DETAILS/REQUIREMENTS/INSTALLATION
  #  Project Title: 
        Multimedia Social Support Intervention: 
           Adherence to HIV Care in South Africa.
  # Project Summary: 
     Intervention intended to support South African people on an HIV drug
     treatment plan. Intervention will promote adherence to the drug's
     requirements and coping with side effects. Problem solving to get past
     barriers to adherence is a major theme. Patients will identify one or
     more support people to attend some sessions with them. The
     intervention will use the Social Support Network Map.
  # Project Page:
      http://ccnmtl.columbia.edu/portfolio/medicine_and_health/smart_sa.html
  # Public Code Repository:
      http://github.com/ccnmtl/smart_sa/tree/master
  # Public Instance:
      http://smartsa.ccnmtl.columbia.edu/

  # Requirements:
      * Python (see http://www.djangoproject.com/ for deployment details)
                e.g. for Apache mod_wsgi, etc.
      * Python virtualenv  http://pypi.python.org/pypi/virtualenv
      * Postgres
      * Firefox (for client use)
  # Installation:
      1. $ python create-ve.py
         $ python bootstrap.py
         $ createdb smart_sa #create postgres database
         $ ./manage.py syncdb
         $ ./manage.py runserver <IP Address>:80

  # Code Details:
    This project includes an editor to construct Interventions.  Server
    logins are required for the administrators of the content.  The final
    product is meant to live, possibly, as a static copy on a computer
    with no Internet access.  All client data is stored locally on the
    hard-drive (by Firefox) using DOMStorage:
    	       https://developer.mozilla.org/en/DOM/Storage
    The server can save backup files and deliver restoral files (the same
    HTML file, actually) for backups made on the client from an local
    client admin page.

I. Make sure the directory you checked trunk out into is called
'smart_sa' (not 'smart' or anything else).
  If you do not do this, python will be unable to import things properly that
  reference from the django project level (e.g. 'import smart_sa.urls')
  and it won't work.

II. Deployment:
  1. push to production (make sure settings_production.py is up there too)
  2a: make sure you have a copy of settings_production.py locally, too
  2b. run ./static-copy.sh to generate snapshots/Masivukeni.zip which 
     will be extracted in ~/My Documents/ on the client's laptop

III. HOW TO DEVELOP A GAME
 A. Start the Django App
   1. ./manage.py startapp myawesome_game #creates directory
   #decent example
   2. cp problemsolving_game/models.py myawesome_game/models.py 
   3. rm myawesome_game/views.py #don't really need this
   4. GOTCHA: if you just made the directory, instead of running
	'startapp' then make sure there's an (empty) __init__.py
	in your ./myawesome_game directory

   #Where game-specific CSS, JS, and Images will go
   4. mkdir myawesome_game/media
   5. ln -s ../myawesome_game/media media/myawesome_game

   #Where your game-specific HTML will go
   3. mkdir -p myawesome_game/templates/myawesome_game
   #decent example
   4. cp watchvideo_game/templates/watchvideo_game/video.html myawesome_game/templates/myawesome_game/

   5. add 'smart_sa.myawesome_game' to INSTALLED_APPS in settings_shared.py
      make sure it's before 'smart_sa.intervention'
      NOTE: This is the one step that will actually BREAK your current app
            until you get models.py and the HTML in shape

   6. when you're ready:
      svn add myawesome_game
      svn add media/myawesome_game

 B. Edit models.py and customize pages(), template(), and variables()
    pages(): return a tuple with a string name for each page in the game
             GOTCHA: a tuple with a single string needs a comma like: ('my_page',)
    @arg page_id is the string of the current page in the pages() list.
    template(page_id): return a tuple of two elements:
             1. string for the template in your templates dir.  e.g. 'myawesome_game/video.html'
             2. a dictionary or other object that will be exposed in the HTML templates as {{game_context}}
    variables(page_id): return a list of variables that the Javascript in the game will need to load and store
             NOTE: these variables MUST be complex objects--e.g. arrays or dictionaries in JS
                   so mostly you just need one, that stores the entire state.

 C. Create your game.  
    1. In JAVASCRIPT you can load and store your variables in the following way:

       var my_state = Intervention.getGameVar('myawesome_game', {'default-object-here':'blah,blah'})
              the string from python's variables()-^^^^^^^      ^^^^ default if we're starting from scratch

       Then just keep the 'my_state' variable handy during the page 
       (e.g. make it a global variable, or attach it to your global game object)

       Whenever you want to change something, just...change it from the 'my_state' var,
       and when you want to save it, run:

       Intervention.saveState();

    2. In HTML.  
       * Your template should have {% extends "intervention/game.html" %} at the top
       * Put your make content in {% block game_content %}
       * Custom javascript and CSS in {% block game_js %} {% block game_css %}
             start the src path from '{{INTERVENTION_MEDIA}}myawesome_game/' which starts in 
             your game's media/ path
       * The GamePage object (see intervention/models.py) is available from {{game}}
         The game_context object you passed from template() is available from {{game_context}}
