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
        When I click the "Next →" link
        Then there is a game
        
    Scenario: Verify Practice Mode
        Using selenium
        There is a "Practice Regimen" title
        There is not an Add Pill button
        There are 3 pills
        There is a pill named "D4T"
        There is a pill named "3TC"
        There is a pill named "Efavirenz"
        
    Scenario: Specify pill dosage time
        When I specify "daytime" time as "06:00"
        When I specify "evening" time as "19:00"
        
    Scenario: Drop a pill into the daytime bucket
        Using selenium
        When I drop "D4T" onto "daytime"
        Then there is 1 "D4T" in "daytime"
        
    Scenario: Drag a pill from the daytime bucket to the nighttime bucket
        Using selenium
        When I drag "D4T" from "daytime" to "evening"
        Then there is 0 "D4T" in "daytime"
        Then there is 1 "D4T" in "evening"
        
    Scenario: Drop a pill into the nighttime bucket
        Using selenium
        When I drop "3TC" onto "evening"
        Then there is 1 "3TC" in "evening"
        
    Scenario: State is not saved in practice mode
        Using selenium
        When I click the "Next →" link
        When I click the "← Back" link
        Then I wait 1 second
        Then there are no pills in "daytime"
        Then there are no pills in "evening"
        Then the "daytime" time is "00:00"
        Then the "evening" time is "12:00"
        
    Scenario: Drop disabled when "not available" is selected
        Using selenium
        When I specify "daytime" time as "Not taken during the day"
        When I specify "evening" time as "Not taken during the day"
        When I drop "D4T" onto "daytime"
        Then there is 0 "D4T" in "daytime"
        When I drop "3TC" onto "evening"
        Then there is 0 "3TC" in "evening"
        
    Scenario: Pills are deleted when a time slot is disabled
        Using selenium
        Specify "daytime" time as "00:00"
        Specify "evening" time as "12:00"
        When I drop "D4T" onto "daytime"
        Then there is 1 "D4T" in "daytime"
        When I drop "3TC" onto "evening"
        Then there is 1 "3TC" in "evening"
        When I specify "daytime" time as "Not taken during the day"
        When I specify "evening" time as "Not taken during the day"
        Then there is 0 "D4T" in "daytime"
        Then there is 0 "3TC" in "evening"
        When I specify "daytime" time as "00:00"
        When I specify "evening" time as "12:00"
        
    Scenario: Drag pill off the bucket
        Using selenium
        When I drop "D4T" onto "daytime"
        Then there is 1 "D4T" in "daytime"
        When I drag "D4T" off "daytime"
        Then there are no pills in "daytime"
