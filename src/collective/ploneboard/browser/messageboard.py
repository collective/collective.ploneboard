from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.discussion.interfaces import IConversation
from AccessControl import getSecurityManager
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.app.discussion.interfaces import IDiscussionSettings


class MessageboardView(BrowserView):

    template = ViewPageTemplateFile('messageboard.pt')

    def __call__(self):
        self.list_of_topics = []
        self.list_of_conv = []
        self.current_user = getSecurityManager().getUser()
        self.catalog = getToolByName(self.context, 'portal_catalog')
        results = self.catalog(portal_type="topic")
        for result in results:
            rid = result.getRID()
            id_of = self.catalog._catalog.getIndex(
                "id").getEntryForObject(rid, default=[])
            self.list_of_topics.append(id_of)
        for topic_id in self.context.objectIds():
            if topic_id not in self.list_of_topics:
                self.list_of_conv.append(topic_id)
        context = self.context.aq_inner
        # print context.category
        if context.category:
            context.cats = list(set(context.category.split('\r\n')))
        else:
            context.cats = []
        if u'' in context.cats:
            context.cats.remove(u'')
        # print context.cats
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        self.qi_tool = getToolByName(context, 'portal_quickinstaller')
        pid = 'plone.formwidget.captcha'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        if pid in installed:
            if context.captcha:
                settings.captcha = "captcha"
            else:
                settings.captcha = "disabled"
        return self.template()

    def givelink(self):
        ans = None
        if str(self.current_user) == "Anonymous User":
            return ans
        ans = self.context.absolute_url() + "/@@my-contribution"
        return ans

    def link_recent_comments(self):
        ans = self.context.absolute_url() + "/@@recent-comments"
        return ans

    def categories(self, sort_mode="recent"):
        # Returns topics grouped by categories
        # Default function: the sort_mode for conversations is RECENT FIRST
        categ = {}
        for topic_id in self.context.objectIds():
            if topic_id not in self.list_of_topics:
                continue
            topic = self.context[topic_id]
            conversations = getMultiAdapter(
                (topic, self.request),
                name="view"
            ).conversations(sort_mode)
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
                        'conversations': conversations,
                        'modification_time': topic.modified().strftime(
                            '%b %d, %Y %I:%M %p'
                            ),
                        })
                else:
                    key = each_category
                    categ[key].append({			# Topic added to that category
                        'title': topic.title,
                        'category': topic.category,
                        'url': topic.absolute_url(),
                        'conversations': conversations,
                        'modification_time': topic.modified().strftime(
                            '%b %d, %Y %I:%M %p'
                            ),
                        })
        # Order based on last modified (default)
        for each_category in categ:
            categ[each_category] = sorted(
                categ[each_category],
                key=lambda topic_instance: topic_instance['modification_time'],
                reverse=True
                )
        return categ

    def direct_conversations(self, sort_mode="recent"):
        conversations = []
        for conv_id in self.list_of_conv:
            conversation_entity = self.context[conv_id]
            # Check for view permission
            sm = getSecurityManager()
            if sm.checkPermission('View', conversation_entity):
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
                    'modification_time':
                        conversation_entity.modified().strftime(
                            '%b %d, %Y %I:%M %p'
                            ),
                    })
        if sort_mode == "recent":
            sort_key = "modification_time"
        else:
            sort_key = "total_comments"
        # Order based on last modified (default)
        conversations = sorted(
            conversations,
            key=lambda conversation_instance: conversation_instance[
                sort_key
                ],
            reverse=True
            )
        return conversations
