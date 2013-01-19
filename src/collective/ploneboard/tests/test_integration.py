# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
import unittest2 as unittest

from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


class PloneboardContenttypesIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    def test_add_ploneboard(self):
        """As an administrator I can add a message board.
        """
        self.browser.open(self.portal_url)
        self.browser.getLink('Message Board').click()
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My Message Board"
        self.browser.getControl(
            name='form.widgets.IBasic.description'
        ).value = "Lorem ipsum"
        self.browser.getControl("Save").click()
        self.assertTrue("My Message Board" in self.browser.contents)
        self.assertTrue("Lorem ipsum" in self.browser.contents)

    def test_add_topic(self):
        """As an administrator I can add a topic to an existing message board.
        """
        self.browser.open(self.portal_url + '/++add++messageboard')
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My Message Board"
        self.browser.getControl("Save").click()

        self.browser.open(self.portal_url + '/my-message-board')
        self.browser.getLink('Topic').click()
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My First Topic"
        self.browser.getControl(
            name='form.widgets.IBasic.description'
        ).value = "Lorem ipsum"
        self.browser.getControl("Save").click()

        self.assertTrue("My First Topic" in self.browser.contents)
        self.assertTrue("Lorem ipsum" in self.browser.contents)

    def test_add_conversation(self):
        """As a member I can add a conversation to an existing topic.
        """
        pass

    def test_add_reply(self):
        """As a member I can reply to an existing conversation.
        """
        pass
