import unittest
from datetime import datetime

from zope.component import getMultiAdapter
from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.discussion.interfaces import IConversation

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.ploneboard.interfaces import ITopic
from collective.ploneboard.testing import (
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING
)


class TopicIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Topic'
        )
        schema = fti.lookupSchema()
        self.assertEquals(ITopic, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Topic'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ITopic.providedBy(new_object))

    def test_global_allow_not_allowed(self):
        self.assertRaises(
            ValueError,
            self.portal.invokeFactory,
            'Topic',
            'my-topic',
        )

    def test_adding(self):
        self.portal.invokeFactory(
            'Message Board',
            'board'
        )
        self.portal.board.invokeFactory(
            'Topic',
            'mytopic'
        )
        obj = self.portal.board['mytopic']
        self.failUnless(ITopic.providedBy(obj))


class TopicViewIntegrationTest(unittest.TestCase):

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
        board = self.portal['board']
        board.invokeFactory('Topic', id='topic1', title='Topic 1')
        self.topic = board.topic1

    def test_messageboard_view(self):
        view = getMultiAdapter(
            (self.topic, self.portal.REQUEST),
            name="view"
        )
        view = view.__of__(self.topic)
        self.assertTrue(view())
        self.assertTrue(view.template.filename.endswith('topic.pt'))
        self.assertTrue('Topic 1' in view())

    def test_conversations_method(self):
        self.topic.invokeFactory(
            'Conversation',
            id='conv1',
            title='Conversation 1'
        )
        conversation = IConversation(self.topic.conv1)
        comment1 = createObject('plone.Comment')
        comment1.creation_date = datetime.utcnow()
        comment1.author_name = u'John Doe'
        conversation.addComment(comment1)
        comment2 = createObject('plone.Comment')
        comment2.creation_date = datetime.utcnow()
        comment2.author_name = u'Jane Doe'
        conversation.addComment(comment2)
        from collective.ploneboard.browser.topic import TopicView
        view = TopicView(self.topic, self.request)

        conversations = view.conversations()

        self.assertEqual(len(conversations), 1)
        self.assertEqual(
            conversations,
            [
                {
                    'title': u'Conversation 1',
                    'url': 'http://nohost/plone/board/topic1/conv1',
                    'total_comments': 2,
                    'last_commenter': u'Jane Doe',
                    'last_comment_date': conversation.last_comment_date,
                }
            ]
        )
