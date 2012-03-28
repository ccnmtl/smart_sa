Feature: Case-Insensitive Participant Login

PMT #79572

    Scenario: Normal
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Intervene" link
      When I fill in "test" in the "name" form field
      When I fill in "test" in the "id_number" form field
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      Finished using selenium

    Scenario: Wrong Case for Name
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Intervene" link
      When I fill in "tESt" in the "name" form field
      When I fill in "test" in the "id_number" form field
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      Finished using selenium

    Scenario: Wrong Case for Participant ID
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Intervene" link
      When I fill in "test" in the "name" form field
      When I fill in "teST" in the "id_number" form field
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      Finished using selenium

    Scenario: Wrong Case for Both
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Intervene" link
      When I fill in "Test" in the "name" form field
      When I fill in "tesT" in the "id_number" form field
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      Finished using selenium

