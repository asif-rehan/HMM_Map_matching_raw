from shapely.geometry import Point
from candidate_points_functions import list_cand_point_constructor
import pyproj
        

class ObsPoint:
    '''
    Input:     gps observation data and road network file
    Output:    gps point object --> attributes: lat, long,timestamp, mean,
               std dev, and list of candidate points. 
               Candidate point objects each has its own attributes   
    '''
    def __init__(self,  gps_lon, gps_lat,timestamp, 
                 gps_mean, gps_std_dev, circ_radius, road_net_shp):
        
        
        self.gps_easting, self.gps_northing = lat_long_to_UTM_point(
                                                            gps_lon, gps_lat)
        self.timestamp = timestamp
        self.gps_point = Point(float(self.gps_easting), float(
                                                        self.gps_northing)) 
        self.gps_mean = gps_mean
        self.circ_radius = circ_radius
        self.gps_std_dev = gps_std_dev
        self.buffered = self.gps_point.buffer(self.circ_radius)
        
        self.candidate_points = list_cand_point_constructor(
                                    self.buffered, 
                                    self.gps_point, 
                                    road_net_shp, 
                                    self.gps_mean, self.gps_std_dev)
    
def lat_long_to_UTM_point(lon, lat):
    UTM18N = pyproj.Proj("+init=EPSG:32618")
    return UTM18N(lon, lat)

#TESTING WITH SAMPLE DATA        
path = "C:/Users/asr13006/Desktop/Thesis/Copy of Data Reservoir/\
routes/County 13/road network micro/nxspatial3/NF/copy/TransformCRS/\
LineString_Road_Network_UTM.shp"        

#gps1  = ObsPoint(-72.25796, 41.808015, '2/18/2014 15:29', 0, 50, path)
#print gps1.gps_point     #727779.5330614256 4632090.555875832
#for candidate_points in gps1.candidate_points:
#    print candidate_points.__dict__