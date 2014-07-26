from zope.interface import Interface


class IRateableCommentsAJAX(Interface):
    """ """

    def upvote(self, oid, uid):
        """ """

    def downvote(self, oid, uid):
        """ """
