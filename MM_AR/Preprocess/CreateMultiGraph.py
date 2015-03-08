import networkx as nx
import fiona, pickle
import os
#import matplotlib.pyplot as plt
from fiona.crs import from_epsg

def CreateMultiGraph(utm_shp_path):
    G = nx.MultiGraph()
    with fiona.open(utm_shp_path,crs= from_epsg(32618)) as shp:
        #,driver='ESRI Shapefile'
        for elem in shp:
            strt = elem['geometry']['coordinates'][0]
            len_coords = len(elem['geometry']['coordinates'])
            end = elem['geometry']['coordinates'][len_coords-1]
            length_meter = elem['properties']['Length_met']
            G.add_edge(strt, end, weight = length_meter)
                                        
    '''print len(G), G.number_of_nodes(),G.number_of_edges()
    nx.draw_graphviz(G)                    
    plt.show()'''
    return G

def CreateMultiDiGraph(utm_shp_path):
    G = nx.MultiDiGraph()
    with fiona.open(utm_shp_path,crs= from_epsg(32618)) as shp:
        #,driver='ESRI Shapefile'
        for elem in shp:
            strt = elem['geometry']['coordinates'][0]
            len_coords = len(elem['geometry']['coordinates'])
            end = elem['geometry']['coordinates'][len_coords-1]
            length_meter = elem['properties']['Length_met']
            G.add_edge(strt, end, weight = length_meter)
            G.add_edge(end, strt, weight = length_meter)                                    
    '''print len(G), G.number_of_nodes(),G.number_of_edges()
    nx.draw_graphviz(G)                    
    plt.show()'''
    return G
utm_shp_path = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                            r'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR',
                            r'Relevant_files\LineString_Road_Network_UTM.shp')
'''
utm_shp_path = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                           r'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR',
                           r'Relevant_files\editing_alumni_rd',
                           'LineString_Road_Network_UTM2.shp') 
'''

#utm_shp_path = "C:/Users/asr13006/Desktop/Thesis/Copy of Data Reservoir/\
#routes/County 13/road network micro/nxspatial3/NF/copy/TransformCRS/\
#LineString_Road_Network_UTM.shp" 

if __name__ == '__main__':
    G = CreateMultiGraph(utm_shp_path)
    pickle.dump(G, open('../Relevant_files/MultiGraph.p', 'wb'))
    MDG = CreateMultiDiGraph(utm_shp_path)
    pickle.dump(MDG, open('../Relevant_files/MultiDiGraph.p', 'wb'))
    #print nx.dijkstra_path(G, (732805.0271117099, 4623614.515877712),
    #                              (729658.6308007092, 4630691.33944068), 'weight')
    
    #print G.neighbors((729658.6308007092, 4630691.33944068))
    #print G.neighbors((732805.0271117099, 4623614.515877712))
    
    #print G.degree([(732805.0271117099, 4623614.515877712),(732805.0271117099, 4623614.515877712)])
    
