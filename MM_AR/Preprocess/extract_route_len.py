import fiona
import pyproj
from shapely.geometry import LineString, shape
import pandas as pd

def extract_route_len(source_file):
    '''
    Returns the total lengths of the road segments in each of the routes  
    source file should have columns for each of the routes. the source file has
    columns 
    '''
    lengths = {'Blue': 0, 'Red': 0, 'Green': 0, 'Yellow': 0, 
               'Purple': 0, 'Orange': 0}
    WGS84 = pyproj.Proj("+init=EPSG:4326")
    UTM18N=pyproj.Proj("+init=EPSG:32618")
            
    try:
        with fiona.open(source_file, driver= 'ESRI Shapefile', crs='WGS84') as source:
            for elem in source:
                
                if elem['geometry']['type'] == 'LineString':
                    lon, lat  = zip(*elem['geometry']['coordinates'])
                    easting, northing = pyproj.transform(WGS84, UTM18N, lon, lat)
                    transformed_LineString_vertices = zip(easting, northing)
                    #tranfrormed_linestring = LineString(transformed_LineString_vertices)
                    elem_length = LineString(transformed_LineString_vertices).length
                    
                if elem['geometry']['type'] == 'MultiLineString':
                    elem_length = 0
                    parts = len(elem['geometry']['coordinates'])
                    for line_num in range(parts):
                        lon, lat  = zip(*elem['geometry']['coordinates'][line_num])
                        easting, northing = pyproj.transform(WGS84, UTM18N, lon, lat)
                        transformed_LineString_vertices = zip(easting, northing)
                        #tranfrormed_linestring = LineString(transformed_LineString_vertices)
                        elem_length += LineString(transformed_LineString_vertices).length
                        
                for route in lengths.keys():
                    if elem['properties'][route] == route:
                        lengths[route] += elem_length
    except:
        pass
    return lengths

def route_ckt_len(single_vis, routes, multivisits):
    """
    Find the complete circuit lengths for each of the routes
    Parameters
    ----------
    single_vis: 
        dbf file for all the road-links consisting of the complete set of 
        routes, each road-link is visited at least once
    routes: list of the route names e.g. ['Red', 'Blue', 'Yellow']
    multivisits:
        list of dbf files for each of the routes. 
        Each dbf file has the record of the road-links which are visited 
        more than once in the route. If a link is visited n times, then 
        this dbf file has (n-1) records of the same road-link for the route
    
    return
    ------
    a dictionary with route names as keys and corresponding lengths as values
    """
    from simpledbf import Dbf5
    lengths = {'Blue': 0, 'Red': 0, 'Green': 0, 'Yellow': 0, 
               'Purple': 0, 'Orange': 0}
    sin_vis = Dbf5(single_vis).to_dataframe()[routes+['Length_met']]
    for i in routes:
        dbl_vis = Dbf5(multivisits[i]).to_dataframe()
        dbl_vis_len = dbl_vis[[i, 'Length_met']].dropna()['Length_met'].sum()
        sin_vis_len = sin_vis[[i, 'Length_met']].dropna()['Length_met'].sum()
        
        lengths[i] = dbl_vis_len + sin_vis_len
    return lengths 
    
    
    
    
if __name__ == "__main__":
    import  os
    source_file = os.path.join(r'C:\Users\asr13006\Desktop\Thesis',
                               'Copy of Data Reservoir\routes\County 13',
                               'Road_network_micro.shp')
    #print extract_route_len(source_file)
    source_file = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                            'Py Codes\HMM_Krumm_Newson_Implementation',
                            'MM_AR\Relevant_files',
                            'LineString_Road_Network_UTM.shp')
    
    sin_vis = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                            'Py Codes\HMM_Krumm_Newson_Implementation',
                            'MM_AR\Relevant_files',
                            'LineString_Road_Network_UTM.dbf')
    routes = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    multivisits = {}
    for rt in routes: 
        multivisits[rt] = os.path.join(r'C:\Users\asr13006\Google Drive',
                                       'UConn MS',
                                  r'Py Codes\HMM_Krumm_Newson_Implementation',
                                  r'MM_AR\Relevant_files',
                                  'route_length_double_visits',
                                  r'{}_double\{}_double.dbf'.format(rt, rt))    
    print  route_ckt_len(sin_vis, routes, multivisits)

    