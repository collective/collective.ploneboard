from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.discussion.interfaces import IConversation


class TopicView(BrowserView):

    template = ViewPageTemplateFile('topic.pt')

    def __call__(self):
        return self.template()

    def conversations(self):
        conversations = []
        for conversation_id in self.context.objectIds():
            conv = self.context[conversation_id]
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
                'total_comments': pad_conv.total_comments(),
                'last_commenter': last_commenter,
                'last_comment_date': pad_conv.last_comment_date,
            })
        return conversations
