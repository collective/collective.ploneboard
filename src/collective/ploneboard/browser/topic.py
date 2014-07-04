from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from AccessControl import getSecurityManager
from plone.app.discussion.interfaces import IConversation


class TopicView(BrowserView):

    template = ViewPageTemplateFile('topic.pt')

    def __call__(self):
        context = self.context.aq_inner
        # print context.category
        if context.category == []:
            context.category.append('Unspecified')
        return self.template()

    def conversations(self, sort_mode="recent"):
        conversations = []
        for conversation_id in self.context.objectIds():
            conv = self.context[conversation_id]
            # Check for view permission
            sm = getSecurityManager()
            if sm.checkPermission('View', conv):
                pad_conv = IConversation(self.context[conversation_id])
                # XXX: last_commenter should be in metadata
                comments = pad_conv.items()
                if comments:
                    last_commenter = comments[-1:][0][1].author_name
                else:
                    last_commenter = ""
                conversations.append({
                    'title': conv.title,
                    'url': conv.absolute_url(),
                    'total_comments': pad_conv.total_comments,
                    'last_commenter': last_commenter,
                    'last_comment_date': pad_conv.last_comment_date,
                    'modification_time': conv.modified().strftime(
                        '%b %d, %Y %I:%M %p'
                        ),
                })
        if sort_mode == "recent":
            sort_key = 'modification_time'
        else:
            sort_key = 'total_comments'
        # Order based on last modified (default)
        conversations = sorted(
            conversations,
            key=lambda conversation_instance: conversation_instance[
                sort_key
                ],
            reverse=True
            )
        return conversations
