from zope.component import createObject
from zope.component import queryUtility
from zope.component import getMultiAdapter
from plone.dexterity.interfaces import IDexterityFTI
import unittest2 as unittest
from datetime import datetime
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
# from plone.namedfile import NamedBlobImage

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
            name='conversation'
            )
        schema = fti.lookupSchema()
        self.assertEquals(IConversation, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='conversation'
            )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IConversation.providedBy(new_object))

    def test_global_allow_not_allowed(self):
        self.assertRaises(
            ValueError,
            self.portal.invokeFactory,
            'conversation',
            'my-conversation',
            )

    def test_adding(self):
        self.portal.invokeFactory(
            'messageboard',
            'board'
            )
        self.portal.board.invokeFactory(
            'topic',
            'topic'
            )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conversation'
            )
        obj = self.portal.board.topic['conversation']
        self.failUnless(IConversation.providedBy(obj))

    def test_permission_for_manager(self):
        self.portal.invokeFactory(
            'messageboard',
            'board'
            )
        self.portal.board.invokeFactory(
            'topic',
            'topic'
            )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conversation'
            )
        permissions = [
            p['name'] for p in
            self.portal.board.topic.permissionsOfRole('Manager')
            if p['selected']]
        self.assertTrue(
            'Collective Ploneboard: Add Conversation'
            in permissions)

    def test_conversation_enabled(self):
        from plone.app.discussion.interfaces import IDiscussionLayer
        from zope.interface import alsoProvides
        alsoProvides(
            self.portal.REQUEST,
            IDiscussionLayer
            )

        self.portal.invokeFactory(
            'messageboard',
            'board'
            )
        self.portal.board.invokeFactory(
            'topic',
            'topic'
            )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conversation'
            )
        obj = self.portal.board.topic['conversation']
        conv = obj.restrictedTraverse('@@conversation_view')
        self.assertTrue(conv.enabled())

# XXX: Todo Repair the attachment problem
"""
    def test_comment_download(self):
        self.portal.invokeFactory(
            'messageboard',
            'board'
            )
        self.portal.board.invokeFactory(
            'topic',
            'topic'
            )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv'
            )
        from plone.app.discussion.interfaces import IConversation
        conversation = IConversation(self.portal.board.topic.conv)
        comment = createObject('plone.Comment')
        comment.text = u'Text goes here'
        comment.attachment = NamedBlobImage('image.png')
        conversation.addComment(comment)
        downloadurl = comment.restrictedTraverse(
            '@@download/attachment/image.png'
            )
        print downloadurl
"""
# XXX: Todo
#        conv = self.portal.board.topic.conv.restrictedTraverse(
#            '@@conversation_view')
#        comment = createObject('plone.Comment')
#        comment.text = u'text'
#        #comment.attachment = NamedBlobImage()
#        conv.addComment(comment)
#        comment.restrictedTraverse('/@@download/attachment/Foto.JPG')


class ConversationViewIntegrationTest(unittest.TestCase):

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
        board = self.portal['board']
        board.invokeFactory('topic', id='topic1', title='Topic 1')
        board.topic1.invokeFactory(
            'conversation',
            id='conv',
            title='Conversation 1'
            )
        self.conv = board.topic1.conv

    def test_conversation_view(self):
        view = getMultiAdapter(
            (
                self.conv, self.portal.REQUEST), name="view"
            )
        view = view.__of__(self.conv)
        self.assertTrue(view())
        self.assertTrue('Conversation 1' in view())

    def test_comments_view(self):
        from plone.app.discussion.interfaces import IConversation
        conversation = IConversation(self.conv)
        comment1 = createObject('plone.Comment')
        comment1.text = "First Comment"
        comment1.creation_date = datetime.now()
        comment1.author_name = u'John Snow'
        conversation.addComment(comment1)
        comment2 = createObject('plone.Comment')
        comment2.text = "Second Comment"
        comment2.creation_date = datetime.now()
        comment2.author_name = u'Tyrion Lannister'
        conversation.addComment(comment2)
        view = getMultiAdapter(
            (
                self.conv, self.portal.REQUEST), name="view"
            )
        view = view.__of__(self.conv)
        lastmodified = comment2.creation_date.strftime("%b %d, %Y %I:%M %p")
        self.assertTrue(lastmodified in view())
