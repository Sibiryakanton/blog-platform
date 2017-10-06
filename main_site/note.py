from .models import BlogPost
from django.conf import settings


class FeedManager(object):
    def __init__(self, request):
        self.session = request.session
        notelist = self.session.get(settings.FEED_SESSION_ID)
        if not notelist:
            notelist = self.session[settings.FEED_SESSION_ID] = {}
        self.notelist = notelist

    def add(self, post):
        post_id = str(post.pk)
        if post.author.username not in self.notelist:
            self.notelist[post.author.username] = []
        if post_id not in self.notelist[post.author.username]:
            self.notelist[post.author.username] += [post_id]
            self.save()
        print(self.notelist[post.author.username])
        print(self.notelist['player'])

    def save(self):
        self.session[settings.FEED_SESSION_ID] = self.notelist
        self.session.modified = True

    def remove(self, author):
        author_username = author.username
        if author_username in self.notelist:
            del self.notelist[author_username]
            self.save()
