Feature: Edit Deployment is Admin Only

From PMT #79865 make location name not editable for counselors

    Scenario: Admin Can Edit Deployment
      Given I am logged in as an admin
      When I access the management console
      Then there is an edit deployment form

    Scenario: Counselor Can Not Edit Deployment
      Given I am logged in as a counselor
      When I access the management console
      Then there is not an edit deployment form

