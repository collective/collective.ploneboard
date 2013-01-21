from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MessageboardView(BrowserView):

    template = ViewPageTemplateFile('messageboard.pt')

    def __call__(self):
        return self.template()

    def topics(self):
        topics = []
        for topic_id in self.context.objectIds():
            topic = self.context[topic_id]
            conversations = []
            for conversation_id in topic.objectIds():
                conversations.append({
                    'title': topic[conversation_id].title,
                    'url': topic[conversation_id].absolute_url(),
                })
            topics.append({
                'title': topic.title,
                'url': topic.absolute_url(),
                'conversations': conversations,
            })
        return topics
