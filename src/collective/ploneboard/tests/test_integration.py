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

    def test_integration(self):
        # Add board
        self.browser.open(self.portal_url + '/++add++messageboard')
        self.browser.getControl(
            name='form.widgets.IDublinCore.title'
        ).value = "My Message Board"
        self.browser.getControl("Save").click()
        self.assertTrue("My Message Board" in self.browser.contents)
        # Add topic
        self.browser.open(self.portal_url + '/my-message-board')
        self.browser.getLink('Topic').click()
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My First Topic"
        self.browser.getControl("Save").click()
        self.assertTrue("My First Topic" in self.browser.contents)
        # Add conversation
        self.browser.open(self.portal_url + '/my-message-board/my-first-topic')
        self.browser.getLink('Conversation').click()
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = "My First Conversation"
        self.browser.getControl(
            name='form.widgets.text'
        ).value = "This is my first conversation"
        self.browser.getControl("Save").click()
        self.assertTrue("My First Conversation" in self.browser.contents)
        # Add reply
        self.browser.getControl(
            name='form.widgets.text'
        ).value = "This is my first reply."
        self.browser.getControl(name="form.buttons.comment").click()
        self.assertTrue("This is my first reply" in self.browser.contents)
