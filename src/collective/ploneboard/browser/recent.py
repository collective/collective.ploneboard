from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class Comments(BrowserView):

    template = ViewPageTemplateFile('recent_comments.pt')

    def __call__(self):
        """"""
        self.catalog = getToolByName(self.context, 'portal_catalog')
        return self.template()

    def recent_comments(self):
        comments = []
	folder_path = '/'.join(self.context.getPhysicalPath())
	limit = 50
        results = self.catalog.searchResults(
            {'portal_type': "Discussion Item",'review_state': "published","path": {'query': folder_path}, "sort_on": "modified", "sort_order":"descending", "sort_limit": limit}
            )
        for result in results:
            comments.append({
            	'title': result["Title"],
            	'description': result["Description"],
            	'review_state': result["review_state"],
            	'url': result.getURL(),
            	'modified_time': result["modified"].strftime(
		'%b %d, %Y %I:%M %p'
                ),
            })
        return comments

