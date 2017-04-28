miles_per_lat = 69
miles_per_lon = 69

from RoutingOO import Node
# GridMap contains all information needed to build and contain the routing map for one route.
class GridMap:


    def __init__(self, planar_res, alt_res, bound_tol, origin_lat, origin_lon, dest_lat, dest_lon):
        self.planar_res = planar_res
        self.alt_res = alt_res

        self.bound_tol = bound_tol # in lat lon
        self.horiz_tol = None # boolean
        self.b0 = None
        self.b1 = None
        self.gmap = self.make_graph(planar_res, alt_res)


        # 178 + 3 = 181  181 % 180 = 1
        if(origin_lat > dest_lat):
            #coord nums in lat lon but 2 in miles _ NEED TO CHANGE THIS IF WE
            self.start_lat = origin_lat + .25
            self.end_lat = dest_lat - .25
            if (self.start_lat > 180):
                self.start_lat = -180 + self.start_lat % 180
            if (self.end_lat < -180):
                self.end_lat = 180 - ((-self.end_lat) % 180)
        else:
            self.start_lat = origin_lat - .25
            self.end_lat = dest_lat - .25
            if (self.start_lat < -180):
                self.end_lat = 180 - ((-self.end_lat) % 180)

            if (self.end_lat > 180):
                self.start_lat = -180 + self.start_lat % 180

        if (origin_lon > dest_lon):
            # coord nums in lat lon but 2 in miles _ NEED TO CHANGE THIS IF WE
            self.start_lon = origin_lon + .25
            self.end_lon = dest_lon - .25
            if (self.start_lon > 180):
                self.start_lon = -180 + self.start_lon % 180
            if (self.end_lon < -180):
                self.end_lon = 180 - ((-self.end_lon) % 180)
        else:
            self.start_lon = origin_lon - .25
            self.end_lon = dest_lon - .25
            if (self.start_lon < -180):
                self.end_lon = 180 - ((-self.end_lon) % 180)

            if (self.end_lon > 180):
                self.start_lon = -180 + self.start_lon % 180

#HAVE TO FIX THIS ERROR STEMMING FROM MI conversion

    # grid_res_planer - resolution in the 2D earth surface plane in miles
    # grid_res_vert - resolution for the altitude in miles
    def make_graph(self, grid_res_planar, grid_res_vert, origin, dest, bounding_tol):

        dim = self.compute_line_coeffs()

        num_vBlocks = 1 # ccurrently just 1 self.alt_res

        #this line is gonna cause lots of error
        num_blocks_line = (dim * 69  + self.bound_tol * 69) / self.planar_res
        alt = 40
        col_map = []
        row_map = []

        for i in range(0, num_vBlocks):
            for j in range(0, num_blocks_line):
                max_val, min_val, curr_line_val = self.get_bound_vals(i, dim)
                curr_val = max_val
                count = 0
                while curr_val > min_val:
                    if self.horiz_tol: # then
                        lon = max_val
                        lat = curr_line_val
                    else:
                        lon = curr_line_val
                        lat = max_val

                    col_map.append(Node([i, j, count], lat, lon, alt))
                    count += 1
                    # lat -= grid_res_planar / miles_per_lon
                    # lon -= grid_res_planar / miles_per_lon
                    # alt += grid_res_vert  # in miles not lon/lat

                row_map.append(col_map)
                col_map = []
            self.gmap.append(row_map)
            row_map = []




        # for i in range(0, num_rows):
        #     for j in range(0, num_cols):
        #         for k in range(0, num_vBlocks):
        #
        #             for a in range(-1, 2):
        #                 for b in range(-1, 2):
        #                     for c in range(-1, 2):
        #                         if (i + a >= 0 and i + a < num_rows and j + b >= 0 and j + b < num_cols and k + c >= 0 and k + c < num_vBlocks):
        #                             grid[i][j][k].neighbors.append(grid[i + a][j + b][k + c])

        return

    # def get_num_blocks(self, grid_res_planar, grid_res_vert, origin, dest):
    #
    #     # Use latitude and longitude to determine how large the graph needs to be - optimization
    #     latitude_dim = abs(origin[0] - dest[0])
    #     longitude_dim = abs(origin[1] - dest[1])
    #
    #     # Adding one extra block here to ensure that the graph is still spanning both points after we center 0th square on leftmost and topmost point dims
    #     num_rows = int((latitude_dim * miles_per_lat) / grid_res_planar) + 1
    #     num_cols = int((longitude_dim * miles_per_lon) / grid_res_planar) + 1
    #     num_vBlocks = int(ALT_DIM / grid_res_vert) + 1
    #
    #     return num_rows, num_cols, num_vBlocks

    def get_bound_vals(self, i):


        offset = (i * self.planar_res) + self.planar_res/2
        if(self.horiz_tol):
            curr_line_val = self.start_lat + ((self.end_lat - self.start_lat)/abs(self.end_lat - self.start_lat)) * offset
        else:
            curr_line_val = self.start_lon + ((self.end_lon - self.start_lon)/abs(self.end_lon - self.start_lon)) * offset

        bound1 = (self.b0 + self.bound_tol_mi) + self.b1 * curr_line_val

        bound2 = bound1 - (2 * self.bound_tol_mi)


        return max(bound1, bound2), min(bound1, bound2), curr_line_val

    def compute_line_coeffs(self):
        # check if lat dim or lon dim is longer to form the box
        lat_dim = abs(self.start_lat - self.end_lat)
        lon_dim = abs(self.start_lon - self.end_lon)

        # if lat dim is greater than lon dim
        if lat_dim > lon_dim:
            self.horiz_tol = True
            longest_dim = lat_dim

        # if lon dim is greater
        else:
            self.horiz_tol = False
            longest_dim = lon_dim

        if(self.horiz_tol):
            # calculate slope
            self.b1 = (self.end_lon - self.start_lon) / (self.end_lat - self.start_lat)

            # calculate intercept
            self.b0 = self.start_lon - self.b1 * self.start_lat

        else:
            # calculate slope
            self.b1 =  (self.end_lat - self.start_lat) / (self.end_lon - self.start_lon)

            # calculate intercept
            self.b0 = self.start_lat - self.b1 * self.start_lon


        return longest_dim



    def valid_block(self, gridNode, coeffs, horiz_tol):

        if(horiz_tol):


            coeffs[0][0] + coeffs[0][1] * gridNode.lon

            coeffs[1][0] + coeffs[1][1] * gridNode.lon

            coeffs[2][0] + coeffs[2][1] * gridNode.lon

            coeffs[3][0] + coeffs[3][1] * gridNode.lon

