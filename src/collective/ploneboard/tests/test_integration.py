# -*- coding: utf-8 -*-
import os
import transaction

import unittest

from plone.testing.z2 import Browser

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


class PloneboardContenttypesFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    def tearDown(self):
        if 'board'in self.portal:
            self.portal.manage_delObjects(['board'])
            transaction.commit()

    def test_messageboard(self):
        self.browser.open(self.portal_url + '/++add++Message Board')
        self.browser.getControl(
            name='form.widgets.IDublinCore.title'
        ).value = "My Message Board"
        self.browser.getControl("Save").click()
        self.assertTrue("My Message Board" in self.browser.contents)

    def test_topic(self):
        self.portal.invokeFactory('Message Board', 'board')
        transaction.commit()

        self.browser.open(self.portal.board.absolute_url())
        self.browser.getLink('Topic').click()
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My First Topic"
        self.browser.getControl("Save").click()
        self.assertTrue("My First Topic" in self.browser.contents)

    def test_conversation(self):
        self.portal.invokeFactory('Message Board', 'board')
        self.portal.board.invokeFactory('Topic', 'topic')
        transaction.commit()

        self.browser.open(self.portal.board.topic.absolute_url())
        self.browser.getLink('Conversation').click()
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My First Conversation"
        self.browser.getControl(
            name='form.widgets.text'
        ).value = "This is my first conversation"
        self.browser.getControl("Save").click()
        self.assertTrue("My First Conversation" in self.browser.contents)

    def test_reply(self):
        self.portal.invokeFactory('Message Board', 'board')
        self.portal.board.invokeFactory('Topic', 'topic')
        self.portal.board.topic.invokeFactory('Conversation', 'conv')
        transaction.commit()

        self.browser.open(self.portal.board.topic.conv.absolute_url())
        self.browser.getControl(
            name='form.widgets.text'
        ).value = "This is my first reply."
        self.browser.getControl(name="form.buttons.comment").click()
        self.assertTrue("This is my first reply" in self.browser.contents)

    def test_conversation_attachment(self):
        self.portal.invokeFactory('Message Board', 'board')
        self.portal.board.invokeFactory('Topic', 'topic')
        self.portal.board.topic.invokeFactory('Conversation', 'conv')
        transaction.commit()

        self.browser.open(self.portal.board.topic.conv.absolute_url())
        self.browser.getControl(name='form.widgets.text')\
            .value = "This is my first comment."
        image_path = os.path.join(os.path.dirname(__file__), "image.png")
        image_ctl = self.browser.getControl(name='form.widgets.attachment')
        image_ctl.add_file(open(image_path), 'image/png', 'image.png')
        self.browser.getControl(name='form.buttons.comment').click()

        self.assertTrue('This is my first comment.' in self.browser.contents)
        self.assertTrue('image.png' in self.browser.contents)
