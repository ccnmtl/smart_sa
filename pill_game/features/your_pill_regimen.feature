Feature: Your Pill Regimen
    ## The your pill regimen is currently in Session 3, Activity 3

    Scenario: Find activity
        Using selenium
        Given I am logged in as a counselor
        When I access the url "/"
        When I click the "Let's get started!" link
        When I click the "Intervene" link
        When I fill in "test" in the "name" form field
        When I fill in "test" in the "id_number" form field
        When I submit the "login-participant-form" form
        Then I am on the Intervention page
        
        When I click on Session 3
        When I click on Activity 3
        When I click the "Next" link
        Then there is a game
        
    Scenario: Verify Real Mode
        Using selenium
        There is a "Medication List" title
        There is an Add Pill button
        There are 0 pills
        When I click the "Add a Pill" link
        Then there are 1 pills
        
        

