class CandidatePointObject:
    '''    creates the candidate point objects
    each candidate point object has its own attributes '''
    
    def __init__(self,cand_pt_northing, cand_pt_easting, 
                            cand_pt_road_id, cand_pt_timestamp,
                            cand_pt_emission_prob):
        self.cand_pt_northing = cand_pt_northing
        self.cand_pt_easting = cand_pt_easting
        self.cand_pt_road_id = cand_pt_road_id
        self.cand_pt_timestamp = cand_pt_timestamp
        self.cand_pt_emission_prob = cand_pt_emission_prob
            

def list_cand_point_constructor(shapely_buffer, shapely_point, timestamp,
                             path_to_road_network_shapefile, 
                             gps_mean, gps_std_dev):
    '''
    creates a list of the candidate point objects given a gps observation point
    
    -->   road_network is a NetworkX object, it doesn't have 
            geometric properties
    so need to have the points along the polyline and construct
    a polyline in the fiona/shapely/OGR
    
    --> disjoint == False, indicates links within error region
    '''
    import scipy.stats
    import fiona
    from shapely.geometry import LineString, Point 

    #the road network with shapefile 
    with fiona.open(path_to_road_network_shapefile) as shp:
        list_cand_pt = []
        rec = shp.next()
        
        
        while rec:
                    
            vertices_on_link = rec['geometry']['coordinates']
            line = LineString(vertices_on_link)
            
            if line.intersects(shapely_buffer) == True:
            
                x = line.interpolate(line.project(shapely_point))
                candidate_point = list(x.coords)
                distance = Point(candidate_point).distance(shapely_point)
                emission_prob = scipy.stats.norm(gps_mean, gps_std_dev).pdf(
                                                                    distance)
                candidate_point=CandidatePointObject(
                                cand_pt_easting =candidate_point[0][0],
                                cand_pt_northing = candidate_point[0][1],
                                cand_pt_road_id = rec['id'],
                                cand_pt_timestamp = timestamp,
                                cand_pt_emission_prob =emission_prob)
                list_cand_pt.append(candidate_point)
                
            try:
                rec = next(shp)
            except StopIteration:
                rec = False
    return list_cand_pt
"""
def OJ_emis_prob(line, shapely_point, shapely_buffer):
    coord = list(line.intersection(shapely_buffer).coords)
    for x 
    
"""