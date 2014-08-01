from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName


class ConversationView(BrowserView):

    template = ViewPageTemplateFile('conversation.pt')

    def __call__(self):
        """"""
        return self.template()

    def givemergelink(self):
        ans = None
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            return ans
        ans = self.context.absolute_url() + "/@@merge-conversation"
        return ans

    def canmerge(self):
        sm = getSecurityManager()
        ans = sm.checkPermission(
            'Collective Ploneboard: Merge Conversation',
            self.context
            )
        return ans
