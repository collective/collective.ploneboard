from Products.Five import BrowserView
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Conversation(BrowserView):
    template = ViewPageTemplateFile('merge_conversation.pt')

    def __call__(self):
        """"""
        self.current_user = getSecurityManager().getUser()
        self.catalog = getToolByName(self.context, 'portal_catalog')
        return self.template()

    def conversations(self):
        my_conversations = []
        results = self.catalog.searchResults({'portal_type': "conversation"})
        for result in results:
            sm = getSecurityManager()
            ans = sm.checkPermission(
                'Collective Ploneboard: Merge Conversation',
                result.getObject()
                )
            if ans:
                my_conversations.append({
                    'title': result["Title"],
                    'description': result["Description"],
                    'review_state': result["review_state"],
                    'url': result.getURL(),
                    'modified_time': result["modified"].strftime(
                        '%b %d, %Y %I:%M %p'
                        ),
                    })
        return my_conversations
