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

    def givemergelink(self):
        return self.context.absolute_url() + "/@@check-and-merge-conversation"

    def selected(self):
        selected_conv = []
        selected_conv.append({
            'id': self.context.getId(),
            'title': self.context.title,
            })
        return selected_conv

    def conversations(self):
        my_conversations = []
        selected_id = self.context.getId()
        results = self.catalog.searchResults({'portal_type': "conversation"})
        for result in results:
            sm = getSecurityManager()
            ans = sm.checkPermission(
                'Collective Ploneboard: Merge Conversation',
                result.getObject()
                )
            if ans:
                if selected_id == result["id"]:
                    continue
                else:
                    my_conversations.append({
                        'id': result["id"],
                        'title': result["Title"],
                        'description': result["Description"],
                        'review_state': result["review_state"],
                        'url': result.getURL(),
                        'modified_time': result["modified"].strftime(
                            '%b %d, %Y %I:%M %p'
                            ),
                        })
        return my_conversations