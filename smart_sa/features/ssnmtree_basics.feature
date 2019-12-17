Feature: SSNMTree Basics
## The tree is in Session 1, Activity 12 & 14
## Defaulter Session 4, Activity 13

    Scenario: 1 - Fill in the tree & test state save
        Given I am a participant
        When I go to Activity 13 of Session 1
        When I click the "Next →" link
        Then there is a game
        When I fill in the SSNM Tree with "regular"
        There is a filled in SSNM Tree with "regular"

        # Verify state saved
        When I click the "Next →" link
        Then I wait 1 second
        When I click the "← Back" link
        Then I wait 1 second
        There is a filled in SSNM Tree with "regular"


    Scenario: 2 - Test disclosure & support buttons
        Given I am a participant
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
        Then I wait 2 seconds
        Then the circle is "gold and purple"

        # Check the clear functionality
        Then "disclosure" is selected
        When I clear the circle
        Then the circle is not "gold"
        Then the circle is not "purple"

        # Circles cannot have attributes w/o a name
        When I click the circle
        Then the circle is not "gold"

        # Restore the state
        When I name the circle "regular"
        There is a filled in SSNM Tree with "regular"
