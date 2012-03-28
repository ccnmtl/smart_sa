Feature: Activity -> Game Lateral Navigation

From PMT #79451: "Could you help me make the lateral navigation better? 
At the activity level (activity.html), can we:
1. Relegate the interactivity of the Let's Begin! button up to the Next -> button instead.
2. Eliminate the now redundant Let's Begin! Button
3. Include this lateral navigation at the interactivity phase (game.html) too. 
Clicking Next -> when the interactivity phase is complete advances the user to the next activity."

    Scenario: Activity With Game
        Given I am logged in as a counselor
        Given I have logged in a participant
        When I go to Session 1, Activity 3
        Then there is a "Next →" nav button
        Then there is no "Let's Begin!" nav button

    Scenario: Going back
        # from Susan's comment on the PMT:
        # When using the "Previous" button -- navigating from an activity back to a game page leaps to the prior activity page 1 rather than to the game page x.
        # To reproduce the behavior:
        # http://masivukeni2.ccnmtl.columbia.edu/activity/110/.
        # Then click the "Previous" button.
        # Expected: http://masivukeni2.ccnmtl.columbia.edu/task/109/addnames/
        # Actual: http://masivukeni2.ccnmtl.columbia.edu/activity/15/
        Given I am logged in as a counselor
        Given I have logged in a participant
        When I go to Session 1, Activity 8
        When I click the "Back" link
        Then there is a game
        Then I am not on an activity page
        Then I am on a game page
