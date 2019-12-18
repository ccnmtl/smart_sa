Feature: Life goals
## The life goals regular session is Session 1, Activity 16
## The life goal defaulter session is Session 4, Activity 10

    Scenario: Find the activity
        Given I am a participant
        Given I clear the privacy notice

        When I go to Activity 17 of Session 1
        When I click the "Next →" link
        Then there is a game

    Scenario: Fill in the steps and goal
        Given I am a participant
        Given I clear the privacy notice

        When I go to Activity 17 of Session 1
        When I click the "Next →" link
        Then there is a game

        When I enter "a" for "Step 2"
        When I enter "d" for "Step 3"
        When I enter "g" for "Step 4"
        When I enter "j" for "Goal"

        Then "Step 2" is "a"
        Then "Step 3" is "d"
        Then "Step 4" is "g"
        Then "Goal" is "j"

        # Verify state saved
        Then I wait 1 second
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        Then I wait 1 second

        Then "Step 2" is "a"
        Then "Step 3" is "d"
        Then "Step 4" is "g"
        Then "Goal" is "j"

        # Navigate to defaulter session
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 4
        When I click on Activity 10
        When I click the "Next →" link
        Then there is a game

        # Life goals for defaulter should be the same as regular
        Then "Step 2" is "a"
        Then "Step 3" is "d"
        Then "Step 4" is "g"
        Then "Goal" is "j"

        When I enter "mno" for "Step 2"
        When I enter "pqr" for "Step 3"
        When I enter "stu" for "Step 4"
        When I enter "vwx" for "Goal"

        # Verify state saved
        Then I wait 1 second
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        Then I wait 1 second

        Then "Step 2" is "m"
        Then "Step 3" is "p"
        Then "Step 4" is "s"
        Then "Goal" is "v"

        # Navigate back to the regular session
        # Data should remain unchanged
        Then I wait 1 second
        When I click the "Sessions" link
        Then I am on the Intervention page
        When I click on Session 1
        Then I click on Activity 17
        When I click the "Next →" link
        Then there is a game

        Then "Step 2" is "a"
        Then "Step 3" is "d"
        Then "Step 4" is "g"
        Then "Goal" is "j"
