Feature: Life goals
## The life goals regular session is Session 1, Activity 16
## The life goal defaulter session is Session 4, Activity 11

    Scenario: Find the activity
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
        Then I click on Activity 16
        When I click the "Next →" link
        Then there is a game
    
    Scenario: Fill in the steps and goal
        Using selenium
        When I enter "abc" for "Step 2"
        When I enter "def" for "Step 3"
        When I enter "ghi" for "Step 4"
        When I enter "jkl" for "Goal"
        
        # Verify state saved
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        Then I wait 1 second
        
        Then "Step 2" is "abc"
        Then "Step 3" is "def"
        Then "Step 4" is "ghi"
        Then "Goal" is "jkl"
        
        # Navigate to defaulter session
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 4
        When I click on Activity 11
        When I click the "Next →" link
        Then there is a game
        
        # Life goals for defaulter should be the same as regular
        Then "Step 2" is "abc"
        Then "Step 3" is "def"
        Then "Step 4" is "ghi"
        Then "Goal" is "jkl"
        
        When I enter "mno" for "Step 2"
        When I enter "pqr" for "Step 3"
        When I enter "stu" for "Step 4"
        When I enter "vwx" for "Goal"
        
        # Verify state saved
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        Then I wait 1 second
        
        Then "Step 2" is "mno"
        Then "Step 3" is "pqr"
        Then "Step 4" is "stu"
        Then "Goal" is "vwx"
        
        # Navigate back to the regular session
        # Data should remain unchanged
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 1
        Then I click on Activity 16
        When I click the "Next →" link
        Then there is a game
        Then "Step 2" is "abc"
        Then "Step 3" is "def"
        Then "Step 4" is "ghi"
        Then "Goal" is "jkl"