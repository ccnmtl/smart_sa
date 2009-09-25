var file_count;
var donedone = -1;

function finishedCaching(evt) {
    $('cacheDone').style.backgroundColor = 'green';
    registerDone();
}

function registerDone() {
    if (++donedone) {
	alert('All Done!  You can go offline now.');
    }
}

connect(applicationCache,'oncached',finishedCaching);


function downloadAllPages() {
    var def = doXHR('cache-manifest.txt');
    def.addCallback(function(xhr) {
	var files = xhr.responseText.split("\n");
	file_count = files.length;
	window.updateCount = function() {
	    --file_count;
	    if (file_count==0) {
		$('pagesDone').style.backgroundColor = 'green';
		registerDone();
	    }
	}
	var iframe_string = '';
	forEach(files,function(line) {
	    if (!(/\.html/.test(line))) {
		--file_count;
		return;
	    }
	    iframe_string += '<iframe src="'+line+'" onload="updateCount()" width="1" height="1"></iframe>';
	});
	$("iframe-dumping-ground").innerHTML = iframe_string;
    });
}

//not allowed  TestRunner.hta, user0extensions.js.sample,js.jar,,custom_rhino.jar, gotapi.py, make_docs.py, pack.py, domains.json, intervention_storage.js~, build.py, Color.rst, Signal.rst, DragAndDrop.rst, index.rst, selenium*, mochikit/tests, mochikit/doc/ (includes rsts)
/*
/mochikit/doc/
/mochikit/tests/
/mochikit/scripts/
/selenium/

*~
*.pdf
*.zip
*/