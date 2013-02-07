Feature: Admin Access

From PMT #79862 'administrate' button needs to show up for counselors

I just logged in as a counselor and the only buttons available 
on my home page are intervene and practice. I should also see 'administrate'

    Scenario: Admin sees Administrate link
      Given I am logged in as an admin
      When I access the counselor landing page
      Then there is an "Administrate" link

    Scenario: Counselor sees Administrate link
      Given I am logged in as a counselor
      When I access the counselor landing page
      Then there is an "Administrate" link
