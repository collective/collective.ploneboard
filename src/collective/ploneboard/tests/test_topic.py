from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI
import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.ploneboard.interfaces import ITopic
from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


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
            name='topic'
        )
        schema = fti.lookupSchema()
        self.assertEquals(ITopic, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='topic'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ITopic.providedBy(new_object))

    def test_global_allow_not_allowed(self):
        self.assertRaises(
            ValueError,
            self.portal.invokeFactory,
            'topic',
            'my-topic',
        )

    def test_adding(self):
        self.portal.invokeFactory(
            'messageboard',
            'board'
        )
        self.portal.board.invokeFactory(
            'topic',
            'mytopic'
        )
        obj = self.portal.board['mytopic']
        self.failUnless(ITopic.providedBy(obj))
