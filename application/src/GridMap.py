import math


miles_per_lat = 69
miles_per_lon = 69

class Node:

    def __init__(self, lat, lon, alt, coords):
        #A* Parameter
        self.lat = lat
        self.lon = lon
        self.alt = alt
	self.coords = coords
        self.approxCost = 0
        self.neighbors = list()
        self.noFly = False
        self.weatherCost = 0
        self.parent = None
        self.priority = None
        self.gridMap = None
        self.timeVisited = None

	    #Aircraft Performance parameters
    	self.aircraftType =  None
	self.aircraftWeight = None
	self.aircraftFuelWeight = None
	self.aircraftCargoWeight = None
	self.aircraftFuelUsage = None
	self.aircraftAirSpeed = None
	self.aircraftGrndSpeed = None

	    #Weather parameters
	self.windSpeed = None
	self.windDirection = None
	self.precipitationChance = None
	self.precipitationType = None
	self.precipitationStrength = None
	self.airTemp = None
	self.humidity = None
	self.dewPoint = None

	    #Airline parameters
        


class GridMapContainer:
    def __init__(self, planar_res, alt_res, bound_tol, added_pt_buffer, origin_lat, origin_lon, dest_lat, dest_lon):
        self.planar_res = planar_res
        self.alt_res = alt_res

        self.bound_tol = bound_tol # in lat lon
        self.is_lon_major_axis = None # boolean
        self.b0 = None
        self.b1 = None
        
	if(added_pt_buffer <0):
		added_pt_Buffer = 0
	self.added_pt_buffer = int(math.ceil(added_pt_buffer * planar_res))

	self.added_pt_buffer =  added_pt_buffer
        self.offsets = list()

        # These variables are all set to actual values later in the funciton.
        self.start_lat = None
        self.end_lat = None
        self.start_lon = None
        self.end_lon = None
        self.major_axis_sign = None
        self.major_axis_sign = None
        self.lat_dim = None
        self.lon_dim = None

        # 178 + 3 = 181  181 % 180 = 1
        if origin_lat > dest_lat:
            # coord nums in lat lon but 2 in miles _ NEED TO CHANGE THIS IF WE
            self.start_lat = origin_lat + self.added_pt_buffer
            self.end_lat = dest_lat - self.added_pt_buffer
            if (self.start_lat > 180):
                self.start_lat = -180 + self.start_lat % 180
            if (self.end_lat < -180):
                self.end_lat = 180 - ((-self.end_lat) % 180)
        else:
            self.start_lat = origin_lat - self.added_pt_buffer
            self.end_lat = dest_lat + self.added_pt_buffer
            if (self.start_lat < -180):
                self.end_lat = 180 - ((-self.end_lat) % 180)

            if (self.end_lat > 180):
                self.start_lat = -180 + self.start_lat % 180

        if (origin_lon > dest_lon):
            # coord nums in lat lon but 2 in miles _ NEED TO CHANGE THIS IF WE
            self.start_lon = origin_lon + self.added_pt_buffer
            self.end_lon = dest_lon - self.added_pt_buffer
            if (self.start_lon > 180):
                self.start_lon = -180 + self.start_lon % 180
            if (self.end_lon < -180):
                self.end_lon = 180 - ((-self.end_lon) % 180)
        else:
            self.start_lon = origin_lon - self.added_pt_buffer
            self.end_lon = dest_lon + self.added_pt_buffer
            if (self.start_lon < -180):
                self.end_lon = 180 - ((-self.end_lon) % 180)

            if (self.end_lon > 180):
                self.start_lon = -180 + self.start_lon % 180

        # check if lat dim or lon dim is longer to form the box
        self.lat_dim = abs(round(self.start_lat - self.end_lat,8))
        self.lon_dim = abs(round(self.start_lon - self.end_lon, 8))

        # if lat dim is greater than lon dim
        if self.lat_dim < self.lon_dim:
            self.is_lon_major_axis = True
            self.major_axis_dim = self.lat_dim
            self.major_axis_sign = (self.end_lat - self.start_lat) / abs(self.start_lat - self.end_lat)
            self.minor_axis_sign = (self.end_lon - self.start_lon) / abs(self.start_lon - self.end_lon)

        # if lon dim is greater LOOK INTO THIS LINE
        else:
            self.is_lon_major_axis = False
            self.major_axis_dim = self.lon_dim
            self.minor_axis_sign = round((self.end_lat - self.start_lat) / abs(self.start_lat - self.end_lat))
            self.major_axis_sign = round((self.end_lon - self.start_lon) / abs(self.start_lon - self.end_lon))



    # grid_res_planer - resolution in the 2D earth surface plane in miles
    # grid_res_vert - resolution for the altitude in miles
    def make_graph(self):
        self.compute_line_coeffs()


        num_vBlocks = 1 # ccurrently just 1 self.alt_res


        nodes = {}
        #TODO ensure user knows the resolution must be passed in as deg lat lon
        num_blocks_line = int(math.ceil(self.major_axis_dim / self.planar_res))
	alt = 40
        col_map = []
        row_map = []
        countVec = []



        # Allocate space for y bounds of the current x value
        bound_curr = {
            'min': None,
            'max': None,
            'min_unit': None,
            'max_unit': None,
        }
        #Allocate space for y bounds of the next x value
        bound_next = {
            'min': None,
            'max': None,
            'min_unit': None,
            'max_unit': None,
        }

        column_next = []
        column_curr = []
        nodes = []

        # Calculate y bounds for current x value
        bound_max_first, bound_min_first = self.get_bound_vals(0)

        bound_min_first_unit = math.floor(bound_min_first / self.planar_res)

        assert(bound_min_first <=180 and bound_min_first >= -180), "not possible bounds"
        assert(bound_max_first <= 180 and bound_max_first >= -180), "not possible bounds"
	
	print("num_vBlocks: ", num_vBlocks)
	print("num_blocks_line: ", num_blocks_line)

        for i in range(0, num_vBlocks):

            for x in range(0, num_blocks_line):

                # Calculate y bounds for current x value
                bound_curr['max'], bound_curr['min'] = self.get_bound_vals(x)
                bound_curr['max_unit'] = int(math.floor(bound_curr['max'] / self.planar_res))
                bound_curr['min_unit'] = int(math.floor(bound_curr['min']/ self.planar_res))


                # Calculate y bounds for next x value
                bound_next['max'], bound_next['min'] = self.get_bound_vals(x + self.major_axis_sign)
                bound_next['max_unit'] = int(math.floor(bound_next['max'] / self.planar_res))
                bound_next['min_unit'] = int(math.floor(bound_next['min'] / self.planar_res))

                self.offsets.append(bound_curr['min_unit'] - bound_min_first_unit)


                if (self.is_lon_major_axis):
                    # same for every val x
                    lon = self.start_lon + (self.major_axis_sign) * x + self.planar_res / 2
                else:
                    lat = self.start_lat + (self.major_axis_sign) * x + self.planar_res / 2

                

                # We must declare and initialize the first column of nodes

                for m in range(bound_curr['min_unit'], bound_curr['max_unit'] + 1):

                    m = m - bound_curr['min_unit']

                    # TODO calculate actual lat lon fix that it doesn't account for going over 180 deg
                    if self.is_lon_major_axis:
                        lat = bound_curr['min_unit'] + (self.minor_axis_sign) * self.planar_res * (m - bound_curr['min_unit']) + self.planar_res / 2
                    else:
                        lon = bound_curr['min_unit'] + (self.minor_axis_sign) * self.planar_res * (m - bound_curr['min_unit']) + self.planar_res / 2

                    if x == 0:
                        column_curr.append(Node(lat, lon, i * self.alt_res, [i , x, m]))
                        if m != 0:

                            column_curr[m-1].neighbors.append(column_curr[m])
                            column_curr[m].neighbors.append(column_curr[m-1])
                    # For every subsequent col of nodes we will have already initialized them below so we just fill in information.
                    else:
                        column_curr[m].lat = lat
                        column_curr[m].lon = lon
                        column_curr[m].alt = alt
                        column_curr[m].coords = [i, x, m]

                        
                # Allocate space for the next column of nodes
                for m in range(bound_next['min_unit'], bound_next['max_unit'] + 1):
                    m = m - bound_next['min_unit']
                    tempNode = Node(None, None, None, [None, None, None])
                    column_next.append(tempNode)

                    if m != 0:

                        column_next[m - 1].neighbors.append(column_next[m])
                        column_next[m].neighbors.append(column_next[m - 1])

                for m in range(bound_curr['min_unit'], bound_curr['max_unit'] + 1):
                    m = m - bound_curr['min_unit']
                    for k in range(m-1, m+2):
                        if(k >= bound_next['min_unit'] and k <= bound_next['max_unit']):
                            if(k >= 0 and k < bound_curr['max_unit']):
                                column_curr[m].neighbors.append(tempNode[k])
                                tempNode[k].neighbors.append(column_curr[m])

                    nodes.append(column_curr)

                    column_curr = column_next

                self.gridMap = nodes
        return


    def get_bound_vals(self, i):

        offset = (i * self.planar_res) + self.planar_res/2
        if self.is_lon_major_axis:
            curr_line_val = self.start_lat + ((self.end_lat - self.start_lat)/abs(self.end_lat - self.start_lat)) * offset
        else:
            curr_line_val = self.start_lon + ((self.end_lon - self.start_lon)/abs(self.end_lon - self.start_lon)) * offset

        bound1 = (self.b0 + self.bound_tol) + self.b1 * curr_line_val

        bound2 = bound1 - (2 * self.bound_tol)

        return max(bound1, bound2), min(bound1, bound2)

    def compute_line_coeffs(self):

        if(self.is_lon_major_axis):
            # calculate slope
            self.b1 = (self.end_lon - self.start_lon) / (self.end_lat - self.start_lat)

            # calculate intercept
            self.b0 = self.start_lon - self.b1 * self.start_lat

        else:
            # calculate slope
            self.b1 =  (self.end_lat - self.start_lat) / (self.end_lon - self.start_lon)

            # calculate intercept
            self.b0 = self.start_lat - self.b1 * self.start_lon


        return
