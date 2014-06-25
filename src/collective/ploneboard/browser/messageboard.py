from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.discussion.interfaces import IConversation
from AccessControl import getSecurityManager


class MessageboardView(BrowserView):

    template = ViewPageTemplateFile('messageboard.pt')

    def __call__(self):
        self.list_of_topics = []
        self.list_of_conv = []
        self.current_user = getSecurityManager().getUser()
        context = self.context.aq_inner
        # print context.category
        context.cats = context.category.split('\r\n')
        # print context.cats
        return self.template()

    def givelink(self):
        ans = None
        if str(self.current_user) == "Anonymous User":
            return ans
        ans = self.context.absolute_url() + "/@@my-contribution"
        return ans

    def categories(self):						# Returns topics grouped by categories
        categ = {}
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(portal_type="topic")
        for result in results:
            rid = result.getRID()
            id_of = catalog._catalog.getIndex(
                "id").getEntryForObject(rid, default=[])
            self.list_of_topics.append(id_of)
        for topic_id in self.context.objectIds():
            if topic_id not in self.list_of_topics:
                self.list_of_conv.append(topic_id)
                continue
            topic = self.context[topic_id]
            conversations = getMultiAdapter(
                (topic, self.request),
                name="view"
            ).conversations()
            if topic.category == []:
                topic.category.append('Unspecified')
            for each_category in topic.category:
                if each_category not in categ:
                    key = each_category
                    categ[key] = []				# New category arrived
                    categ[key].append({
                        'title': topic.title,
                        'category': topic.category,
                        'url': topic.absolute_url(),
                        'conversations': conversations
                        })
                else:
                    key = each_category
                    categ[key].append({			# Topic added to that category
                        'title': topic.title,
                        'category': topic.category,
                        'url': topic.absolute_url(),
                        'conversations': conversations,
                        })
        return categ

    def direct_conversations(self):
        conversations = []
        for conv_id in self.list_of_conv:
            conversation_entity = self.context[conv_id]
            pad_conv = IConversation(conversation_entity)
            # XXX: last_commenter should be in metadata
            comments = pad_conv.items()
            if comments:
                last_commenter = comments[-1:][0][1].author_name
            else:
                last_commenter = ""
            conversations.append({
                'title': conversation_entity.title,
                'url': conversation_entity.absolute_url(),
                'total_comments': pad_conv.total_comments,
                'last_commenter': last_commenter,
                'last_comment_date': pad_conv.last_comment_date,
                })
        return conversations
    """
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
                'category': topic.category,
                'url': topic.absolute_url(),
                'conversations': conversations,
            })
        return topics
    """
