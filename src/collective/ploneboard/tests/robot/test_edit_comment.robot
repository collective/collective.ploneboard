*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Scenario: Edit Comment
    Given a logged in site administrator
      and the portal root
      When I add a comment in a conversation
#     Then I can edit comment

*** Keywords ***

a logged in site administrator
  Enable autologin as  Site Administrator
  Go to  ${PLONE_URL}

the portal root
  Go to  ${PLONE_URL}

#  Click Link  css=#plone-contentmenu-factories a
#  Import library  DebugLibrary
#  Debug
#  Click Link  css=#plone-contentmenu-factories #message-board
I add a comment in a conversation
  ${message_board_uid}  Create content  type=messageboard  id=my-message-board  title=My Message Board
  Go to  ${PLONE_URL}/my-message-board/view
  ${topic_uid}  Create content  type=topic  id=my-topic  title=My Topic  container=${message_board_uid}
  Go to  ${PLONE_URL}/my-message-board/my-topic/view
  ${conversation_uid}  Create content  type=conversation  id=my-conv  title=My Conv  container=${topic_uid}
  Go to  ${PLONE_URL}/my-message-board/my-topic/my-conv/view
#  Import library  DebugLibrary
#  Debug
#  Wait until page contains element  id=form-widgets-comment-text
# Input Text  id=form-widgets-comment-text  This is a comment
#  Set field value  id=form-widgets-comment-text  HELLO
#  Click Button  Comment

I can edit comment
  Go to  ${PLONE_URL}/my-message-board/my-topic/my-conv/view
  Wait until page contains  My Conv
