Feature: Hide Other Counselors

From PMT #79863 hide other counselors on adminstrate page for counselors

    Scenario: Admin Can See Counselors Table
      Given I am logged in as an admin
      When I access the management console
      Then there is a counselors table

    Scenario: Counselor Can Not See Counselors Table      
      Given I am logged in as a counselor
      When I access the management console
      Then there is not a counselors table
