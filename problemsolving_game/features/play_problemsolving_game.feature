Feature: Problem Solving Activity
    ## Notes
    ## Barrier is currently in Session 4, Activity 10
    ## Warning: User data is cleared between scenarios.  

    Scenario: Find activity
        Using selenium
        Given I am logged in as a counselor
        When I access the url "/"
        When I click the "Let's get started!" link
        When I click the "Intervene" link
        When I fill in "test" in the "name" form field
        When I fill in "test" in the "id_number" form field
        When I submit the "login-participant-form" form
        Then I am on the Intervention page
        
        When I click on Session 4
        When I click on Activity 10
        When I click the "Next" link
        Then there is a game
        
    Scenario: Test focus change
        Using selenium
        Then barrier 1 has "focus"  
        When I select barrier 3
        Then barrier 1 does not have "focus"
        Then barrier 3 has "focus"
      
    Scenario: Test Right/Left Navigation
        Using selenium
        When I select barrier 1
        Then barrier 1 has "focus"
        There there is no left arrow
        There there is a right arrow
        
        When I navigate "right"
        Then barrier 2 has "focus"
        There there is a left arrow
        There there is a right arrow
        
        When I navigate "left"
        Then barrier 1 has "focus"
        There there is no left arrow
        There there is a right arrow
        
        # Assuming 17 issues
        When I select barrier 17
        There there is a left arrow
        There there is no right arrow
              
    Scenario: Personal Challenge on, navigate, off
        Using selenium
        When I select barrier 1
        Then barrier 1 has "focus"
        There is no action plan button
        When I toggle personal challenge
        Then barrier 1 has "marked"
        Then there is a Make Plan button
        When I click the "Next" link
        When I click the "Back" link
        Then barrier 1 has "marked"
        Then there is a Make Plan button
        When I toggle personal challenge
        Then barrier 1 does not have "marked"
        
    Scenario: Action plan displayed, then toggled off
        Using selenium   
        When I select barrier 3
        Then barrier 3 has "focus"
        Then barrier 3 does not have "marked"
        There is no action plan button
        
        When I toggle personal challenge
        Then barrier 3 has "marked"
        Then there is a Make Plan button
        
        When I click the "Make Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        
        # Unmarking the barrier should close the form 
        When I toggle personal challenge
        Then there is no Action Plan form
        There there is an issue selector
        There there is a left arrow
        There there is a right arrow
        Then barrier 3 does not have "marked"
        
     Scenario: Action plan displayed, then closed through save
        Using selenium   
        When I select barrier 3
        Then barrier 3 has "focus"
        Then barrier 3 does not have "marked"
        There is no action plan button
        
        When I toggle personal challenge
        Then barrier 3 has "marked"
        Then there is a Make Plan button
        
        When I click the "Make Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        
        When I click the Save Plan button
        Then there is no Action Plan form
        There there is an issue selector
        There there is a left arrow
        There there is a right arrow
        Then barrier 3 has "marked"
        
    Scenario: Action Plan Complete, then toggled off while editing
        Using selenium
        Then barrier 3 has "focus"
        Then barrier 3 has "marked"
        Then there is a Make Plan button
        
        When I click the "Make Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        
        When I type "1" in "barriers"
        When I type "1" in "proposals"
        When I type "1" in "finalPlan"
        When I click the Save Plan button
        Then there is no Action Plan form
        Then barrier 3 has "complete"
        Then there is an Edit Plan button
        
        When I click the "Edit Plan" link
        Then there is an Action Plan form
        When I toggle personal challenge
        Then barrier 3 does not have "marked"
        Then there is no action plan button
        
        When I select barrier 1
        Then barrier 1 has "focus"
        Then barrier 1 does not have "marked"
        Then there is no action plan button
        
        When I toggle personal challenge
        Then barrier 1 has "marked"
        Then there is a Make Plan button
        
     Scenario: Testing out the archive
        Using selenium
        When I select barrier 3 
        Then barrier 3 has "focus"
        Then barrier 3 does not have "marked"
        
        # The data should still be around from the previous test
        When I toggle personal challenge
        Then barrier 3 has "complete"
        Then there is an Edit Plan button
        
        When I click the "Edit Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        Then "barriers" reads "1"
        Then "proposals" reads "1"
        Then "finalPlan" reads "1"
        
        # Update the data & save
        When I type "2" in "barriers"
        When I type "2" in "proposals"
        When I type "2" in "finalPlan"
        When I click the Save Plan button
        There there is no Action Plan form
        
        When I click the "Edit Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        Then "barriers" reads "12"
        Then "proposals" reads "12"
        Then "finalPlan" reads "12"
        When I click the Save Plan button
        There there is no Action Plan form
        There there is an issue selector
        There there is a left arrow
        There there is a right arrow
        
    Scenario: Testing out multiple barrier plan selection.
        Using selenium
        When I select barrier 1
        Then barrier 1 has "focus"
        Then barrier 1 has "marked"
        Then there is a Make Plan button
        
        When I click the "Make Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        
        When I type "abc" in "barriers"
        When I type "def" in "proposals"
        When I type "ghi" in "finalPlan"
        When I click the Save Plan button
        Then barrier 1 has "complete"
        Then there is an Edit Plan button
        
        When I select barrier 3
        Then barrier 3 has "focus"
        Then barrier 3 has "complete"
        Then there is an Edit Plan button
        
        When I click the "Edit Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        Then "barriers" reads "12"
        Then "proposals" reads "12"
        Then "finalPlan" reads "12"
        When I click the Save Plan button
        
        When I select barrier 1
        Then barrier 1 has "focus"
        Then barrier 1 has "complete"
        Then there is no Action Plan form
        There there is an issue selector
        There there is no left arrow
        There there is a right arrow
        Then there is an Edit Plan button
        
        When I click the "Edit Plan" link
        Then there is an Action Plan form
        There there is no issue selector
        There there is no left arrow
        There there is no right arrow
        Then "barriers" reads "abc"
        Then "proposals" reads "def"
        Then "finalPlan" reads "ghi"
        When I click the Save Plan button
        Then there is no Action Plan form
        
    Scenario: Testing "other" item behavior
        Using selenium
        # Assuming "other" barrier is #14. 
        When I select barrier 14
        Then barrier 14 has "focus"
        Then I can specify my issue
        
        When I toggle personal challenge
        Then barrier 14 has "marked"
        Then I specify my issue as "abc"
        
        When I select barrier 13
        Then barrier 13 has "focus"
        Then I cannot specify my issue
        When I select barrier 14
        Then barrier 14 has "focus"
        Then I can specify my issue
        My issue is "abc"
        
        When I toggle personal challenge
        Then barrier 14 does not have "marked"
        Then I can specify my issue
        
        When I toggle personal challenge
        Then barrier 14 has "marked"
        My issue is "abc"
        
        When I click the "Next" link
        When I click the "Back" link
        When I select barrier 14
        Then barrier 14 has "focus"
        Then barrier 14 has "marked"
        Then I can specify my issue
        My issue is "abc"
        
        
         
        