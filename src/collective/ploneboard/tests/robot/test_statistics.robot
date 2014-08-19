*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Scenario: Statistics
    Given a logged in site administrator
      and the portal root
      When I make a ploneboard
      Then I can see statistics

*** Keywords ***

a logged in site administrator
  Enable autologin as  Site Administrator
  Go to  ${PLONE_URL}

the portal root
  Go to  ${PLONE_URL}

#  Import library  DebugLibrary
#  Debug
I make a ploneboard
  ${message_board_uid}  Create content  type=messageboard  id=my-message-board  title=My Message Board
  Go to  ${PLONE_URL}/my-message-board/view
  ${topic_uid}  Create content  type=topic  id=my-topic  title=My Topic  container=${message_board_uid}
  Go to  ${PLONE_URL}/my-message-board/my-topic/view
  ${conversation_uid}  Create content  type=conversation  id=my-conv  title=My Conv  container=${topic_uid}
  Go to  ${PLONE_URL}/my-message-board/my-topic/my-conv/view
#  Import library  DebugLibrary
#  Debug

I can see statistics
  Go to  ${PLONE_URL}/my-message-board/view
  Wait until page contains  My Message Board
  Click link  id=stat_button
  Wait until page contains  Topics
  Wait until page contains  Conversations
  Wait until page contains  Comments
  Wait until page contains  Users
  Wait until page contains  Comments Today
