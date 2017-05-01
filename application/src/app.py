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
        received_query2 = copy.deepcopy(received_query)
        flights, verbose_toggle, paths_toggle = flights_df(received_query)
        flights_bar, verbose_toggle, paths_toggle = flights_df(received_query2)
        plot_data = mean_data(flights, flights_bar)
        return_data = {}
        if(verbose_toggle):
           return_data['verbose'] = "This is eventually going to be more information!"
        if(paths_toggle):
            airports = airports_dict("data/airport_locs.csv")
            nodes, node_lookup = create_nodes(flights, airports)
            if len(nodes) == 1:
                self.write({"response":"Error no airports found for given query"})
            links = make_links(nodes, flights, node_lookup)
            return_data['nodes'] = nodes
            return_data['links'] = links
            return_data['plot_data'] = plot_data
            nodes = color(nodes)
            self.write(return_data)
        else:
            airports = airports_dict("data/airport_locs.csv")
            nodes, node_lookup = create_nodes(flights, airports)
            return_data['nodes'] = nodes
            return_data['plot_data'] = plot_data
            nodes = color(nodes)
            self.write(return_data)

class RoutingComputeHandler(tornado.web.RequestHandler):
   def post(self):
      received_query = json_decode(self.request.body)
      return_data = {}
      #recieved_qurey has name, origin, dest, grid_res_planar, grid_res_vert, heruistic
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
      return_data = {'response': list(rows)}
      self.write(return_data)

class DisplayRouteHandler(tornado.web.RequestHandler):
   def get(self, route_name):
      #query with route name get route information
      #return nodes and links
      query = """SELECT * from Routing WHERE "jobName" = '%s' """ % (route_name)
      rows = cql_query_dict(query)
      return_data = {'response': list(rows)[0]}
      self.write(return_data)

class DeleteRouteHandler(tornado.web.RequestHandler):
   def get(self, route_name):
      #CQL DELETE with route name
      query = """DELETE FROM Routing WHERE "jobName" = '%s'  """ %(route_name)
      cql_query_dict(query)
      return_data = {'response': "Attempted to delete: {}".format(route_name)}
      self.write(return_data)

def mean_data(flights_line, flights_bar):
   plot_data = {}
   line_plot_data = {}
   bar_plot_data = {}
   #for line
   typeData = "date"
   plot_data_line = calc_data(flights_line, typeData)


   #for bar
   typeData = "origin"
   plot_data_bar = calc_data(flights_bar, typeData)

   plot_data['line'] = plot_data_line
   plot_data['bar'] = plot_data_bar
   return plot_data

def calc_data(flights, typeData):
    indp_var = []
    delay_time = []
    plot_data = {}
    line_plot_data = {}
    bar_plot_data = {}
    for index, row in flights.iterrows():
       print(type(row))
       print row
       if(typeData == "date"):
         indp_var.append(row.FlightDate)
       if(typeData == "origin"):
         indp_var.append(row.Origin)
       delay_time.append(row.CarrierDelay)
    start_day_index = 0
    curr_day = indp_var[0]
    mean_day = []
    indp_axis = []

    for index in range(0, len(indp_var)):
        if(curr_day != indp_var[index]):
            mean_day.append(np.round(np.mean(delay_time[start_day_index:index])))
            indp_axis.append(curr_day)
            curr_day = indp_var[index]
            start_day_index = index

    if(start_day_index == index):
        mean_day.append(np.round(delay_time[index]))

    else:
        mean_day.append(np.round(np.mean(delay_time[start_day_index:index])))

    indp_axis.append(indp_var[index])
    '''Plot data: { 'bar':{
                        'labels': [distinct airports],
                        'series': [values]
                        },
                  'line':{
                        'labels': [distinct dates],
                        'series': [daily sums]
                     }
                 }
    '''

    line_plot_data['labels'] = indp_axis
    line_plot_data['series'] = mean_day
    #plot_data['line'] = line_plot_data
    #plot_data['bar'] = line_plot_data
    return line_plot_data


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
