# -*- coding: UTF-8 -*-
from plone.app.textfield import RichText
from plone.directives import form
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.ploneboard import _


class ICollectivePloneboardLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMessageboard(form.Schema):
    """
    """


class ITopic(form.Schema):
    """
    """


class IConversation(form.Schema):
    """
    """

    text = RichText(
        title=_(u"Text"),
        required=True
    )
