import webapp2

import jinja2
import os
import json

from models import *


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



class DashboardPage(webapp2.RequestHandler):
    def get(self, action = None, project_id = None):
        if action is not None:
            projects = Project.all().fetch(100)

            projects_json = json.dumps(map(lambda p: p.to_json(), projects))

            template_values = {
                'action': action,
                'project_id': project_id,
                'projects': projects,
                'projects_json': projects_json,
                'projects_count': len(projects)
            }

            template = jinja_environment.get_template('dashboard.html')
        else:
            template = jinja_environment.get_template('index.html')
            template_values = {}

        self.response.out.write(template.render(template_values))



class ProjectsHandler(BaseHandler):
    def post(self):
        model = json.loads(self.request.body)

        project = Project(name = model['name'],
                          android_id = model['android_id'],
                          appstore_id = model['appstore_id'])
        project.put()

        self.render_json(project.to_json())


    def get(self, project_id = None):
        if project_id is None:            
            projects = Project.all()
            self.render_json(map(lambda p: p.to_json(), projects))
        else:
            project_key = db.Key.from_path("Project", int(project_id))
            interactions = Interaction.all().ancestor(project_key).order('-created_at')
            self.render_json(map(lambda p: p.to_json(), interactions))


    def delete(self, project_id):
        project = Project.get_by_id(int(project_id))
        project.delete()

        self.render_json({ 'status': 'DELETED' })


class CheckProjectHandler(BaseHandler):
    def get(self, project_id):
        project = Project.get_by_id(int(project_id))
        project.check()


class InteractionsHandler(BaseHandler):
    def post(self):
        model = json.loads(self.request.body)


app = webapp2.WSGIApplication(
    [       
        (r'/api/projects/check/(\d+)', CheckProjectHandler),
        (r'/api/projects', ProjectsHandler),
        (r'/api/projects/(\d+)', ProjectsHandler),   
             
        (r'/(\w+)/(\d+)', DashboardPage),
        (r'/(\w+)', DashboardPage),
        (r'/', DashboardPage)
    ],
debug=True)