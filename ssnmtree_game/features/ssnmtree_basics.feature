Feature: SSNMTree Basics

Test the basic functionality of the SSNMTree

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
      Then I click on Activity 10
      When I click the "Next" link
      Then there is a game
      When I fill in the SSNM Tree

      Finished using selenium
