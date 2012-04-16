Feature: SSNMTree Basics
## The tree is in Session 1, Activity 12 & 14
## Defaulter Session 4, Activity 65

    Scenario: Fill in the tree & test state save
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
        Then I click on Activity 12
        When I click the "Next →" link
        Then there is a game
        When I fill in the SSNM Tree with "regular"
        When I click the "Next →" link
        When I click the "← Back" link
        There is a filled in SSNM Tree with "regular"
        
    Scenario: Test Defaulter saving
        Using selenium
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 4
        When I click on Activity 13
        When I click the "Next →" link
        Then there is a game
        When I fill in the SSNM Tree with "defaulter"
        When I click the "Next →" link
        When I click the "← Back" link
        There is a filled in SSNM Tree with "defaulter"
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 1
        Then I click on Activity 12
        When I click the "Next →" link
        Then there is a game
        There is a filled in SSNM Tree with "regular"
            
         
    
    
    
        
