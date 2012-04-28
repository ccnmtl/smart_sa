Feature: Alcohol Quiz

    Scenario: Alcohol Audit
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
      Then I click on Activity 11
      When I click the "Next →" link
      
      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz

      # fill out all the questions      
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      
      # fill out 1, 9, 10
      When I answer 0 for question 1
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      When I answer 0 for question 9
      When I answer 0 for question 10
      When I click the "What is My Score?" link
      Then my score says "no issues"
      
      # fill out question #1 at a higher level
      When I answer 1 for question 1
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      When I answer 0 for question 2
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      When I answer 0 for question 3 
      When I click the "What is My Score?" link
      Then my score says "no issues"
      
      # fill out questions #2/#3 at a higher level
      When I answer 0 for question 2 
      When I answer 1 for question 3 
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      
      When I answer 1 for question 2 
      When I answer 0 for question 3 
      When I click the "What is My Score?" link
      Then I'm asked to answer all the questions
      
      # fill out the remaining questions
      When I answer 0 for question 4
      When I answer 0 for question 5
      When I answer 0 for question 6
      When I answer 0 for question 7
      When I answer 0 for question 8
      When I click the "What is My Score?" link
      Then my score says "no issues"
      
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