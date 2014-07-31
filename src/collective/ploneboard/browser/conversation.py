from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ConversationView(BrowserView):

    template = ViewPageTemplateFile('conversation.pt')

    def __call__(self):
        """"""
        return self.template()
