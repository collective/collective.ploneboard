# -*- coding: UTF-8 -*-
from plone.app.textfield import RichText
from plone.directives import form
from zope import schema
from collective.ploneboard import _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from five import grok

@grok.provider(IContextSourceBinder)
def possibleCategories(context):
    #cat = context.category
    terms = []
    category = context.cats
    #print category
    for category_i in category:
        terms.append(SimpleVocabulary.createTerm(str(category_i), str(category_i), str(category_i)))
    return SimpleVocabulary(terms)


class IMessageboard(form.Schema):
	category=schema.Text(
		title=_(u"Categories for tagging Topics"),
        description=_(u"Seperate by writing in different lines"),
		required=True
		)

class ITopic(form.Schema):
    category = schema.List(
            title=_(u"Category"),
            description=_(u"Choose to tag your Topic"),
            required=True,
            value_type= schema.Choice(title=_(u"Ssup"),source=possibleCategories,required=False)
        )

class IConversation(form.Schema):
    """
    """
    text = RichText(
        title=_(u"Text"),
        required=True
    )
