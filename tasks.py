import webapp2
from models import *

class Interaction(webapp2.RequestHandler):

	def get(self, project_id, market_type, app_id):		
		if market_type == 'appstore':
			check_appstore_reviews(int(project_id), app_id)
		elif market_type == "android_market":
			check_android_reviews(int(project_id), app_id)


app = webapp2.WSGIApplication(
    [        
        (r'/task/interactions/(\d+)/(\w+)/(.*)', Interaction)
    ],
debug=True)
