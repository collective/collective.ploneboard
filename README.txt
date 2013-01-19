.. contents::

Introduction
============

This is an experimental Plone add-on product to rewrite the functionality
of Products.Ploneboard from the scratch with Dexterity types and
plone.app.discussion.

User Stories
============

Add Ploneboard
--------------

As an administrator I can add a message board.

- Go to portal root
- Click "Message Board" on add-menu
- Fill out "title" and "description"

Add Topic
---------

As an administrator I can add a topic to an existing message board.

- Add Ploneboard
- Click "Topic" in add-menu

Add Conversation
----------------

As a member I can add a conversation to an existing topic.

- Add Ploneboard
- Add Topic
- Click "Add conversation" Button
- Fill out "title" and "text"
- Click "post comment"

Reply to a comment
------------------

As a member I can add a reply to an existing conversation.

- Add Ploneboard
- Add Topic
- Add Conversation
- Go to conversation
- Fill out text
- Click on "post comment"

Message board view
------------------

- As an anonymous user I can view all topics of a message board.
- As an anonymous user I can view the latest 5 conversations of a topic.

Topic view
----------

- As a member I can view all conversations of a topic.

Conversation view
-----------------

- As a member I can view all posts of a conversation.


Later
-----

- As a member I can attach a file to my comments/replies.
- As a member I can search a message board.

