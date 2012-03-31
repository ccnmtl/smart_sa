Feature: Quiz Basics

Check the basic functionality of the quiz

    Scenario: Fill it in
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
      Then I click on Activity 7
      When I click the "Next" link
      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz
      When I fill in all 3s in the quiz
      Finished using selenium
