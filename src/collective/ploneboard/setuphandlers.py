__docformat__ = "epytext"


def runCustomCode(site):
    """ Run custom add-on product
    installation code to modify Plone
    site object and others

    @param site: Plone site
    """


def setupVarious(context):
    """
    @param context:
    Products.GenericSetup.context.DirectoryImportContext
    instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('collective.ploneboard-various.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    runCustomCode(portal)


def importVarious(context):
    """
    @param context:
    Products.GenericSetup.context.DirectoryImportContext
    instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('collective.ploneboard-various.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    runCustomCode(portal)
