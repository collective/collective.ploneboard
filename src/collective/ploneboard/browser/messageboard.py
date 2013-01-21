from zope.component import getMultiAdapter

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
            conversations = getMultiAdapter(
                (topic, self.request),
                name="view"
            ).conversations()
            topics.append({
                'title': topic.title,
                'url': topic.absolute_url(),
                'conversations': conversations,
            })
        return topics
