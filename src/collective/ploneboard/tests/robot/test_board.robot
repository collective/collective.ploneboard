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
      When I add a topic within ploneboard
      Then a topic has been created

Scenario: Add Conversation within a Topic in Plone Board
    Given a logged in site administrator
      and the portal root
      When I add a conversation within topic within ploneboard
      Then a conversation has been created

*** Keywords ***

a logged in site administrator
  Enable autologin as  Site Administrator
  Go to  ${PLONE_URL}

the portal root
  Go to  ${PLONE_URL}

I add a message board
#  Click Link  css=#plone-contentmenu-factories a
  ${message_board_uid}  Create content  type=messageboard  id=my-message-board  title=My Message Board
#  Import library  DebugLibrary
#  Debug
#  Click Link  css=#plone-contentmenu-factories #message-board

I add a topic within ploneboard
  ${message_board_uid}  Create content  type=messageboard  id=my-message-board  title=My Message Board
  Go to  ${PLONE_URL}/my-message-board/view
  ${topic_uid}  Create content  type=topic  id=my-topic  title=My Topic  container=${message_board_uid}

I add a conversation within topic within ploneboard
  ${message_board_uid}  Create content  type=messageboard  id=my-message-board  title=My Message Board
  Go to  ${PLONE_URL}/my-message-board/view
  ${topic_uid}  Create content  type=topic  id=my-topic  title=My Topic  container=${message_board_uid}
  Go to  ${PLONE_URL}/my-message-board/my-topic/view
  ${conversation_uid}  Create content  type=conversation  id=my-conv  title=My Conv  container=${topic_uid}

a new message board has been created
  Go to  ${PLONE_URL}/my-message-board/view
  Wait until page contains  My Message Board

a topic has been created
  Go to  ${PLONE_URL}/my-message-board/my-topic/view
  Wait until page contains  My Topic

a conversation has been created
  Go to  ${PLONE_URL}/my-message-board/my-topic/my-conv/view
  Wait until page contains  My Conv
