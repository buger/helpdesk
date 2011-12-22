import webapp2
import lib.appstore.api as appstore
import lib.android_market.api as android_market

import jinja2
import os
import json

from google.appengine.ext import db


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/templates'))


class BaseHandler(webapp2.RequestHandler):

    def render_json(self, data, status = None):
        if status:
            self.response.set_status(status)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

    def render_text(self, string):
        self.response.headers['Content-Type'] = 'text'
        self.response.out.write(string)


class AppStorePage(webapp2.RequestHandler):
    def get(self):        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(appstore.getReviews(143441, 431451004))


class AndroidMarketPage(webapp2.RequestHandler):
    def get(self):  
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(android_market.getReviews('','com.masshabit.squibble.paid'))


class DashboardPage(webapp2.RequestHandler):
    def get(self, action):
        projects = Project.all().fetch(100)

        projects_json = json.dumps(map(lambda p: p.to_json(), projects))

        template_values = {
            'action': action,
            'projects': projects,
            'projects_json': projects_json,
            'projects_count': len(projects)
        }

        template = jinja_environment.get_template('dashboard.html')

        self.response.out.write(template.render(template_values))


class Project(db.Model):  
    owner = db.UserProperty()
    name = db.StringProperty()
    android_url = db.StringProperty()
    appstore_url = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def to_json(self):
        return {
            'id': self.key().id(),
            'name': self.name,
            'android_url': self.android_url,
            'appstore_url': self.appstore_url
        }


class ProjectsHandler(BaseHandler):
    def post(self):
        model = json.loads(self.request.body)

        project = Project(name = model['name'],
                          android_url = model['android'],
                          appstore_url = model['appstore'])
        project.put()

        self.render_json(project.to_json())


    def get(self):
        projects = Project.all()

        self.render_json(map(lambda p: p.to_json(), projects))


    def delete(self, project_id):
        project = Project.get_by_id(int(project_id))
        project.delete()

        self.render_json({ 'status': 'DELETED' })


app = webapp2.WSGIApplication(
    [
        ('/appstore', AppStorePage),
        ('/android-market', AndroidMarketPage),

        ('/api/projects', ProjectsHandler),
        ('/api/projects/(.*)', ProjectsHandler),
        
        ('/(.*)', DashboardPage)
    ],
debug=True)