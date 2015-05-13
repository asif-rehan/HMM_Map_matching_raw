from pyproj import Proj, Geod
import networkx as nx
import math, fiona
from shapely.geometry import LineString, Point

class TransitionWeight(object):
    '''
    creates transition object and sequence of shortest path nodes in the 
    road network MultiGraph
    cand_pt1 = cand_pt at time (t-1)
    cand_pt2 = cand_pt at time t
    '''
    def __init__(self, cand_pt1, cand_pt2, G , shapefile, beta):
        
        self.cand_pt1 = cand_pt1
        self.cand_pt2 = cand_pt2
        self.transition_wt = self.transition_weight(self.cand_pt1, 
                                                    self.cand_pt2, 
                                                    G, beta, shapefile)
        self.sp_len, self.sp_nodes, self.sp_rd_id_len =  \
                                            self.shortest_path(self.cand_pt1, 
                                                      self.cand_pt2,
                                                      G, shapefile)
                
    def end_nodes_dist(self, cand_pt, shapefile):
        '''for candidate point, returns two end nodes of the road it is on 
        and associated distances'''
        with fiona.open(shapefile) as roadnet:
            
            road = list(roadnet)[int(cand_pt.cand_pt_road_id)]
            node_count = len(road['geometry']['coordinates'])
            end_nodes = (road['geometry']['coordinates'][0], 
                         road['geometry']['coordinates'][node_count-1])
            roadlink = LineString(road['geometry']['coordinates'])
            pt = Point(cand_pt.cand_pt_easting, cand_pt.cand_pt_northing)
            dist_to_1st_node =  roadlink.project(pt)
            dist_to_2nd_node = roadlink.length - dist_to_1st_node
        return ({"node":end_nodes[0], "dist":dist_to_1st_node},
                {"node":end_nodes[1], "dist":dist_to_2nd_node})
        
 
    def shortest_path_diff_road(self, cand_pt1, cand_pt2, G, shapefile):
        '''
        shortest path length in meter
        shortest path results in sequence of node sequence forming the shortest
        path
        '''
        cp1_e_n_d = self.end_nodes_dist(cand_pt1, shapefile)
        cp2_e_n_d = self.end_nodes_dist(cand_pt2, shapefile) 
        #e_n_d end_nodes_dist
        
        sd = float("inf")
        
        for i in [0,1]:
            for j in [0,1]:
                #this try-except block catches KeyError in NX Dijkstra path
                try:
                    #print "cp1_e_n_d[i]['node']", cp1_e_n_d[i]['node']
                    #print "cp1_e_n_d[j]['node']", cp1_e_n_d[j]['node']
                    end_to_end_dist = nx.shortest_path_length(
                                        G, cp1_e_n_d[i]['node'], 
                                           cp2_e_n_d[j]['node'], 'weight')
                except KeyError:
                    print 'KeyError'
                    #print "cp1_e_n_d[i]['node']", cp1_e_n_d[i]['node']
                    #print "cp1_e_n_d[j]['node']", cp1_e_n_d[j]['node']
                    end_to_end_dist = float('inf')
                except nx.exception.NetworkXNoPath:
                    end_to_end_dist = float('inf')
                #distance between nearest road intersections for each of 
                #the cand points                    
                shortest_path_length = (cp1_e_n_d[i]['dist']
                                        + end_to_end_dist
                                        + cp2_e_n_d[j]['dist'])
                #total shortest path between cand points considering the 
                #pair of nearest intersection
                if shortest_path_length < sd:
                    sd = shortest_path_length
                    end_to_end_seq = nx.shortest_path(G, 
                                           cp1_e_n_d[i]['node'], 
                                           cp2_e_n_d[j]['node'], 
                                           'weight')                       
                    sp_nodes= list([(cand_pt1.cand_pt_easting,
                                          cand_pt1.cand_pt_northing)]
                                   + end_to_end_seq[:] +
                                   [(cand_pt2.cand_pt_easting,
                                     cand_pt2.cand_pt_northing)])
                    end_to_end_rd_id_len =[]
                    for i in range(len(end_to_end_seq)-1):
                        edge_info = [G[end_to_end_seq[i]][end_to_end_seq[i+1]]]
                        rd_id = edge_info.keys()
                        rd_len = edge_info.values()[0]['weight']
                        end_to_end_rd_id_len.append[(rd_id, rd_len)]
                    
                    
                    
                    sp_rd_id_len = [(cand_pt1.cand_pt_road_id,  
                                     cp1_e_n_d[i]['dist'])] +  \
                                     end_to_end_rd_id_len +   \
                                     [(cand_pt2.cand_pt_road_id,
                                       cp2_e_n_d[j]['dist'])]       
                                    
        if sd == float('inf'):
            sp_nodes = [(None, None)] 
            sp_rd_id_len = [('No road', float('inf'))]       
        #except nx.exception.NetworkXNoPath:
            #print "cand_pt_1",(cand_pt1.cand_pt_easting, 
            #                   cand_pt1.cand_pt_northing)
            #print "cand_pt_2",(cand_pt2.cand_pt_easting, 
            #                   cand_pt2.cand_pt_northing)
        #    sp_nodes = [None]
        #    shortest_path_length = float('inf')          
        return sd, sp_nodes, sp_rd_id_len    
    
    def shortest_path_same_road(self, cand_pt1, cand_pt2, G, shapefile):
        cp1_e_n_d = self.end_nodes_dist(cand_pt1, shapefile)
        cp2_e_n_d = self.end_nodes_dist(cand_pt2, shapefile)
        shortest_path_length = abs(cp1_e_n_d[0]['dist']
                                               - cp2_e_n_d[0]['dist'])
        sp_nodes= [(cand_pt1.cand_pt_easting, 
                                         cand_pt1.cand_pt_northing)] +  \
                                       [(cand_pt2.cand_pt_easting,
                                        cand_pt2.cand_pt_northing)]
        sd = shortest_path_length
        sp_rd_id_len = [(cand_pt1.cand_pt_road_id, sd)] 
        return sd, sp_nodes, sp_rd_id_len
    
    def shortest_path(self, cand_pt1, cand_pt2, G, shapefile):
        if cand_pt1.cand_pt_road_id == cand_pt2.cand_pt_road_id:
            dist, nd_seq, rd_id_len = self.shortest_path_same_road(cand_pt1, 
                                                     cand_pt2, 
                                                     G, shapefile)
        else:
            dist, nd_seq, rd_id_len = self.shortest_path_diff_road(cand_pt1, 
                                                     cand_pt2, 
                                                     G, shapefile)
        return dist, nd_seq, rd_id_len
    
    def cand_pt_UTM_to_LongLat(self, cand_pt_easting, cand_pt_northing):
        '''
        converts cand pt easting northing to lat-long for GCD calculations
        '''
         
        projection = Proj("+proj=utm +zone=18T, +north +ellps=WGS84\
                      +datum=WGS84 +units=m +no_defs")
        
        cand_pt_long, cand_pt_lat = projection(cand_pt_easting, 
                                               cand_pt_northing, inverse=True)
        return cand_pt_long, cand_pt_lat

    def GCD (self):
        '''calculates the Great Circular distance in meter using WGS84 and 
        UTM18T '''                    
        lon1, lat1 = self.cand_pt_UTM_to_LongLat(self.cand_pt1.cand_pt_easting, 
                                                self.cand_pt1.cand_pt_northing)
       
        lon2, lat2 = self.cand_pt_UTM_to_LongLat(self.cand_pt2.cand_pt_easting, 
                                                self.cand_pt2.cand_pt_northing)
        g = Geod(ellps='WGS84')
        GCD = g.inv(lon1, lat1, lon2, lat2)[2]       #GCD in meter  
        return GCD
        
    def transition_weight(self, cand_pt1, cand_pt2, G, beta, shapefile):
        '''
        calculates the transition probability based on Newson-Krumm's method
                        
                        p(diff) = (1/beta) * exp (-diff / beta)
        Here, 
            diff = absolute difference between GCD and Shortest distance
            beta = empirical formula 
        '''
        
        diff = abs(self.GCD() - self.shortest_path(cand_pt1, cand_pt2, G, 
                                                   shapefile)[0])
        transition_weight = (1/beta) * math.exp(-diff/beta)
        
        return transition_weight
        