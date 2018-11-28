.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.ploneboard
==============================================================================

.. image:: https://travis-ci.org/kitconcept/collective.ploneboard.svg?branch=master
    :target: https://travis-ci.org/kitconcept/collective.ploneboard

.. image:: https://img.shields.io/pypi/status/collective.ploneboard.svg
    :target: https://pypi.python.org/pypi/collective.ploneboard/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/v/collective.ploneboard.svg
    :target: https://pypi.python.org/pypi/collective.ploneboard
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/collective.ploneboard.svg
    :target: https://pypi.python.org/pypi/collective.ploneboard
    :alt: License

|

.. image:: https://raw.githubusercontent.com/collective/collective.ploneboard/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

This is an experimental Plone add-on product to rewrite the functionality
of Products.Ploneboard from the scratch with Dexterity types and
plone.app.discussion.

Features
--------

- Add message board
- Add Topic
- Add conversation
- Reply to a conversation
- Add an attachment to a conversation


Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install collective.ploneboard by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.ploneboard


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.ploneboard/issues
- Source Code: https://github.com/collective/collective.ploneboard
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues,
`please let us know <https://github.com/collective/collective.ploneboard/issues>`_.

If you require professional support, or want to sponsor new features, feel free to drop us a note at info@kitconcept.com.


License
-------

The project is licensed under the GPLv2.


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

  >>> browser.open(portal_url + '/++add++Message Board')
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
