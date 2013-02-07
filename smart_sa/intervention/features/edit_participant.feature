Feature: Edit Participant Info

From PMT #80028

    Scenario: Basic Edit
      Using Selenium
      Given I am logged in as an admin
      When I access the management console
      When I go to the Edit Participant page for "test"
      When I toggle the Defaulter checkbox
      When I save
      When I go to the Edit Participant page for "test"
      Then the "name" field has the value "test"
      Finished using Selenium
