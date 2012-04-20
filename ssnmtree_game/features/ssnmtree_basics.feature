Feature: SSNMTree Basics
## The tree is in Session 1, Activity 12 & 14
## Defaulter Session 4, Activity 65

    Scenario: Fill in the tree & test state save
        Using selenium
        Given I am logged in as a counselor
        Given I have logged in a participant
        When I go to Activity 13 of Session 1
        When I click the "Next →" link
        Then there is a game
        When I fill in the SSNM Tree with "regular"
        There is a filled in SSNM Tree with "regular"
        
        # Verify state saved
        When I click the "Next →" link
        When I click the "← Back" link
        There is a filled in SSNM Tree with "regular"
        Finished using Selenium
        
    Scenario: Test disclosure & support buttons
        Using selenium
        # Disclosure
        Given I am logged in as a counselor
        Given I have logged in a participant
        When I go to Activity 13 of Session 1
        When I click the "Next →" link
        Then there is a game
        When I fill in the SSNM Tree with "regular"
        There is a filled in SSNM Tree with "regular"
        Then "disclosure" is selected
        When I click the circle
        Then the circle is "gold"
        When I click the circle
        Then the circle is not "gold"
        
        # Support
        When I click the "support" button
        When I click the circle
        Then the circle is "purple"
        When I click the circle
        Then the circle is not "purple"
        
        # Disclosure & support
        When I click the "disclosure" button
        When I click the circle
        Then the circle is "gold"
        When I click the "support" button
        When I click the circle
        Then the circle is "gold and purple"
        
        # Verify state saved
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        Then the circle is "gold and purple"
        
        # Check the clear functionality
        Then "disclosure" is selected
        When I clear the circle
        Then the circle is not "gold"
        Then the circle is not "purple"
        
        # Circles cannot have attributes w/o a name
        When I click the circle
        Then the circle is not "gold"
        Finished using Selenium
        
    Scenario: Test Defaulter saving
        Using selenium
        Given I am logged in as a counselor
        Given I have logged in a participant
        When I go to Activity 13 of Session 1
        When I click the "Next →" link
        Then there is a game
        When I fill in the SSNM Tree with "regular"
        There is a filled in SSNM Tree with "regular"
        
        # Need a state save event before navigate
        # otherwise, the json data is not saved
        When I name the circle "regular"
        When I click the circle
        Then the circle is "gold"
        When I click the "support" button
        When I click the circle
        Then the circle is "gold and purple"
        
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 4
        When I click on Activity 14
        When I click the "Next →" link
        Then there is a game
        There is a filled in SSNM Tree with "regular"
        Then the circle is "gold and purple"
        When I fill in the SSNM Tree with "defaulter"
        Then "disclosure" is selected
        
        # Clearing out the name (via fill-in), clears out the attributes
        Then the circle is not "gold"
        Then the circle is not "purple"
        When I click the circle
        Then the circle is "gold"
        
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        There is a filled in SSNM Tree with "defaulter"
        Then the circle is "gold"
        
        # Make sure the regular session data remains the same
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 1
        Then I click on Activity 13
        When I click the "Next →" link
        Then there is a game
        There is a filled in SSNM Tree with "regular"  
        Then the circle is "purple"      
        Finished using Selenium                
        
        
            
         
    
    
    
        
