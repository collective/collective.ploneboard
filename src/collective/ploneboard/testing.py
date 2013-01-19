from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class CollectiveploneboardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.ploneboard
        xmlconfig.file(
            'configure.zcml',
            collective.ploneboard,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.ploneboard:default')

COLLECTIVE_PLONEBOARD_FIXTURE = CollectiveploneboardLayer()
COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PLONEBOARD_FIXTURE,),
    name="CollectiveploneboardLayer:Integration"
)
