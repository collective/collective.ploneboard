from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager


class Contribution(BrowserView):

    template = ViewPageTemplateFile('contribution.pt')

    def __call__(self):
        """"""
        self.current_user = getSecurityManager().getUser()
        self.catalog = getToolByName(self.context, 'portal_catalog')
        return self.template()

    def messageboards(self):
        my_messageboards = []
        results = self.catalog.searchResults({'portal_type': "messageboard"})
        for result in results:
            rid = result.getRID()
            author = self.catalog._catalog.getIndex(
                'Creator'
                ).getEntryForObject(rid, default=[])
            if str(self.current_user) == str(author):
                my_messageboards.append({
                    'title': result["Title"],
                    'description': result["Description"],
                    'review_state': result["review_state"],
                    'url': result.getURL(),
                    'modified_time': result["modified"].strftime(
                        '%b %d, %Y %I:%M %p'
                        ),
                    })
        return my_messageboards

    def topics(self):
        my_topics = []
        results = self.catalog.searchResults({'portal_type': "topic"})
        for result in results:
            rid = result.getRID()
            author = self.catalog._catalog.getIndex(
                'Creator'
                ).getEntryForObject(rid, default=[])
            if str(self.current_user) == str(author):
                my_topics.append({
                    'title': result["Title"],
                    'description': result["Description"],
                    'review_state': result["review_state"],
                    'url': result.getURL(),
                    'modified_time': result["modified"].strftime(
                        '%b %d, %Y %I:%M %p'
                        ),
                    })
        return my_topics

    def conversations(self):
        my_conversations = []
        results = self.catalog.searchResults({'portal_type': "conversation"})
        for result in results:
            rid = result.getRID()
            author = self.catalog._catalog.getIndex(
                'Creator'
                ).getEntryForObject(rid, default=[])
            if str(self.current_user) == str(author):
                my_conversations.append({
                    'title': result["Title"],
                    'description': result["Description"],
                    'review_state': result["review_state"],
                    'url': result.getURL(),
                    'modified_time': result["modified"].strftime(
                        '%b %d, %Y %I:%M %p'
                        ),
                    })
        return my_conversations

    def comments(self):
        my_comments = []
        results = self.catalog.searchResults(
            {'portal_type': "Discussion Item"}
            )
        for result in results:
            rid = result.getRID()
            author = self.catalog._catalog.getIndex(
                'Creator'
                ).getEntryForObject(rid, default=[])
            if str(self.current_user) == str(author):
                my_comments.append({
                    'title': result["Title"],
                    'description': result["Description"],
                    'review_state': result["review_state"],
                    'url': result.getURL(),
                    'modified_time': result["modified"].strftime(
                        '%b %d, %Y %I:%M %p'
                        ),
                    })
        return my_comments
