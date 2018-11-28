# -*- coding: UTF-8 -*-
from plone.app.textfield import RichText
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.ploneboard import _


class ICollectivePloneboardLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMessageboard(Interface):
    """
    """


class ITopic(Interface):
    """
    """


class IConversation(Interface):
    """
    """

    text = RichText(
        title=_(u"Text"),
        required=True
    )
