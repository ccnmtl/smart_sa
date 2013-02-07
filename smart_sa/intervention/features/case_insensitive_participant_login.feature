Feature: Case-Insensitive Participant Login

PMT #79572

    Scenario Outline: Case Variations
      Using selenium
      Given I am logged in as a counselor
      When I access the url "/"
      When I click the "Let's get started!" link
      When I click the "Counsel" link
      When I fill in "<username>" in the "name" form field
      When I fill in "<id_number>" in the "id_number" form field
      When I submit the "login-participant-form" form
      Then I am on the Intervention page
      Finished using selenium
      
     Examples:
        |username|id_number|
        |test    |test     |
        |test    |Test     |
        |Test    |test     |
        |Test    |Test     |
        |tEst    |tEst     |
        |teSt    |teSt     |
        |TEST    |TEST     |

