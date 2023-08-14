import json


class Post:
    def __init__(self, post):
        self.description = post.get('description', 'No description available')
        self.postID = post.get('postID', None)
        self.keywords = post.get('keywords', '').strip().split(",") if post.get('keywords') else []
        self.source = post.get('source', 'Unknown')
        self.articleSlug = post.get('articleSlug', '')
        self.publishedDate = post.get('publishedDate', 'Unknown')
        self.pageTitle = post.get('pageTitle', '')
        self.taxonomyTerms = post.get('taxonomyTerms', [])
        self.where = post.get('where', 'Unknown')
        self.displayAuthors = post.get('displayAuthors', False)
        self.topics = post.get('topics', 'Unknown')

    def to_dict(self):
        return self.__dict__