# def create_graph(grid_res_planar, grid_res_vert):
#     num_rows, num_cols, num_vBlocks = get_num_blocks(grid_res_planar, grid_res_vert)
#
#     speed = 2
#     print(num_rows)
#     print(num_cols)
#     print(num_vBlocks)
#
#     grid = []
#     col_map = []
#     alt_map = []
#     for i in range(0,num_rows):
#         for j in range(0,num_cols):
#             for k in range(0,num_vBlocks):
#                 #lat = BOT_LAT + grid_res_planar * i + (grid_res_planar/2)
#                 #lon = RIGHT_LON + grid_res_planar * j + (grid_res_planar/2)
#                 #alt = grid_res_vert * k + (grid_res_vert/2)
#                 lat = BOT_LAT + (LAT_DIM/num_rows) * i + ((LAT_DIM/num_rows)/2)
#                 lon = RIGHT_LON + (LON_DIM / num_cols) * j + ((LON_DIM / num_cols) / 2)
#                 alt =  ALT_DIM/num_vBlocks * k + (ALT_DIM/num_vBlocks)/2
#                 alt_map.append(Node([i,j,k], lat, lon, alt))
#             col_map.append(alt_map)
#             alt_map = []
#         grid.append(col_map)
#         col_map = []
#
#
#     for i in range(0, num_rows):
#         for j in range(0, num_cols):
#             for k in range(0, num_vBlocks):
#
#                 for a in range(-1, 2):
#                     for b in range(-1, 2):
#                         for c in range(-1, 2):
#                             if(i+a >= 0 and i+a < num_rows and j+b >= 0 and j+b < num_cols and k+c >= 0 and k+c < num_vBlocks):
#                                 grid[i][j][k].neighbors.append(grid[i + a][j + b][k + c])
#
#     return grid



        # # handle case where the flight is up and down.....
        # origin_plus = [coord_orig[1] + x_tol, coord_orig[2] + y_tol]
        # origin_minus = [coord_orig[1] - x_tol, coord_orig[2] - y_tol]
        #
        # dest_plus = [coord_dest[1] + x_tol, coord_dest[2] + y_tol]
        # dest_minus = [coord_dest[1] - x_tol, coord_dest[2] - y_tol]
        #
        # # calculating the coeffs for the bounding lines of the boxes..
        # # the bounding lines between origin in and dest
        # coeffs1 = self.calc_b0_b1(origin_plus, dest_plus, grid_size, horiz_tol)
        # coeffs2 = self.calc_b0_b1(origin_minus, dest_minus, grid_size, horiz_tol)
        #
        # # the bounding lines between uppers and lowers
        # coeffs3 = self.calc_b0_b1(origin_plus, origin_minus, grid_size, horiz_tol)
        # coeffs4 = self.calc_b0_b1(dest_plus, dest_minus, grid_size, horiz_tol)

        # num_rows, num_cols, num_vBlocks = self.get_num_blocks(grid_res_planar, grid_res_vert, origin, dest)

        # Left most latitude and longitude assuming positive latitudes and longitudes
        # topLeft = [max(origin[0], dest[0]) + (grid_res_planar / miles_per_lat) / 2,
        #           max(origin[1], dest[1]) + (grid_res_planar / miles_per_lon) / 2]

        # lat = topLeft[0] - grid_res_planar / 2
        # lon = topLeft[1] - grid_res_planar / 2
        # alt = grid_res_vert / 2
