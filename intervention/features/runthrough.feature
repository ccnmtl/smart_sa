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
      
      ## SESSION 1
      When I click on Session 1
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      When I click on Complete Activity
      Then I am on the Activity 4 page
      When I click on Complete Activity
      Then I am on the Activity 5 page
      When I click on Complete Activity
      Then I am on the Activity 6 page
      When I click on Complete Activity
      Then I am on the Activity 7 page
      When I click the "Next" link

      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz
      When I fill in all 3s in the quiz
      When I click the "Next" link
      Then I am on the Activity 8 page
      When I click the "Next" link

      # assessment quiz part 2 - alcohol audit
      Then there is a game
      Then there is an assessmentquiz-audit
      When I fill in all 2s in the quiz
      When I click the "Next" link
      Then I am on the Activity 9 page

      # assessment quiz part 3 - drug audit
      When I click the "Next" link
      Then there is a game
      Then there is an assessmentquiz-audit
      When I fill in all 2s in the quiz
      When I click the "Next" link
      Then I am on the Activity 10 page
      When I click the "Next" link

      # ssnmtree
      Then there is a game
      When I fill in the SSNM Tree
      When I click the "Next" Link
      Then I am on the Activity 11 page
      When I click the "Next" link
      Then I am on the Activity 12 page
      # ssnmtree
      When I click the "Next" link
      Then there is a game
      When I fill in the SSNM Tree
      When I click on Complete Activity
      Then I am on the Activity 13 page
      When I click on Complete Activity
      Then I am on the Activity 14 page
      
      # reasons to stay healthy
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 15 page
      When I click on Complete Activity
      Then I am on the Session 1 page

      ## SESSION2
      When I click on Session 2
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      When I click on Complete Activity
      Then I am on the Activity 4 page
      When I click on Complete Activity
      Then I am on the Activity 5 page
      When I click on Complete Activity
      Then I am on the Activity 6 page
      When I click on Complete Activity
      Then I am on the Activity 7 page
      # island game
      When I click the "Next" link
      Then there is a game
      When I click the "Next" link
      Then I am on the Activity 8 page
      # watch video
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 9 page
      # island game part 2
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 10 page
      When I click on Complete Activity
      Then I am on the Activity 11 page
      # reasons to stay healthy
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 12 page
      When I click on Complete Activity
      Then I am on the Session 2 page

      ## SESSION 3
      When I click on Session 3
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      # Pill Regimen
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 4 page
      When I click on Complete Activity
      Then I am on the Activity 5 page
      # Watch Video
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 6 page
      When I click on Complete Activity
      Then I am on the Activity 7 page
      When I click on Complete Activity
      Then I am on the Activity 8 page
      When I click on Complete Activity
      Then I am on the Activity 9 page
      When I click on Complete Activity
      Then I am on the Activity 10 page
      # Reasons To Stay Healthy
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 11 page
      When I click on Complete Activity
      Then I am on the Session 3 page

      ## SESSION 4
      When I click on Session 4
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      
      # pill game
      When I click the "Next" link
      Then there is a game
      When I click the "Next" link
      Then I am on the Activity 4 page
      
      # barrier game
      When I click the "Next" link
      Then there is a game
      When I select the first barrier
      When I click on Complete Activity

      Then I am on the Activity 5 page
      When I click on Complete Activity
      Then I am on the Activity 6 page
      When I click on Complete Activity
      Then I am on the Activity 7 page
      When I click on Complete Activity
      Then I am on the Session 4 page

      # defaulter sessions
      When I click on Session 5
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      When I click on Complete Activity
      Then I am on the Activity 3 page
      # quiz - assessment
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 4 page
      
      # quiz - assessment audit
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 5 page
      
      # quiz - drugs
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 6 page
      
      # island game
      When I click on Complete Activity
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 7 page
      
      # island game part 2
      When I click on Complete Activity
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 8 page
      When I click on Complete Activity
      Then I am on the Activity 9 page
      
      # tree
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 10 page
      When I click on Complete Activity
      Then I am on the Activity 11 page

      # tree
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 12 page
      
      # pill game
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 13 page
      
      # barrier game - no need to select something
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 14 page
      When I click on Complete Activity
      Then I am on the Activity 15 page
      When I click on Complete Activity
      Then I am on the Activity 16 page

      # barrier game redux - no need to select something
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 17 page

      # reasons to stay healthy redux
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Session 5 page
      
      ## SESSION 6
      When I click on Session 6
      When I click on Activity 1
      Then I am on the Activity 1 page
      When I click on Complete Activity
      Then I am on the Activity 2 page
      
      # reasons to stay healhty
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 3 page
      
      # barrier game redux - no need to select something
      When I click the "Next" link
      Then there is a game
      When I click on Complete Activity
      Then I am on the Activity 4 page
      
      When I click on Complete Activity
      Then I am on the Session 6 page

      Finished using selenium
