from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.discussion.interfaces import IConversation
from AccessControl import getSecurityManager
from zope.component import queryUtility
from datetime import date
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

    def statistics_topics(self):
        self.num_of_topics = 0
        folder_path = '/'.join(self.context.getPhysicalPath())
        topics = self.catalog.searchResults({
            'portal_type': "topic",
            'review_state': "published",
            "path": {'query': folder_path},
            "sort_on": "modified",
            "sort_order": "descending",
            })
        self.num_of_topics = len(topics)
        return self.num_of_topics

    def statistics_conv(self):
        self.num_of_conversations = 0
        folder_path = '/'.join(self.context.getPhysicalPath())
        conversations = self.catalog.searchResults({
            'portal_type': "conversation",
            'review_state': "published",
            "path": {'query': folder_path},
            "sort_on": "modified",
            "sort_order": "descending",
            # "sort_limit": limit
            })
        self.num_of_conversations = len(conversations)
        return self.num_of_conversations

    def statistics_comment(self):
        self.num_of_comments = 0
        self.last_commenter = None
        self.last_comment_date = None
        self.last_comment_url = None
        folder_path = '/'.join(self.context.getPhysicalPath())
        comments = self.catalog.searchResults({
            'portal_type': "Discussion Item",
            'review_state': "published",
            "path": {'query': folder_path},
            "sort_on": "modified",
            "sort_order": "descending",
            })
        self.num_of_comments = len(comments)
        if len(comments) != 0:
            self.last_commenter = comments[0]["Title"]
            self.last_comment_date = comments[0]["modified"].strftime(
                '%b %d, %Y %I:%M %p'
                )
            self.last_comment_url = comments[0].getURL()
        portal_membership = getToolByName(
            self.context,
            'portal_membership')
        if self.last_commenter is None:
            self.last_commenter_image = 'defaultUser.png'
        else:
            self.last_commenter_image = portal_membership\
                .getPersonalPortrait(self.last_commenter)\
                .absolute_url()
        result = {
            'comments': self.num_of_comments,
            'last_commenter': self.last_commenter,
            'last_commenter_image': self.last_commenter_image,
            'last_comment_date': self.last_comment_date,
            'last_comment_url': self.last_comment_url,
            }
        ans = []
        ans.append(result)
        return ans

    def statistics_users(self):
        self.users_participated = 0
        folder_path = '/'.join(self.context.getPhysicalPath())
        comments = self.catalog.searchResults({
            'portal_type': "Discussion Item",
            'review_state': "published",
            "path": {'query': folder_path},
            "sort_on": "modified",
            "sort_order": "descending",
            })
        conversations = self.catalog.searchResults({
            'portal_type': "conversation",
            'review_state': "published",
            "path": {'query': folder_path},
            "sort_on": "modified",
            "sort_order": "descending",
            })
        topics = self.catalog.searchResults({
            'portal_type': "topic",
            'review_state': "published",
            "path": {'query': folder_path},
            "sort_on": "modified",
            "sort_order": "descending",
            })
        users = []
        self.comments_today = 0
        for comment in comments:
            if comment["Creator"] not in users:
                users.append(comment["Creator"])
            if comment["modified"].strftime('%b %d, %Y') == \
                    date.today().strftime('%b %d, %Y'):
                self.comments_today += 1
        for conv in conversations:
            if conv["Creator"] not in users:
                users.append(conv["Creator"])
        for topic in topics:
            if topic["Creator"] not in users:
                users.append(topic["Creator"])
        self.users_participated = len(users)
        result = {
            'users': self.users_participated,
            'comments_today': self.comments_today
            }
        ans = []
        ans.append(result)
        return ans

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
