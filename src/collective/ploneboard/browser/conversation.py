from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName


class ConversationView(BrowserView):

    template = ViewPageTemplateFile('conversation.pt')

    def __call__(self):
        """"""
        form_var = self.request.form
        if 'conv_selected_to_merge' in form_var:
            if 'merge_with_conv' in form_var:
                if 'form.button.MergeConversationDone' in form_var:
                    self.merge_them(
                        form_var["conv_selected_to_merge"],
                        form_var["merge_with_conv"]
                        )
                    return self.request.response.\
                        redirect(self.context.absolute_url())
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

    def merge_them(self, merge_into=None, merge_from=None):
        """"""
        print "Hey, I'm a function which merges two conversations"
