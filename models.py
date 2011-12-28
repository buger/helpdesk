from google.appengine.ext import db

from google.appengine.api import taskqueue
from google.appengine.ext import deferred

import lib.appstore.api as appstore
import lib.android_market.api as android_market

from lib.model_to_json import model_to_json


class Interaction(db.Model):
    source = db.StringProperty()
    author = db.StringProperty(indexed = False)
    title = db.StringProperty(indexed = False)
    content = db.TextProperty(indexed = False)
    content_length = db.IntegerProperty()
    rank = db.IntegerProperty()
    date = db.DateTimeProperty()
    version = db.StringProperty()
    device = db.StringProperty()
    date = db.DateTimeProperty()
    helpful = db.BooleanProperty(default = False)
    created_at = db.DateTimeProperty(auto_now_add=True)

    def to_json(self):
        return model_to_json(self)     

    
def check_appstore_reviews(project_id, app_id):
    reviews = appstore.getReviews(143441, app_id)

    parent_key = db.Key.from_path("Project", project_id)

    for_put = map(lambda r: Interaction(parent = parent_key,
                                        key_name = "%s%s%s%s" % (r['title'], r['user'],r['date'],r['rank']),
                                        source = "IOS",
                                        title = r['title'],
                                        author = r['user'],
                                        content = r['review'],
                                        content_length = len(r['review'] or ""),
                                        rank = r['rank'],
                                        date = r['date'],
                                        version = r['version']), reviews)

    db.put(for_put)

    
def check_android_reviews(project_id, app_id):
    reviews = android_market.getReviews('en',app_id)

    parent_key = db.Key.from_path("Project", project_id)

    for_put = map(lambda r: Interaction(parent = parent_key,
                                        key_name = "%s%s%s%s" % (r['title'], r['user'],r['date'],r['rank']),
                                        source = "Android",
                                        title = r['title'],
                                        author = r['user'],
                                        content = r['review'],
                                        content_length = len(r['review'] or ""),
                                        rank = r['rank'],
                                        device = r['device'],
                                        date = r['date'],
                                        version = r['version']), reviews)

    db.put(for_put)


class Project(db.Model):  
    owner = db.UserProperty()
    name = db.StringProperty()
    android_id = db.StringProperty()
    appstore_id = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def to_json(self):
        return model_to_json(self)
    
    def check(self):
        if self.appstore_id is not None:           
            taskqueue.add(url='/task/interactions/%s/appstore/%s' % (self.key().id(), self.appstore_id), method='GET')
                
        if self.android_id is not None:
            taskqueue.add(url='/task/interactions/%s/android_market/%s' % (self.key().id(), self.android_id), method='GET')