*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Scenario: Add Plone Board
    Given a logged in site administrator
      and the portal root
     When I add a message board
#     Then a new message board has been created


*** Keywords ***

a logged in site administrator
  Enable autologin as  Site Administrator
  Go to  ${PLONE_URL}

the portal root
  Go to  ${PLONE_URL}

I add a message board
  Click Link  css=#plone-contentmenu-factories a
  Import library  DebugLibrary
  Debug
#  Click Link  css=#plone-contentmenu-factories #message-board


a new message board has been created
  Page should contain  Item created
