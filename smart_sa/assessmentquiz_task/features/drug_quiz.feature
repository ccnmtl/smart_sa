Feature: Drug Quiz    
    
    Scenario: Drug Audit
      
      Given I am a participant
      When I click on Session 1
      Then I click on Activity 12
      When I click the "Next →" link
      
      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz

      # fill out all the questions - alerts do not work in headless mode
      # When I click the "What is My Score?" link
      # Then I'm asked to answer all the questions
      
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
      
      