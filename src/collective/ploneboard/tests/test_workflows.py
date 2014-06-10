import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from Products.CMFCore.utils import _checkPermission as checkPerm
from Products.CMFCore.permissions import View

# from AccessControl import Unauthorized

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout

from collective.ploneboard.testing import (
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING
)


class WorkflowIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        workflowTool = getToolByName(self.portal, 'portal_workflow')
        workflowTool.setChainForPortalTypes(('topic',), 'try_topi_w')
        workflowTool.setChainForPortalTypes(
            ('conversation',),
            'try_conv_no_review_w'
            )
        workflowTool.updateRoleMappings()

    def test_workflow_installed(self):
        workflow = getToolByName(self.portal, 'portal_workflow')
        self.assertTrue('try_conv_w' in workflow)
        self.assertTrue('try_conv_no_review_w' in workflow)
        self.assertTrue('try_topi_w' in workflow)

    def test_topic_workflow_mapped(self):
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic',
        )
        workflow = getToolByName(self.portal.board.topic, 'portal_workflow')
        self.assertEqual(
            ('try_topi_w',),
            workflow.getChainFor(self.portal.board.topic)
            )

    def test_conv_workflow_mapped(self):
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic',
        )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv',
        )
        workflow = getToolByName(
            self.portal.board.topic.conv,
            'portal_workflow'
            )
        self.assertEqual(
            ('try_conv_no_review_w',),
            workflow.getChainFor(self.portal.board.topic.conv)
            )

    # XXX: Todo- test for adding conversation as a member
    """
    def test_permission(self):
        workflowTool = getToolByName(self.portal, 'portal_workflow')
        workflowTool.setChainForPortalTypes(('topic',), 'try_topi_w')
        workflowTool.setChainForPortalTypes(
            ('conversation',),
            'try_conv_no_review_w'
            )
        workflowTool.updateRoleMappings()
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic',
        )
        # setRoles(self.portal, TEST_USER_ID, ['Member','Authenticated'])
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])
        workflowTool.updateRoleMappings()
        login(self.portal, 'user1')
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getMemberById('user1')
        print member.getRolesInContext(self.portal.board.topic)

        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv',
        )
        logout()
    """

    def test_review_conversation_permission(self):
        # 'Review portal content'
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic',
        )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv',
        )
        setRoles(self.portal, TEST_USER_ID, ['Reviewer'])
        self.assertTrue(
            self.portal.portal_membership.checkPermission(
                'Review portal content',
                self.portal.board.topic.conv
                ),
            self.portal.board.topic.conv
            )
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.assertFalse(
            self.portal.portal_membership.checkPermission(
                'Review portal content',
                self.portal.board.topic.conv
                ),
            self.portal.board.topic.conv
            )


class ConversationNoReviewWorkflowTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflowTool = getToolByName(self.portal, 'portal_workflow')
        self.workflowTool.setChainForPortalTypes(['topic'], 'try_topi_w')
        self.workflowTool.setChainForPortalTypes(
            ['conversation'],
            'try_conv_no_review_w'
            )
        self.workflowTool.updateRoleMappings()
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic',
        )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv',
        )
        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser(
            'reviewer', 'secret', ['Reviewer'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.portal.acl_users._doAddUser('editor', ' secret', ['Editor'], [])
        self.portal.acl_users._doAddUser('reader', 'secret', ['Reader'], [])

    def test_initial_workflow_state(self):
        # Initial workflow state should be 'published'
        self.assertEqual(
            self.workflowTool.getInfoFor(
                self.portal.board.topic.conv,
                'review_state'
                ),
            'published'
            )

    def test_view_conversations(self):
        # Conversations published are viewed by everyone
        # Member is allowed
        login(self.portal, 'member')
        self.assertTrue(checkPerm(View, self.portal.board.topic.conv))
        # Reviewer is allowed
        login(self.portal, 'reviewer')
        self.assertTrue(checkPerm(View, self.portal.board.topic.conv))
        # Anonymous is allowed
        logout()
        self.assertTrue(checkPerm(View, self.portal.board.topic.conv))
        # Editor is allowed
        login(self.portal, 'editor')
        self.assertTrue(checkPerm(View, self.portal.board.topic.conv))
        # Reader is allowed
        login(self.portal, 'reader')
        self.assertTrue(checkPerm(View, self.portal.board.topic.conv))

"""
class ConversationReviewWorkflowTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.workflowTool = getToolByName(self.portal, 'portal_workflow')
        self.workflowTool.setChainForPortalTypes(['topic'], 'try_topi_w')
        self.workflowTool.setChainForPortalTypes(
            ['conversation'],
            'try_conv_w'
            )
        self.workflowTool.updateRoleMappings()
        self.portal.invokeFactory(
            'messageboard',
            'board',
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic',
        )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv',
        )
        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser(
            'reviewer', 'secret', ['Reviewer'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.portal.acl_users._doAddUser('editor', ' secret', ['Editor'], [])
        self.portal.acl_users._doAddUser('reader', 'secret', ['Reader'], [])

    def test_delete(self):

        self.portal.REQUEST.form['conv'] = self.portal.board.topic.conv
        view = self.portal.board.topic.conv.restrictedTraverse(
            '@@moderate-delete-conversation'
            )
        view()
        # del self.portal.board.topic['conv']
        self.assertFalse('conv' in self.portal.board.topic.objectIds())

    def test_delete_as_anonymous(self):
        logout();
        del self.portal.board.topic['conv']
        #self.assertRaises(Unauthorized)
        self.assertTrue('conv' in self.portal.board.topic.objectIds())

    def test_delete_as_user(self):
        # Members can not delete conversations
        logout();
        #setRoles(self.portal, TEST_USER_ID, ['Member'])
        #del self.portal.board.topic['conv']
        #self.assertRaises(Unauthorized)
        #self.assertTrue('conv' in self.portal.board.topic.objectIds())
"""
