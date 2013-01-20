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
            conversations.append({
                'title': self.context[conversation_id].title,
                'url': self.context[conversation_id].absolute_url(),
                'total_comments': IConversation(
                    self.context[conversation_id]
                ).total_comments,
            })
        return conversations
