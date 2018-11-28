import unittest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_installer

from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.installer = get_installer(self.portal, self.request)

    def test_product_is_installed(self):
        self.assertTrue(
            self.installer.is_product_installed('collective.ploneboard'),
            'package collective.ploneboard appears not to have been installed'
        )

    def test_dexterity_is_installed(self):
        self.assertTrue(
            self.installer.is_product_installed('plone.app.dexterity'),
            'package plone.app.dexterity appears not to have been installed'
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
        self.request = self.layer['request']
        self.installer = get_installer(self.portal, self.request)
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('collective.ploneboard')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.ploneboard is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'collective.ploneboard'))

    def test_browserlayer_removed(self):
        """Test that ICollectivePloneboard is removed."""
        from collective.ploneboard.interfaces import \
            ICollectivePloneboardLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectivePloneboardLayer,
            utils.registered_layers())
