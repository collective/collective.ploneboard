
from plone.namedfile.field import NamedBlobFile
from persistent import Persistent

from z3c.form.field import Fields

from zope import interface

from zope.annotation import factory
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.z3cform.fieldsets import extensible

from plone.app.discussion.browser.comments import CommentForm
from plone.app.discussion.comment import Comment

from collective.ploneboard import _


class ICommentExtenderFields(Interface):
    attachment = NamedBlobFile(
        title=_(u"Attachment"),
        description=_(u""),
        required=False,
    )


class CommentExtenderFields(Persistent):
    interface.implements(ICommentExtenderFields)
    adapts(Comment)
    attachment = u""


CommentExtenderFactory = factory(CommentExtenderFields)


class CommentExtender(extensible.FormExtender):
    adapts(Interface, IDefaultBrowserLayer, CommentForm)

    fields = Fields(ICommentExtenderFields)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        self.add(ICommentExtenderFields, prefix="")
        self.move('attachment', after='text', prefix="")


# Patch Comment security to allow access for audio attachment
###


# a) The first option is to allow access or all sub objects, which means that
#    anyone, who can see the comment object, can see all its (non protected)
#    attributes
Comment.__allow_access_to_unprotected_subobjects__ = 1

# b) Would be to either provide __allow_access_to_unprotected_subobjects__
#    function with check for all possible fields or configure permission
#    for the audio field. Unfortunately, the permission on the field would
#    work only if the field value is acquisition aware, which NamedBlob
#    is not, and therefore the following would not work (and would also
#    prevent option a) from working by making the subobject protected.
