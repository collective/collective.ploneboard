import unittest2 as unittest

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
