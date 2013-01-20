from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MessageboardView(BrowserView):

    template = ViewPageTemplateFile('messageboard.pt')

    def __call__(self):
        return self.template()
