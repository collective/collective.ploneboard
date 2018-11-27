from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI
import unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.ploneboard.interfaces import IConversation
from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


class ConversationIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Conversation'
        )
        schema = fti.lookupSchema()
        self.assertEquals(IConversation, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Conversation'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IConversation.providedBy(new_object))

    def test_global_allow_not_allowed(self):
        self.assertRaises(
            ValueError,
            self.portal.invokeFactory,
            'Conversation',
            'my-conversation',
        )

    def test_adding(self):
        self.portal.invokeFactory(
            'Message Board',
            id='board'
        )
        self.portal.board.invokeFactory(
            'Topic',
            id='topic'
        )
        self.portal.board.topic.invokeFactory(
            'Conversation',
            id='conversation'
        )

        obj = self.portal.board.topic['conversation']
        self.failUnless(IConversation.providedBy(obj))

    def test_conversation_enabled(self):
        from plone.app.discussion.interfaces import IDiscussionLayer
        from zope.interface import alsoProvides
        alsoProvides(
            self.portal.REQUEST,
            IDiscussionLayer
        )

        self.portal.invokeFactory(
            'Message Board',
            'board'
        )
        self.portal.board.invokeFactory(
            'Topic',
            'topic'
        )
        self.portal.board.topic.invokeFactory(
            'Conversation',
            'conversation'
        )
        obj = self.portal.board.topic['conversation']
        conv = obj.restrictedTraverse('@@conversation_view')
        self.assertTrue(conv.enabled())

    def test_comment_download(self):
        self.portal.invokeFactory(
            'Message Board',
            'board'
        )
        self.portal.board.invokeFactory(
            'Topic',
            'topic'
        )
        self.portal.board.topic.invokeFactory(
            'Conversation',
            'conv'
        )

# XXX: Todo
#        conv = self.portal.board.topic.conv.restrictedTraverse(
#            '@@conversation_view')
#        comment = createObject('plone.Comment')
#        comment.text = u'text'
#        #comment.attachment = NamedBlobImage()
#        conv.addComment(comment)
#        comment.restrictedTraverse('/@@download/attachment/Foto.JPG')
