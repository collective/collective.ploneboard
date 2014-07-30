import json
from zope.component.hooks import getSite
from zope.interface import implements
from zope.interface.declarations import alsoProvides
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import interfaces


class RateableCommentsAJAX(BrowserView):
    """ """
    implements(interfaces.IRateableCommentsAJAX)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def upvote(self, path):
        """ """
        user_rating = None
        s = getSite()
        rpath = '/'.join(
            s.getPhysicalPath()
            ) + path.replace(s.absolute_url(), '')
        reply = self.context.restrictedTraverse(rpath)
        if not IAttributeAnnotatable.providedBy(reply):
            alsoProvides(reply, IAttributeAnnotatable)
        annotations = IAnnotations(reply)
        voters = annotations.get('collective.ploneboard.discussion.voters', {})
        rating = annotations.get('collective.ploneboard.discussion.rating', 0)
        pm = getToolByName(s, 'portal_membership')
        member = pm.getAuthenticatedMember()
        member_id = member.getId()
        if member_id not in voters:
            voters[member_id] = 'up'
            user_rating = 'up'
            annotations['collective.ploneboard.discussion.voters'] = voters
            rating += 1
            annotations['collective.ploneboard.discussion.rating'] = rating
        elif voters.get(member_id) == 'down':
            # The voter is removing his vote, so let's delete him
            del voters[member_id]
            annotations['collective.ploneboard.discussion.voters'] = voters
            rating += 1
            annotations['collective.ploneboard.discussion.rating'] = rating
        elif voters.get(member_id) == 'up':
            # The up arrow has already been clicked before
            user_rating = 'up'

        return json.dumps(
            {'reply_rating': rating, 'user_rating': user_rating})

    def downvote(self, path):
        """ """
        user_rating = None
        s = getSite()
        rpath = '/'.join(
            s.getPhysicalPath()
            ) + path.replace(s.absolute_url(), '')
        reply = self.context.restrictedTraverse(rpath)
        if not IAttributeAnnotatable.providedBy(reply):
            alsoProvides(reply, IAttributeAnnotatable)
        annotations = IAnnotations(reply)
        voters = annotations.get('collective.ploneboard.discussion.voters', {})
        rating = annotations.get('collective.ploneboard.discussion.rating', 0)
        pm = getToolByName(s, 'portal_membership')
        if pm.isAnonymousUser():
            return
        pm = getToolByName(s, 'portal_membership')
        member = pm.getAuthenticatedMember()
        member_id = member.getId()
        if member_id not in voters:
            voters[member_id] = 'down'
            user_rating = 'down'
            annotations['collective.ploneboard.discussion.voters'] = voters
            rating -= 1
            annotations['collective.ploneboard.discussion.rating'] = rating
        elif voters.get(member_id) == 'up':
            # The voter is removing his vote, so let's delete him
            del voters[member_id]
            annotations['collective.ploneboard.discussion.voters'] = voters
            rating -= 1
            annotations['collective.ploneboard.discussion.rating'] = rating
        elif voters.get(member_id) == 'down':
            # The down arrow has already been clicked before
            user_rating = 'down'

        return json.dumps(
            {'reply_rating': rating, 'user_rating': user_rating})
