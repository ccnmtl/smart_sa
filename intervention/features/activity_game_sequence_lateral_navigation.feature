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
        When I go to Session 1
        When I go to Activity 3
        Then there is a "Next" button
