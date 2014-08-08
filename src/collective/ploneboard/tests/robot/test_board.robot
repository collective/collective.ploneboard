*** Settings ***

#Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Scenario: Add Plone Board
    Given a logged in site administrator
      and the portal root
     When I add a message board
     Then a new message board has been created

Scenario: Add Topic within Plone Board
    Given a logged in site administrator
      and the portal root
      When I add a message board
      and I add a topic
      Then a topic has been created


Scenario: Add Conversation within a Topic in Plone Board
    Given a logged in site administrator
      and the portal root
      When I add a message board
      and I add a topic
      and I add a conversation
      Then a conversation has been created

*** Keywords ***

a logged in site administrator
  Enable autologin as  Site Administrator
  Go to  ${PLONE_URL}

the portal root
  Go to  ${PLONE_URL}

I add a message board
#  Click Link  css=#plone-contentmenu-factories a
  Create content  type=messageboard  id=my-message-board  title=My Message Board
#  Import library  DebugLibrary
#  Debug
#  Click Link  css=#plone-contentmenu-factories #message-board

I add a topic
  Go to  ${PLONE_URL}/my-message-board/view
  Wait until page contains  My Message Board
  Go to  ${PLONE_URL}/my-message-board/++add++topic
  Input text  name=form.widgets.IBasic.title  My Topic
  Click Button  Save

I add a conversation
  Go to  ${PLONE_URL}/my-message-board/view
  Wait until page contains  My Message Board
  Go to  ${PLONE_URL}/my-message-board/++add++topic
  Input text  name=form.widgets.IBasic.title  My Topic
  Click Button  Save
  Go to  ${PLONE_URL}/my-message-board/my-topic/++add++conversation
  Input text  name=form.widgets.IBasic.title  My Conversation
#  Import library  DebugLibrary
#  Debug
#  Input text  name=form.widgets.text  Text in my conversation
#  Click Button  Save

a new message board has been created
  Go to  ${PLONE_URL}/my-message-board/view
  Wait until page contains  My Message Board

a topic has been created
  Go to  ${PLONE_URL}/my-message-board/my-topic/view
  Wait until page contains  My Topic

a conversation has been created
  Go to  ${PLONE_URL}/my-message-board/my-topic/my-conversation/view
  Wait until page contains  My Conversation
