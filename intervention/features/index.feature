Feature: Rocking with lettuce and django

    Scenario: Index Page Load
        Given I access the url "/"
        Then I see the header "Welcome to Masivukeni!"

    Scenario: Index Page Load 2
        Given I access the url "/home.html"
        Then I see the header "Welcome to Masivukeni!"
