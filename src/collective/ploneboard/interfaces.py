# -*- coding: UTF-8 -*-
from plone.app.textfield import RichText
from plone.directives import form

from collective.ploneboard import _


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
