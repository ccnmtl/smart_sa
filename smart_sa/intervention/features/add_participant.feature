Feature: Add Participant

    Scenario: Try To Add Duplicate
      Using selenium
      Given I am logged in as an admin
      Given participant named "test" exists
      When I go to the Add Participant Page
      When I fill in "test" in the "name" form field
      When I fill in "test_id_number" in the "id_number" form field
      When I fill in "test_patient_id" in the "patient_id" form field
      When I save
      Then there is an error message
      Then the "name" field has the value "test"
      Then the "id_number" field has the value "test_id_number"
      Then the "patient_id" field has the value "test_patient_id"
      Finished using selenium

