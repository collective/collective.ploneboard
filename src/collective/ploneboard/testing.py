from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig


class CollectiveploneboardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.ploneboard
        xmlconfig.file(
            'configure.zcml',
            collective.ploneboard,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.ploneboard:default')


COLLECTIVE_PLONEBOARD_FIXTURE = CollectiveploneboardLayer()
COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PLONEBOARD_FIXTURE,),
    name="CollectiveploneboardLayer:Integration"
)
