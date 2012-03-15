Feature: Full Run-Through

Run through the entire intervention. All sessions, 
all activities, all games. Just hit them all in selenium and
check very basic things.

    Scenario: Run-Through
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Intervene" link
      When I fill in "test" in the "name" form field
      When I fill in "test" in the "id_number" form field
      When I click the "Begin" submit button
      Finished using selenium
