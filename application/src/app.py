from helpers import *
from routingDriver import *

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
      POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/airports"
      engine = create_engine(POSTGRES_URL)
      query  = 'SELECT DISTINCT "{}" FROM flights LIMIT 100000'.format(column)
      dataframe = pd.read_sql_query(query, con = engine)
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

class RoutingComputeHandler(tornado.web.RequestHandler):
   def post(self):
      print "TEST"
      received_query = json_decode(self.request.body)
      return_data = {}
      #recieved_qurey has name, origin, dest, grid_res_planar, grid_res_vert, heruistic
      pp.pprint(received_query)
      return_data['response'] = routingDriver(received_query)
      #return_data['response'] = "Error could not handle request at this time."
      #kick off compute job, write to cassandra
      #response on success
      self.write(return_data)

class ComputedRoutesHandler(tornado.web.RequestHandler):
   def get(self):
      #query cassandra for all already computed routes
      #return list of unique route names

      query = """SELECT "jobName" from Routing """
      rows = cql_query_dict(query)
      #print(list(rows))
      pp.pprint(rows)
      return_data = {'response': list(rows)}
      self.write(return_data)

class DisplayRouteHandler(tornado.web.RequestHandler):
   def get(self, route_name):
      #query with route name get route information
      #return nodes and links
      query = """SELECT * from Routing WHERE "jobName" = '%s' """ % (route_name)
      rows = cql_query_dict(query)
      print(rows)
      return_data = {'response': list(rows)[0]}
      self.write(return_data)

class DeleteRouteHandler(tornado.web.RequestHandler):
   def get(self, route_name):
      #CQL DELETE with route name
      print route_name
      query = """DELETE FROM Routing WHERE "jobName" = '%s'  """ %(route_name)
      cql_query_dict(query)
      return_data = {'response': "Attempted to delete: {}".format(route_name)}
      self.write(return_data)

#URL of endpoint, mapped to which class it correlates to
#URL is matched via regex
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/routing", RoutingHandler),
        (r"/computed-routes", ComputedRoutesHandler),
        (r"/routing-compute", RoutingComputeHandler),
        (r"/display-route/(.*)", DisplayRouteHandler),
        (r"/delete-route/(.*)", DeleteRouteHandler),
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
