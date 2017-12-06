Feature: Life goals
## The life goals regular session is Session 1, Activity 16
## The life goal defaulter session is Session 4, Activity 10

    Scenario: Find the activity
        Using selenium
        Given I am a participant
        When I go to Activity 17 of Session 1
        When I click the "Next →" link
        Then there is a game
        Finished using selenium

    Scenario: Fill in the steps and goal
        Using selenium
        Given I am a participant
        When I go to Activity 17 of Session 1
        When I click the "Next →" link
        Then there is a game

        When I enter "abc" for "Step 2"
        When I enter "def" for "Step 3"
        When I enter "ghi" for "Step 4"
        When I enter "jkl" for "Goal"

        Then "Step 2" is "abc"
        Then "Step 3" is "def"
        Then "Step 4" is "ghi"
        Then "Goal" is "jkl"
        Then I wait 1 second

        # Verify state saved
        When I click the "Next →" link
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
        When I click on Activity 10
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
        Then I click on Activity 17
        When I click the "Next →" link
        Then I wait 1 second
        Then there is a game
        Then "Step 2" is "abc"
        Then "Step 3" is "def"
        Then "Step 4" is "ghi"
        Then "Goal" is "jkl"

        Finished using selenium
