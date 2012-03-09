Feature: Index Page

Just some simple sanity checks on the index page of the application
This also serves as a good test that the lettuce and selenium
stuff is all hooked up properly and running. 

    Scenario: Index Page Load
        Given I am not logged in
        When I access the url "/"
        Then I see the header "Welcome to Masivukeni!"
        Then I see the page title "Masivukeni: Welcome!"
	Then the deployment is displayed as "Clinic"
	Then I am not logged in
	Then there is a login link
#	Then I see a counselor login form
#	Then I do not see a WIND login form

    Scenario: Index Page Load With Selenium
        Using selenium
        When I access the url "/"
        Then I see the header "Welcome to Masivukeni!"
        Then I see the page title "Masivukeni: Welcome!"	
        Finished using selenium
        
