
from plone.namedfile.field import NamedBlobFile
from persistent import Persistent

from z3c.form.field import Fields

from zope import interface

from zope.annotation import factory
from zope.component import adapts, queryUtility
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.z3cform.fieldsets import extensible

from plone.registry.interfaces import IRegistry
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.app.discussion.browser.comments import CommentForm
from plone.app.discussion.comment import Comment

from collective.ploneboard import _
# import pdb


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
        # pdb.set_trace()
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        self.add(ICommentExtenderFields, prefix="")
        self.move('attachment', after='text', prefix="")
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        settings.text_transform = 'text/html'
