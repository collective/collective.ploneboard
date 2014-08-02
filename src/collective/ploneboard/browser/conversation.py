from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import createObject
from AccessControl import getSecurityManager
from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.interfaces import IReplies
from Products.CMFCore.utils import getToolByName


class ConversationView(BrowserView):

    template = ViewPageTemplateFile('conversation.pt')

    def __call__(self):
        """"""
        form_var = self.request.form
        self.catalog = getToolByName(self.context, 'portal_catalog')
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
        results = self.catalog.searchResults({'portal_type': "conversation"})
        # Merges conv2 (merge_from) into conv1 (merge_into)
        conv1 = None
        conv2 = None
        for result in results:
            if result["id"] == merge_from:
                conv2 = result.getObject()
            elif result["id"] == merge_into:
                conv1 = result.getObject()
            else:
                continue
        conversation1 = IConversation(conv1)
        IReplies(conversation1)
        conversation2 = IConversation(conv2)
        IReplies(conversation2)
        # print "Conv2"
        # print list(conversation2.getThreads())
        # print "Conv1"
        # print list(conversation1.getThreads())
        old_to_new_id = {0: 0}
        for comment_dict in conversation2:
            new_comment = createObject('plone.Comment')
            new_comment.text = conversation2[comment_dict]\
                .getText('text/plain')
            new_comment.modification_date = conversation2[comment_dict]\
                .modification_date
            new_comment.creation_date = conversation2[comment_dict]\
                .modification_date

            old_reply_id = conversation2[comment_dict].in_reply_to
            new_comment.in_reply_to = old_to_new_id[old_reply_id]

            old_comment_id = conversation2[comment_dict].comment_id
            new_comment_id = conversation1.addComment(new_comment)
            if old_comment_id not in old_to_new_id:
                old_to_new_id[old_comment_id] = new_comment_id
