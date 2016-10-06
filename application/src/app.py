import tornado.ioloop
import tornado.web
from  tornado.escape import json_decode
import random

#API endpoints are defined as classes

#Serve index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./html/index.html")

#Server hello world
class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

#Get request takes in one arg via url and sends data back
class TestGetHandler(tornado.web.RequestHandler):
    def get(self, data):
        data=int(data)
        return_data={
                'response':[]
        }
        for i in range(0,data):
            return_data['response'].append(random.random() * 10)
        self.write(return_data)

#POST request takes in JSON from body, and returns JSON
class TestPostHandler(tornado.web.RequestHandler):
    def post(self):
        print json_decode(self.request.body)
        return_data={
                'response':{
                    'message':'It Worked!!',
                    'content':random.random()*10
                }
        }
        self.write(return_data)

#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/hello", HelloWorldHandler),
        #localhost:8888/testpost/(any single digit number)
        (r"/testget/([0-9]*)", TestGetHandler),
        (r"/testpost", TestPostHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
