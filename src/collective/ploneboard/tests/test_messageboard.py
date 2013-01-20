import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility
from zope.component import getMultiAdapter

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.ploneboard.interfaces import IMessageboard
from collective.ploneboard.testing import (
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING
)


class MessageBoardIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='messageboard'
        )
        schema = fti.lookupSchema()
        self.assertEquals(IMessageboard, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='messageboard'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IMessageboard.providedBy(new_object))

    def test_adding(self):
        self.portal.invokeFactory(
            'messageboard',
            'board')
        board = self.portal['board']
        self.failUnless(IMessageboard.providedBy(board))


class MessageBoardViewIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.board = self.portal['board']
        self.board.title = "My Message Board"

    def test_messageboard_view(self):
        view = getMultiAdapter(
            (self.board, self.portal.REQUEST),
            name="view"
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())
        self.assertTrue(view.template.filename.endswith('messageboard.pt'))
        self.assertTrue('My Message Board' in view())
