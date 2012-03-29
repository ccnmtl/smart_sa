Feature: Conditional Completion for Session Nav

from PMT #79450. "At the session level (session.html), can a user only
see the We're Done with Session #! button once the session
is actually complete instead of a persistent placement?"

    Scenario: Not completed any activities in the session
      Given I am logged in as a counselor
      Given I have logged in a participant
      Given the participant has not completed any sessions
      When I go to Session 1
      Then there is no "Click to Complete Session 1!" button

    Scenario: Some activities completed, but not all
      Given I am logged in as a counselor
      Given I have logged in a participant
      Given the participant has completed 1 activity in session 1
      When I go to Session 1
      Then there is no "Click to Complete Session 1!" button

    Scenario: All activities completed
      Given I am logged in as a counselor
      Given I have logged in a participant
      Given the participant has completed all activities in session 1
      When I go to Session 1
      Then there is a "Click to Complete Session 1!" button

      
