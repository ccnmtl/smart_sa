Feature: Your Pill Regimen
    ## The your pill regimen is currently in Session 3, Activity 21

    Scenario: runthrough 
        # Find activity
        
        Given I am a participant
        
        When I click on Session 3
        When I click on Activity 21
        When I click the "Next" link
        Then there is a game
        
        # Verify Real Mode
        There is a "Medication List" title
        There is an Add Pill button
        There are 0 pills
        When I click Add Pill
        Then there are 1 pills
        When I drop pill 1 onto "daytime"
        # Then I'm asked to enter a pill name
        # When I name pill 1 "Foo"
        # Then there is a pill named "Foo"
        # I can edit "Foo"
        # When I name pill 1 "ish"
        # Then there is a pill named "Fooish"
        
        # # A few more pills
        # When I click Add Pill 
        # When I name pill 2 "Sam"
        # Then there is a pill named "Sam"
        # When I click Add Pill
        # When I name pill 3 "Bar"
        # Then there is a pill named "Bar"
        # Then there are 3 pills
        
        # # Specify pill dosage time
        # When I specify "daytime" time as "06:00"
        # When I specify "evening" time as "19:00"
        
        # # Drop a pill into the daytime bucket
        # When I drop "Fooish" onto "daytime"
        # Then there is 1 "Fooish" in "daytime"
        
        # # Drag a pill from the daytime bucket to the nighttime bucket
        # When I drag "Fooish" from "daytime" to "evening"
        # Then there is 0 "Fooish" in "daytime"
        # Then there is 1 "Fooish" in "evening"
        
        # # Drop a pill into the nighttime bucket
        # When I drop "Bar" onto "evening"
        # Then there is 1 "Bar" in "evening"
    
        # # State is saved in real mode
        # # State save event required at the beginning of a scenaro
        # When I specify "daytime" time as "03:00"
        # When I click the "Next →" link
        # When I click the "← Back" link
        # Then I wait 1 second
        # Then there are 3 pills
        # Then there is a pill named "Fooish"
        # Then there is a pill named "Sam"
        # Then there is a pill named "Bar"
        # Then there is 1 "Bar" in "evening"
        # Then there is 1 "Fooish" in "evening"
        # Then the "daytime" time is "03:00"
        # Then the "evening" time is "19:00"
        
        # # Drop disabled when "not available" is selected
        # When I specify "daytime" time as "Not taken during the day"
        # When I specify "evening" time as "Not taken during the day"
        # Then there are no pills in "daytime"
        # Then there are no pills in "evening"
        # When I drop "Sam" onto "daytime"
        # Then there is 0 "Sam" in "daytime"
        # When I drop "Sam" onto "evening"
        # Then there is 0 "Sam" in "evening"
                
        # # Drag pill off the bucket
        # When I specify "daytime" time as "06:00"
        # When I specify "evening" time as "19:00"
        # When I drop "Sam" onto "daytime"
        # Then there is 1 "Sam" in "daytime"
        # When I drag "Sam" off "daytime"
        # Then there are no pills in "daytime"
        
        # # Deleting a pill removes it from its bucket, other pills remain
        # When I drop "Fooish" onto "daytime"
        # When I drop "Fooish" onto "daytime"
        # When I drop "Fooish" onto "daytime"
        # When I drop "Fooish" onto "evening"
        # When I drop "Fooish" onto "evening"
        # Then there is 3 "Fooish" in "daytime"
        # Then there is 2 "Fooish" in "evening"
        # When I drop "Sam" onto "daytime"
        # When I drop "Sam" onto "evening"
        # When I drop "Bar" onto "daytime"
        # When I drop "Bar" onto "evening"            
        # When I delete "Fooish"
        # Then there is no pill named "Fooish"
        # Then there are 2 pills in "daytime"
        # Then there are 2 pills in "evening"
        # Then there is 1 "Sam" in "daytime"
        # Then there is 1 "Sam" in "evening"
        # Then there is 1 "Bar" in "daytime"
        # Then there is 1 "Bar" in "evening"
            
        # # Limit of 10 pills
        # Then there are 2 pills
        # When I click Add Pill
        # When I click Add Pill
        # When I click Add Pill
        # When I click Add Pill
        # When I click Add Pill
        # When I click Add Pill
        # When I click Add Pill
        # When I click Add Pill
        # Then there are 10 pills
        # When I click Add Pill
        # Then I'm told I can only enter 10 pills
