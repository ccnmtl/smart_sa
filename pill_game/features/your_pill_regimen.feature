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
        When I click Add Pill
        Then there are 1 pills
        When I drop pill 1 onto "daytime"
        Then I'm asked to enter a pill name
        Then I dismiss second dialog # Test artifact. dialog appears onBlur, which appears to happen twice with testing
        When I name pill 1 "Foo"
        Then there is a pill named "Foo"
        
    Scenario: A few more pills
        Using selenium
        When I click Add Pill 
        When I name pill 2 "Sam"
        Then there is a pill named "Sam"
        When I click Add Pill
        When I name pill 3 "Bar"
        Then there is a pill named "Bar"
        Then there are 3 pills
        
    Scenario: Specify pill dosage time
        When I specify "daytime" time as "06:00"
        When I specify "evening" time as "19:00"
        
    Scenario: Drop a pill into the daytime bucket
        Using selenium
        When I drop "Foo" onto "daytime"
        Then there is 1 "Foo" in "daytime"
        
    Scenario: Drag a pill from the daytime bucket to the nighttime bucket
        Using selenium
        When I drag "Foo" from "daytime" to "evening"
        Then there is 0 "Foo" in "daytime"
        Then there is 1 "Foo" in "evening"
        
    Scenario: Drop a pill into the nighttime bucket
        Using selenium
        When I drop "Bar" onto "evening"
        Then there is 1 "Bar" in "evening"
    
    Scenario: State is saved in real mode
        Using selenium
        # State save event required at the beginning of a scenaro
        When I specify "daytime" time as "03:00"
        When I click the "Next →" link
        When I click the "← Back" link
        Then I wait 1 second
        Then there are 3 pills
        Then there is a pill named "Foo"
        Then there is a pill named "Sam"
        Then there is a pill named "Bar"
        Then there is 1 "Bar" in "evening"
        Then there is 1 "Foo" in "evening"
        Then the "daytime" time is "03:00"
        Then the "evening" time is "19:00"
        
    Scenario: Drop disabled when "not available" is selected
        Using selenium
        When I specify "daytime" time as "Not taken during the day"
        When I specify "evening" time as "Not taken during the day"
        Then there are no pills in "daytime"
        Then there are no pills in "evening"
        When I drop "Sam" onto "daytime"
        Then there is 0 "Sam" in "daytime"
        When I drop "Sam" onto "evening"
        Then there is 0 "Sam" in "evening"
                
    Scenario: Drag pill off the bucket
        Using selenium
        When I specify "daytime" time as "06:00"
        When I specify "evening" time as "19:00"
        When I drop "Sam" onto "daytime"
        Then there is 1 "Sam" in "daytime"
        When I drag "Sam" off "daytime"
        Then there are no pills in "daytime"
        
    Scenario: Deleting a pill removes it from its bucket, other pills remain
        Using selenium
        When I drop "Foo" onto "daytime"
        When I drop "Foo" onto "daytime"
        When I drop "Foo" onto "daytime"
        When I drop "Foo" onto "evening"
        When I drop "Foo" onto "evening"
        Then there is 3 "Foo" in "daytime"
        Then there is 2 "Foo" in "evening"
        When I drop "Sam" onto "daytime"
        When I drop "Sam" onto "evening"
        When I drop "Bar" onto "daytime"
        When I drop "Bar" onto "evening"            
        When I delete "Foo"
        Then there is no pill named "Foo"
        Then there are 2 pills in "daytime"
        Then there are 2 pills in "evening"
        Then there is 1 "Sam" in "daytime"
        Then there is 1 "Sam" in "evening"
        Then there is 1 "Bar" in "daytime"
        Then there is 1 "Bar" in "evening"
        