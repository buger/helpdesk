import webapp2
import lib.appstore.api as appstore
import lib.android_market.api as android_market


class AppStorePage(webapp2.RequestHandler):
    def get(self):        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(appstore.getReviews(143441, 284993459))


class AndroidMarketPage(webapp2.RequestHandler):
    def get(self):  
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(android_market.getReviews('','com.masshabit.squibble.paid'))


app = webapp2.WSGIApplication(
    [
        ('/appstore', AppStorePage),
        ('/android-market', AndroidMarketPage)
    ],
debug=True)