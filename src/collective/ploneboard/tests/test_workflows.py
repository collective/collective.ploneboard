import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from Products.CMFCore.utils import _checkPermission as checkPerm
from Products.CMFCore.permissions import View
from Products.CMFCore import permissions

# from AccessControl import Unauthorized
from Products.CMFCore.WorkflowCore import WorkflowException

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

    def test_permission(self):
        # As a member I can add new conversation
        workflowTool = getToolByName(self.portal, 'portal_workflow')
        workflowTool.setChainForPortalTypes(['topic'], 'try_topi_w')
        workflowTool.setChainForPortalTypes(
            ['conversation'],
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
        # Publish messageboard and topic
        workflowTool.doActionFor( self.portal.board , "publish")
        workflowTool.doActionFor( self.portal.board.topic , "publish")

        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser(
            'reviewer', 'secret', ['Reviewer'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.portal.acl_users._doAddUser('editor', ' secret', ['Editor'], [])
        self.portal.acl_users._doAddUser('reader', 'secret', ['Reader'], [])

        login(self.portal, 'member')
        self.portal.board.topic.invokeFactory(
            'conversation',
            'conv',
        )
        self.assertTrue('conv' in self.portal.board.topic.objectIds())


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

    def test_add_conversation_as_member(self):
        # As a member I can add new conversations
        # Publish messageboard and topic
        self.workflowTool.doActionFor(
            self.portal.board,
            "publish"
            )
        self.workflowTool.doActionFor(
            self.portal.board.topic,
            "publish"
            )
        # Member logs in
        login(self.portal, "member")
        self.portal.board.topic.invokeFactory(
            'conversation',
            'my_first_conversation',
        )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'my_second_conversation',
        )
        self.assertTrue('my_first_conversation' and 'my_second_conversation' in self.portal.board.topic.objectIds())

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
        self.portal.acl_users._doAddUser('anonymous', 'secret', [], [])
        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser(
            'reviewer', 'secret', ['Reviewer'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.portal.acl_users._doAddUser('editor', ' secret', ['Editor'], [])
        self.portal.acl_users._doAddUser('reader', 'secret', ['Reader'], [])

    def test_add_conversation_as_member(self):
        # As a member I can add new conversations
        # Publish messageboard and topic
        self.workflowTool.doActionFor(
            self.portal.board,
            "publish"
            )
        self.workflowTool.doActionFor(
            self.portal.board.topic,
            "publish"
            )
        # Member logs in
        login(self.portal, "member")
        self.portal.board.topic.invokeFactory(
            'conversation',
            'my_first_conversation',
        )
        self.portal.board.topic.invokeFactory(
            'conversation',
            'my_second_conversation',
        )
        self.assertTrue('my_first_conversation' and 'my_second_conversation' in self.portal.board.topic.objectIds())

    def test_initial_workflow_state(self):
        # Initial workflow state should be 'private'
        self.assertEqual(
            self.workflowTool.getInfoFor(
                self.portal.board.topic.conv,
                'review_state'
                ),
            'private'
            )

    def test_delete(self):
        mt = getToolByName(self.portal, 'portal_membership')
        self.assertTrue(mt.checkPermission(
            permissions.DeleteObjects,
            self.portal.board.topic.conv)
            )
        # Can delete
        self.portal.board.topic.manage_delObjects(["conv"])
        # Deleted
        self.assertFalse('conv' in self.portal.board.topic.objectIds())

    def test_delete_as_user(self):
        logout()
        # Members can not delete conversations
        login(self.portal, 'member')
        mt = getToolByName(self.portal, 'portal_membership')
        self.assertFalse(mt.checkPermission(
            permissions.DeleteObjects,
            self.portal.board.topic.conv)
            )

    def test_delete_as_anonymous(self):
        # Anonymous user can not delete conversation
        logout()
        login(self.portal, 'anonymous')
        mt = getToolByName(self.portal, 'portal_membership')
        self.assertFalse(mt.checkPermission(
            permissions.DeleteObjects,
            self.portal.board.topic.conv)
            )

    def test_submit(self):
        self.workflowTool.doActionFor(self.portal.board.topic.conv, "submit")
        # Workflow state should be 'pending'
        self.assertEqual(
            self.workflowTool.getInfoFor(
                self.portal.board.topic.conv,
                'review_state'
                ),
            'pending'
            )

    def test_publish(self):
        self.workflowTool.doActionFor(self.portal.board.topic.conv, "publish")
        # Workflow state should be 'published'
        self.assertEqual(
            self.workflowTool.getInfoFor(
                self.portal.board.topic.conv,
                'review_state'
                ),
            'published'
            )

    def test_publish_as_anonymous(self):
        logout()
        # self.workflowTool.doActionFor(self.portal.board.topic.conv,"publish")
        try:
            self.workflowTool.doActionFor(
                self.portal.board.topic.conv,
                "publish"
                )
        except WorkflowException:
                # Exception is raised
                pass
        # Workflow state should remain 'private'
        self.assertEqual(
            self.workflowTool.getInfoFor(
                self.portal.board.topic.conv,
                'review_state'
                ),
            'private'
            )
