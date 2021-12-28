Feature: users
    Scenario: A user can log into the app
        Given I empty the "User" table

        And I create the following users:
        | username | email          | password1  | password2 |
        | sumi     | sumi@gmail.com | python123  | python123 |

        When I log in with email "sumi@gmail.com" and password "python123"

        Then I am logged in