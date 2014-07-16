*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Scenario: Add Plone Board
    Given a logged in site administrator
      and the portal root
     When I add a message board
     Then a new message board has been created


*** Keywords ***

a logged in site administrator
  Go to  ${PLONE_URL}
  Enable autologin as  Site Administrator

the portal root
  Go to  ${PLONE_URL}

I add a message board
  Go to  ${PLONE_URL}

a new message board has been created
  Page should contain  Item created
