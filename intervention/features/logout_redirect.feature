Feature: Logout redirect

PMT #79460: "log out for non-uni users goes to django page 
and then 'log back in' goes to 404"

    Scenario: Logout
      Given I am logged in as a counselor
      When I log out
      Then I am taken to the index

