import unittest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        pid = 'collective.ploneboard'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(
            pid in installed,
            'package %s appears not to have been installed' % pid
        )

    def test_dexterity_is_installed(self):
        pid = 'plone.app.dexterity'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(
            pid in installed,
            'package %s appears not to have been installed' % pid
        )

    def test_discussion_is_globally_allowed(self):
        from zope.component import queryUtility
        from plone.registry.interfaces import IRegistry
        from plone.app.discussion.interfaces import IDiscussionSettings
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        self.assertEqual(settings.globally_enabled, True)

    def test_image_resource_registered(self):
        self.portal.restrictedTraverse(
            '++resource++collective.ploneboard/images/ploneboard.gif'
        )

    def test_stylesheets_resource_registered(self):
        self.portal.restrictedTraverse(
            '++resource++collective.ploneboard/stylesheets/ploneboard.css'
        )


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.ploneboard'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.ploneboard is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.ploneboard'))

    def test_browserlayer_removed(self):
        """Test that ICollectivePloneboard is removed."""
        from collective.ploneboard.interfaces import \
            ICollectivePloneboardLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectivePloneboardLayer,
            utils.registered_layers())
