#!/bin/bash
rm -rf $HOME/tmp_chrome
cp -R $HOME/clean_chrome $HOME/tmp_chrome
chromium-browser --user-data-dir=$HOME/tmp_chrome http://masivukeni2.ccnmtl.columbia.edu/site_media/selenium/TestRunner.html\?test\=..%2Ftests%2FTestSuite.html\&resultsUrl\=..%2FpostResults

