Feature: Management Interface

Test out the management interface.

    Scenario: Not Logged In
      Given I am not logged in
      When I access the management console
      Then I am taken to a login screen

    Scenario: Logged In As Counselor
      Given I am logged in as a counselor
      When I access the management console
      Then there is not an "+ Add a Counselor" link

    Scenario: Logged in as Admin
      Given I am logged in as an admin
      When I access the management console
      Then there is an "+ Add Participant" link
      Then there is an "+ Add a Counselor" link
      Then there is a location edit form

