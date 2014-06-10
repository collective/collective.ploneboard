import unittest2 as unittest

from Products.CMFCore.utils import getToolByName


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
