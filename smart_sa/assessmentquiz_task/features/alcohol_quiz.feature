Feature: Alcohol Quiz

    Scenario: Alcohol Audit
      Using selenium
      Given I am a participant
      When I click on Session 1
      Then I click on Activity 11
      When I click the "Next →" link
      
      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz
      
      # fill out 1, 9, 10
      When I answer 0 for question 1
      When I answer 0 for question 9
      When I answer 0 for question 10
      When I click the "What is My Score?" link
      Then my score says "no issues"
      
      # fill out question #1 at a higher level
      When I answer 1 for question 1
      When I answer 0 for question 2
      When I answer 0 for question 3 
      When I click the "What is My Score?" link
      Then my score says "no issues"
      
      # fill out questions #2/#3 at a higher level
      When I answer 0 for question 2 
      When I answer 1 for question 3 
      
      When I answer 1 for question 2 
      When I answer 0 for question 3 
      
      # fill out the remaining questions
      When I answer 0 for question 4
      When I answer 0 for question 5
      When I answer 0 for question 6
      When I answer 0 for question 7
      When I answer 0 for question 8
      
      # mild
      When I fill in all 1s in the quiz
      When I click the "What is My Score?" link
      Then my score says "Mild drinking issues"
      
      # moderate
      When I answer 2 for question 8
      When I answer 4 for question 9
      When I answer 4 for question 10
      When I click the "What is My Score?" link
      Then my score says "Moderate drinking issues"
      
      # severe
      When I fill in all 2s in the quiz
      When I click the "What is My Score?" link
      Then my score says "Severe drinking issues"

      Finished using selenium