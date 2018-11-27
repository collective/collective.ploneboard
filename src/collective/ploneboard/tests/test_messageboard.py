import unittest

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
            name='Message Board'
        )
        schema = fti.lookupSchema()
        self.assertEquals(IMessageboard, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Message Board'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IMessageboard.providedBy(new_object))

    def test_adding(self):
        self.portal.invokeFactory(
            'Message Board',
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
            'Message Board',
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

    def test_topics_method_returns_topics(self):
        self.portal.board.invokeFactory('Topic', id='topic1', title='Topic 1')
        self.portal.board.invokeFactory('Topic', id='topic2', title='Topic 2')
        from collective.ploneboard.browser.messageboard import MessageboardView
        view = MessageboardView(self.portal.board, self.request)

        topics = view.topics()

        self.assertEqual(len(topics), 2)
        self.assertEqual(
            [x['title'] for x in topics],
            ['Topic 1', 'Topic 2']
        )

    def test_topics_method_returns_conversations(self):
        self.portal.board.invokeFactory('Topic', id='topic1', title='Topic 1')
        self.portal.board.topic1.invokeFactory(
            'Conversation',
            id='conv1',
            title='Conversation 1'
        )
        self.portal.board.topic1.invokeFactory(
            'Conversation',
            id='conv2',
            title='Conversation 2'
        )
        from collective.ploneboard.browser.messageboard import MessageboardView
        view = MessageboardView(self.portal.board, self.request)

        topics = view.topics()

        self.assertEqual(len(topics), 1)
        self.assertEqual(
            topics[0]['conversations'][0]['title'],
            'Conversation 1',
        )
        self.assertEqual(
            topics[0]['conversations'][0]['url'],
            'http://nohost/plone/board/topic1/conv1'
        )
        self.assertEqual(
            topics[0]['conversations'][1]['title'],
            'Conversation 2'
        )
        self.assertEqual(
            topics[0]['conversations'][1]['url'],
            'http://nohost/plone/board/topic1/conv2'
        )
