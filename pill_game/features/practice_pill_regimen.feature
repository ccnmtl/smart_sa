Feature: Practice Pill Regimen
    ## The practice pill regimen is currently in Session 1, Activity 7

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
        
        When I click on Session 1
        When I click on Activity 7
        When I click the "Next" link
        Then there is a game
        
    Scenario: Verify Practice Mode
        Using selenium
        There is a "Practice Regimen" title
        There is not an Add Pill button
        There are 3 pills
        There is a pill named "D4T"
        There is a pill named "3TC"
        There is a pill named "Efavirenz"
        
    Scenario: Specify pill dosage schedule
        Specify "daytime" schedule as "06:00"
        Specify "evening" schedule as "19:00"
        
    Scenario: Drop a pill into the daytime bucket
        Using selenium
        When I drop "D4T" into the "daytime" slot
        Then there is 1 "D4T" in the "daytime" slot
        
    Scenario: Drag a pill from the daytime bucket to the nighttime bucket
        Using selenium
        When I drag "D4T" from the "daytime" slot into the "evening" slot
        Then there is 0 "D4T" in the "daytime" slot
        Then there is 1 "D4T" in the "evening" slot
        
    Scenario: Drop a pill into the nighttime bucket
        Using selenium
        When I drop "3TC" into the "evening" slot
        Then there is 1 "3TC" in the "evening" slot
        
    Scenario: State is not saved in practice mode
        Using selenium
        When I click the "Next" link
        When I click the "Back" link
        Then there are no pills in the "daytime" slot
        Then there are no pills in the "evening" slot
        Then the "daytime" schedule is "00:00"
        Then the "evening" schedule is "12:00"
        
    Scenario: Drop disabled when "not available" is selected
        Using selenium
        When I specify "daytime" schedule as "Not taken during the day"
        When I specify "evening" schedule as "Not taken during the day"
        When I drop "D4T" into the "daytime" slot
        Then there is 0 "D4T" in the "daytime" slot
        When I drop "3TC" into the "evening" slot
        Then there is 0 "3TC" in the "evening" slot
        
    Scenario: Pills are deleted when a time slot is disabled
        Specify "daytime" schedule as "00:00"
        Specify "evening" schedule as "12:00"
        When I drop "D4T" into the "daytime" slot
        Then there is 1 "D4T" in the "daytime" slot
        When I drop "3TC" into the "evening" slot
        Then there is 1 "3TC" in the "evening" slot
        When I specify "daytime" schedule as "Not taken during the day"
        When I specify "evening" schedule as "Not taken during the day"
        Then there is 0 "D4T" in the "daytime" slot
        Then there is 0 "3TC" in the "evening" slot
        
        
