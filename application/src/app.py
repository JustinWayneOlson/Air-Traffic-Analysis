from helpers import *

#Handler for main (index) page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #URL to main (index) page
        self.render("./html/index.html")

#Handler for about page
class AboutHandler(tornado.web.RequestHandler):
  def get(self):
      #URL to about page
      self.render("./html/about.html")

#Handler for routing page
class RoutingHandler(tornado.web.RequestHandler):
  def get(self):
      #URL to about page
      self.render("./html/routing.html")

#Handler to populate dropdown menus with options from database
class DropdownFillHandler(tornado.web.RequestHandler):
   def get(self, column):
        query  = 'SELECT "{}" FROM AirportTrafficAnalytics.Transtats LIMIT 100000 ALLOW FILTERING'.format(column)
        dataframe = cql_query(query, [column])
        response = {'response':[j for i in dataframe.values.tolist() for j in i]}
        self.write(response)

#Handler to display airports (nodes) and flights (links)
class DisplayAirportsHandler(tornado.web.RequestHandler):
    def post(self):
        received_query = json_decode(self.request.body)
        flights, verbose_toggle, paths_toggle = flights_df(received_query)
        return_data = {}
        if(verbose_toggle):
           return_data['verbose'] = "This is eventually going to be more information!"
        print(paths_toggle)
        print(type(paths_toggle))
        if(paths_toggle):
            airports = airports_dict("data/airport_locs.csv")
            nodes, node_lookup = create_nodes(flights, airports)
            if len(nodes) == 1:
                self.write({"response":"Error no airports found for given query"})

            links = make_links(nodes, flights, node_lookup)
            return_data['nodes'] = nodes
            return_data['links'] = links
            nodes = color(nodes)
            self.write(return_data)
        else:
            airports = airports_dict("data/airport_locs.csv")
            nodes, node_lookup = create_nodes(flights, airports)
            return_data['nodes'] = nodes
            nodes = color(nodes)
            pp.pprint(return_data)
            self.write(return_data)

#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/routing", RoutingHandler),
        (r"/js/(.*)",tornado.web.StaticFileHandler, {"path": "./static/js"},),
        (r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "./static/css"},),
        (r"/img/(.*)",tornado.web.StaticFileHandler, {"path": "./static/img"},),
        (r"/display-airports", DisplayAirportsHandler),
        (r"/dropdown-fill/(.*)", DropdownFillHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("serving on port 8888")
    tornado.ioloop.IOLoop.current().start()
