Feature: Practice Pill Regimen
    ## The practice pill regimen is currently in Session 1, Activity 7

    Scenario: runthrough
        Using selenium
        Given I am logged in as a counselor
        When I access the url "/"
        When I click the "Let's get started!" link
        When I click the "Counsel" link
        When I fill in "test" in the "name" form field
        When I fill in "test" in the "id_number" form field
        When I submit the "login-participant-form" form
        Then I am on the Intervention page
        
        When I click on Session 1
        When I click on Activity 7
        When I click the "Next →" link
        Then there is a game
        
        #Verify Practice Mode
        Using selenium
        There is a "Practice ARVs" title
        There is not an Add Pill button
        There are 3 pills
        There is a pill named "Tenofovir (TDF)"
        There is a pill named "Lamivudine (3TC)"
        There is a pill named "Efavirennz (EFV)"
        I cannot edit "Tenofovir (TDF)"
        
        # Specify pill dosage time
        When I specify "daytime" time as "06:00"
        When I specify "evening" time as "19:00"
        
        #Drop a pill into the daytime bucket
        When I drop "Tenofovir (TDF)" onto "daytime"
        Then there is 1 "Tenofovir (TDF)" in "daytime"
        
        # Drag a pill from the daytime bucket to the nighttime bucket
        When I drag "Tenofovir (TDF)" from "daytime" to "evening"
        Then there is 0 "Tenofovir (TDF)" in "daytime"
        Then there is 1 "Tenofovir (TDF)" in "evening"
        
        # Drop a pill into the nighttime bucket
        When I drop "Lamivudine (3TC)" onto "evening"
        Then there is 1 "Lamivudine (3TC)" in "evening"
        
        # State is not saved in practice mode
        When I click the "Next →" link
        When I click the "← Back" link
        Then I wait 1 second
        Then there are no pills in "daytime"
        Then there are no pills in "evening"
        Then the "daytime" time is "00:00"
        Then the "evening" time is "12:00"
        
        # Drop disabled when "not available" is selected
        When I specify "daytime" time as "Not taken during the day"
        When I specify "evening" time as "Not taken during the day"
        When I drop "Tenofovir (TDF)" onto "daytime"
        Then there is 0 "Tenofovir (TDF)" in "daytime"
        When I drop "Lamivudine (3TC)" onto "evening"
        Then there is 0 "Lamivudine (3TC)" in "evening"
        
        # Pills are deleted when a time slot is disabled
        Specify "daytime" time as "00:00"
        Specify "evening" time as "12:00"
        When I drop "Tenofovir (TDF)" onto "daytime"
        Then there is 1 "Tenofovir (TDF)" in "daytime"
        When I drop "Lamivudine (3TC)" onto "evening"
        Then there is 1 "Lamivudine (3TC)" in "evening"
        When I specify "daytime" time as "Not taken during the day"
        When I specify "evening" time as "Not taken during the day"
        Then there is 0 "Tenofovir (TDF)" in "daytime"
        Then there is 0 "Lamivudine (3TC)" in "evening"
        When I specify "daytime" time as "00:00"
        When I specify "evening" time as "12:00"
        
        # Drag pill off the bucket
        When I drop "Tenofovir (TDF)" onto "daytime"
        Then there is 1 "Tenofovir (TDF)" in "daytime"
        When I drag "Tenofovir (TDF)" off "daytime"
        Then there are no pills in "daytime"
        
        Finished using selenium
