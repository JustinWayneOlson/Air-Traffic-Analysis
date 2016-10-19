import tornado.ioloop
import tornado.web
from  tornado.escape import json_decode
import random

#API endpoints are defined as classes

#Serve index.html
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #Patht to the webpage to be served
        self.render("./html/index.html")

#Get request takes in one arg via url and sends data back
class TestGetHandler(tornado.web.RequestHandler):
    def get(self, data):
        print("Serving JSON response to: " + data)
        #Convert passed in get request into int
        data=int(data)
        #Create dict to store data to return
        return_data={'response':[]}
        #Create random data
        '''Get data from database at this point'''
        for i in range(0,data):
            return_data['response'].append(random.random() * 10)
        #Write dict content to page, like a json response
        print return_data
        self.write(return_data)

#POST request takes in JSON from body, and returns JSON
class TestPostHandler(tornado.web.RequestHandler):
    def post(self):
        print(json_decode(self.request.body))
        return_data={
                'response':{
                    'message':'It Worked!!',
                    'content':random.random()*10
                }
        }
        self.write(return_data)

class D3TestHandler(tornado.web.RequestHandler):
    def get(self, city):
        #get lats and lons
        print city
        return_data={
                   "KMAE": [-120.12, 36.98 ],
                    "KSJC": [-121.92, 37.37 ],
                    "KMCE": [-120.50, 37.28 ],
                    "KMER": [-120.57, 37.37 ]
        }
        self.write(return_data)



#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        #localhost:8888/testget/(any number)
        (r"/testget/([0-9]*)", TestGetHandler),
        (r"/testd3/(.*)", D3TestHandler),
        (r"/testpost", TestPostHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
