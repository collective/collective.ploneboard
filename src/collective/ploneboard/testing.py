from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2

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

COLLECTIVE_PLONEBOARD_ROBOT_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PLONEBOARD_FIXTURE,
        AUTOLOGIN_LIBRARY_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="CollectivePloneboardLayer:Robot"
)
