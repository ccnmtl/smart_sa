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
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      When I click on Session 1
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      # assessment quiz
      When I click on Complete Activity
      Then I am on the Activity 4 page
      When I click on Complete Activity
      Then I am on the Activity 5 page
      # ssnmtree
      When I click on Complete Activity
      Then I am on the Activity 6 page
      # ssnmtree
      When I click on Complete Activity
      Then I am on the Activity 7 page
      # reasons to stay healthy
      When I click on Complete Activity
      Then I am on the Activity 8 page
      When I click on Complete Activity
      Then I am on the Session 1 page

      When I click on Session 2
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      When I click on Complete Activity
      Then I am on the Activity 4 page
      # watchvideo
#      When I click on Complete Activity
#      Then I am on the Activity 5 page
#      When I click on Complete Activity
#      Then I am on the Activity 6 page
      # ssnmtree
#      When I click on Complete Activity
#      Then I am on the Activity 7 page
      # reasons to stay healthy
#      When I click on Complete Activity
#      Then I am on the Activity 8 page
#      When I click on Complete Activity
#      Then I am on the Session 2 page

      When I click the "Sessions" link
      When I click on Session 3
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      # watchvideo
      When I click on Complete Activity
      Then I am on the Activity 3 page
      When I click on Complete Activity
      Then I am on the Activity 4 page
      When I click on Complete Activity
      Then I am on the Activity 5 page
      When I click on Complete Activity
      Then I am on the Activity 6 page
      # watchvideo
      When I click on Complete Activity
      Then I am on the Activity 7 page
      # reasons to stay healthy
      When I click on Complete Activity
      Then I am on the Activity 8 page
      When I click on Complete Activity
      Then I am on the Session 3 page

      When I click on Session 4
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      # pill game
      When I click on Complete Activity
      Then I am on the Activity 3 page
      # watchvideo
      When I click on Complete Activity
      Then I am on the Activity 4 page
      When I click on Complete Activity
      Then I am on the Activity 5 page
      When I click on Complete Activity
      Then I am on the Activity 6 page
      When I click on Complete Activity
      Then I am on the Session 4 page

      # defaulter sessions
      When I click on Session 5
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      # quiz
      # When I click on Complete Activity
      # Then I am on the Activity 3 page
      # When I click on Complete Activity
      # Then I am on the Activity 4 page
      # pill game
      # When I click on Complete Activity
      # Then I am on the Activity 5 page
      # watchvideo
      # When I click on Complete Activity
      # Then I am on the Activity 6 page
      # ssnmtree
      # When I click on Complete Activity
      # Then I am on the Activity 7 page
      # reasons to stay healthy
      # When I click on Complete Activity
      # Then I am on the Session 5 page
      When I click the "Sessions" link

      When I click on Session 6
      When I click on Activity 1
      Then I am on the Activity 1 page
      # problem solving
      When I click on Complete Activity
      Then I am on the Activity 2 page
      # watchvideo
      When I click on Complete Activity
      Then I am on the Activity 3 page
      When I click on Complete Activity
      Then I am on the Session 6 page

      Finished using selenium
