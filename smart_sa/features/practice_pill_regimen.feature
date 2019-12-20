Feature: Practice Pill Regimen
    ## The practice pill regimen is currently in Session 1, Activity 7

    Scenario: runthrough
        Given I am a participant
        Given I clear the privacy notice

        When I click on Session 1
        When I click on Activity 7
        When I click the "Next →" link
        Then there is a game
        
        #Verify Practice Mode
        
        Then there is a "Practice ARVs" title
        Then there is not an Add Pill button
        Then there are 3 pills
        Then there is a pill named "Tenofovir (TDF)"
        Then there is a pill named "Lamivudine (3TC)"
        Then there is a pill named "Efavirennz (EFV)"
        Then I cannot edit "Tenofovir (TDF)"
        
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

        # Drag pill off the bucket
        When I drop "Tenofovir (TDF)" onto "daytime"
        Then there is 1 "Tenofovir (TDF)" in "daytime"
