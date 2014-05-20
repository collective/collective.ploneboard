.. contents::

Introduction
============

.. image:: https://secure.travis-ci.org/collective/collective.ploneboard.png?branch=master

This is an experimental Plone add-on product to rewrite the functionality
of Products.Ploneboard from the scratch with Dexterity types and
plone.app.discussion.

https://travis-ci.org/tisto/collective.ploneboard.png?branch=master

Test Setup
----------

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic admin:secret')
    >>> portal = layer['portal']
    >>> portal_url = 'http://nohost/plone'


Add message board
-----------------

"As an administrator I can add a message board."

  >>> browser.open(portal_url + '/++add++messageboard')
  >>> browser.getControl(name='form.widgets.IDublinCore.title').value = "My Message Board"
  >>> browser.getControl("Save").click()
  >>> "My Message Board" in browser.contents
  True


Add Topic
---------

"As an administrator I can add a topic to an existing message board"

  >>> browser.open(portal_url + '/my-message-board')
  >>> browser.getLink('Topic').click()
  >>> browser.getControl(name='form.widgets.IBasic.title').value = "My First Topic"
  >>> browser.getControl("Save").click()
  >>> "My First Topic" in browser.contents
  True


Add Conversation
----------------

"As a member I can add a conversation to an existing topic."

  >>> browser.open(portal_url + '/my-message-board/my-first-topic')
  >>> browser.getLink('Conversation').click()
  >>> browser.getControl(name='form.widgets.IBasic.title').value = "My First Conversation"
  >>> browser.getControl(name='form.widgets.text').value = "This is my first conversation"
  >>> browser.getControl("Save").click()
  >>> "My First Conversation" in browser.contents
  True


Reply
-----

As a member I can add a reply to an existing conversation.

  >>> browser.getControl(name='form.widgets.text').value = "This is my first reply."
  >>> browser.getControl(name="form.buttons.comment").click()
  >>> "This is my first reply" in browser.contents
  True


Later
-----

As a member I can attach a file to my comments/replies.
As a member I can search a message board.

