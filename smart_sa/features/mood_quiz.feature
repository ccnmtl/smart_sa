Feature: Mood Quiz

    Scenario: Mood
      Given I am a participant
      Given I clear the privacy notice

      When I click on Session 1
      Then I click on Activity 10
      When I click the "Next →" link

      # assessment quiz part 1 - mood
      Then there is a game
      Then there is an assessmentquiz

      # fill out all the questions - alerts do not work in headless mode
      # When I click the "What is My Score?" link
      # Then I'm asked to answer all the questions

      # no distress
      When I fill in all 1s in the quiz
      When I click the "What is My Score?" link
      Then my score says "no significant distress"

      # state saved
      When I click the "Next →" link
      When I click the "← Back" link
      Then my score says "no significant distress"
      
      # mild distress
      When I fill in all 2s in the quiz
      When I click the "What is My Score?" link
      Then my score says "Mild distress"
      
      # moderate distress
      When I answer 3 for question 1
      When I answer 3 for question 2
      When I answer 3 for question 3
      When I answer 3 for question 4
      When I answer 3 for question 5
      When I click the "What is My Score?" link
      Then my score says "Moderate distress"
      
      # severe distress
      When I fill in all 3s in the quiz
      When I click the "What is My Score?" link
      Then my score says "Severe distress" 


    Scenario: Mood Defaulter - State is clear
      Given I am a participant
      Given I clear the privacy notice

      When I click on Session 1
      Then I click on Activity 10
      When I click the "Next →" link
      
      # assessment quiz non defaulter - mood
      Then there is a game
      Then there is an assessmentquiz
      When I fill in all 1s in the quiz
      When I click the "What is My Score?" link
      Then my score says "no significant distress"

      # defaulter session
      When I click the "Sessions" link
      When I click on Session 4
      Then I click on Activity 3
      When I click the "Next →" link
      
      # assessment quiz defaulter - mood
      Then there is a game
      Then there is an assessmentquiz
