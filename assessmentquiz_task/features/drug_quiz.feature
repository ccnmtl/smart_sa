Feature: Drug Quiz    
    
    Scenario: Drug Audit
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Counsel" link
      When I fill in "test" in the "name" form field
      When I fill in "test" in the "id_number" form field
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      When I click on Session 1
      Then I click on Activity 12
      When I click the "Next →" link
      
      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz

      # fill out all the questions      
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      
      # No issues
      When I fill in all 0s in the quiz
      When I click the "What is My Score?" link
      Then my score says "no issues"
      
      # Respondent screens positive if response to question 1 or 2 is greater than 2,
      When I fill in all 0s in the quiz
      When I answer 3 for question 1
      When I click the "What is My Score?" link
      Then my score says "serious problems"
      
      When I fill in all 0s in the quiz
      When I answer 3 for question 2
      When I click the "What is My Score?" link
      Then my score says "serious problems"
      
      # OR Respondent screens positive if question 3 or 4 greater than 0.
      When I fill in all 0s in the quiz
      When I answer 1 for question 3
      When I click the "What is My Score?" link
      Then my score says "serious problems"
      
      When I fill in all 0s in the quiz
      When I answer 1 for question 4
      When I click the "What is My Score?" link
      Then my score says "serious problems"
      
      # Just generally serious 
      When I fill in all 3s in the quiz
      When I click the "What is My Score?" link
      Then my score says "serious problems"
      
      Finished using selenium