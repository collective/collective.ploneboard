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
        self.board.category = "Get Started\r\nPromotion\r\nCommunications"

    def test_messageboard_view(self):
        view = getMultiAdapter(
            (self.board, self.portal.REQUEST),
            name="view"
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())
        self.assertTrue(view.template.filename.endswith('messageboard.pt'))
        self.assertTrue('My Message Board' in view())
        self.assertTrue('Get Started' in view())
        self.assertTrue('Promotion' in view())
        self.assertTrue('Communications' in view())

    def test_categories_method_returns_categories(self):
        self.portal.board.invokeFactory(
            'topic',
            id='topic1',
            title='Topic 1',
            description="testing",
            category=[u'Get Started'])
        self.portal.board.invokeFactory(
            'topic',
            id='topic2',
            title='Topic 2',
            description="testing",
            category=[u'Get Started', u'Promotion'])
        view = getMultiAdapter(
            (self.portal.board, self.request),
            name="view"
            )
        view = view.__of__(self.portal.board)
        view()
        topics = view.categories()
        self.assertTrue(u'Promotion' in topics)
        self.assertTrue(u'Get Started' in topics)

    def test_categories_method_returns_topics(self):
        self.portal.board.invokeFactory(
            'topic',
            id='topic1',
            title='Topic 1',
            description="testing",
            category=[u'Get Started'])
        self.portal.board.invokeFactory(
            'topic',
            id='topic2',
            title='Topic 2',
            description="testing",
            category=[u'Get Started', u'Promotion'])
        view = getMultiAdapter(
            (self.portal.board, self.request),
            name="view"
            )
        view = view.__of__(self.portal.board)
        view()
        topics = view.categories()
        self.assertEqual(len(topics[u'Get Started']), 2)
        self.assertEqual(len(topics[u'Promotion']), 1)

    def test_unspecified_category_for_topic(self):
        self.portal.board.invokeFactory(
            'topic',
            id='topic1',
            title='Topic 1',
            description="testing",
            category=[])
        view = getMultiAdapter(
            (self.portal.board, self.request),
            name="view"
            )
        view = view.__of__(self.portal.board)
        view()
        topics = view.categories()
        self.assertTrue(u'Unspecified' in topics)

    def test_direct_conversations(self):
        self.portal.board.invokeFactory(
            'conversation',
            id='conv1',
            title='Conversation1',)
        view = getMultiAdapter(
            (self.portal.board, self.request),
            name="view"
            )
        view = view.__of__(self.portal.board)
        view()
        convs = view.direct_conversations()
        self.assertEqual(convs[0]['title'], 'Conversation1')
