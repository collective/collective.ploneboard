from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import createObject
from AccessControl import getSecurityManager
from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.interfaces import IReplies
from zope.interface.declarations import alsoProvides
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
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
        # Take out all the comments out of conversation1
        # For each comment store text, author_username, creator, creation_date
        # and modification, comment_id, in_reply_to, title, author_name,
        # author_email, user_notification
        comments_list = []
        comments_id = conversation1.keys()
        for id_comment in conversation1:
            comment_obj = conversation1[id_comment]
            if not IAttributeAnnotatable.providedBy(comment_obj):
                alsoProvides(comment_obj, IAttributeAnnotatable)
            annotations = IAnnotations(comment_obj)
            rating = annotations.get(
                'collective.ploneboard.discussion.rating',
                0
                )
            comments_list.append({
                'comment_obj': conversation1[id_comment],
                'comment_text': comment_obj.getText('text/plain'),
                'comment_au': comment_obj.author_username,
                'comment_an': comment_obj.author_name,
                'comment_ae': comment_obj.author_email,
                'comment_un': comment_obj.user_notification,
                'comment_creator': comment_obj.creator,
                'comment_cd': comment_obj.creation_date,
                'comment_md': comment_obj.modification_date,
                'comment_id': id_comment,
                'comment_irt': comment_obj.in_reply_to,
                'comment_title': comment_obj.title,
                'comment_rating': rating,
                })
        for i in comments_id:
            try:
                del conversation1[i]
            except:
                print "Id was not found"

        comments_list2 = []
        for id_comment in conversation2:
            comment_obj = conversation2[id_comment]
            if not IAttributeAnnotatable.providedBy(comment_obj):
                alsoProvides(comment_obj, IAttributeAnnotatable)
            annotations = IAnnotations(comment_obj)
            rating = annotations.get(
                'collective.ploneboard.discussion.rating',
                0
                )
            comments_list2.append({
                'comment_obj': conversation2[id_comment],
                'comment_text': comment_obj.getText('text/plain'),
                'comment_au': comment_obj.author_username,
                'comment_an': comment_obj.author_name,
                'comment_ae': comment_obj.author_email,
                'comment_un': comment_obj.user_notification,
                'comment_creator': comment_obj.creator,
                'comment_cd': comment_obj.creation_date,
                'comment_md': comment_obj.modification_date,
                'comment_id': id_comment,
                'comment_irt': comment_obj.in_reply_to,
                'comment_title': comment_obj.title,
                'comment_rating': rating,
                })
        f_c_l = comments_list + comments_list2
        final_comments_list = sorted(
            f_c_l,
            key=lambda comment: comment['comment_cd']
            )

        old_to_new_id = {0: 0}
        for comment in final_comments_list:
            new_comment = createObject('plone.Comment')
            new_comment.text = comment['comment_text']
            new_comment.author_username = comment['comment_au']
            new_comment.author_name = comment['comment_an']
            new_comment.author_email = comment['comment_ae']
            new_comment.user_notification = comment['comment_un']
            new_comment.creator = comment['comment_creator']
            new_comment.creation_date = comment['comment_cd']
            new_comment.modification_date = comment['comment_md']
            new_comment.in_reply_to = old_to_new_id[comment['comment_irt']]
            new_comment.title = comment['comment_title']
            old_comment_id = comment['comment_id']
            new_comment_id = conversation1.addComment(new_comment)
            if old_comment_id not in old_to_new_id:
                old_to_new_id[old_comment_id] = new_comment_id
            if not IAttributeAnnotatable.providedBy(new_comment):
                alsoProvides(new_comment, IAttributeAnnotatable)
            annotations = IAnnotations(new_comment)
            rating = comment['comment_rating']
            annotations['collective.ploneboard.discussion.rating'] = rating
