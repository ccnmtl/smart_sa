Feature: Rocking with lettuce and django

    Scenario: Index Page Load
        Given I access the url "/"
        Then I see the header "Welcome to Masivukeni!"
        Then I see the page title "Masivukeni: Welcome!"
	Then the deployment is displayed as "Clinic"

    Scenario: Index Page Load With Selenium
        Using selenium
        Given I access the url "/"
        Then I see the header "Welcome to Masivukeni!"
        Then I see the page title "Masivukeni: Welcome!"	
        Finished using selenium

