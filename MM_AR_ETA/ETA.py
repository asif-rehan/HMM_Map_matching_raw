
'''
Created on Jan 3, 2015

@author: asr13006
'''

class ETA(object):
    '''
    inputs
    ======
    1.  coordinates of the bus stops in KML document
    2.  Create a dummy NetworkX graph for the bus stops showing connections
        with directionality
    3.  Find the arrival time at stop n, and travel time between n to (n+1)
        Arrival time in seconds. Between 0 to 86400
        Travel time in seconds
    '''

    #def __init__(self, st_node_csv):
        
        

    def extract_bus_stops(self, datafile, st_node_csv):
        '''from Google Earth bus stops are pinned into a KMZ folder 
        from KML extracts bus stop names and coordinates into a CSV'''

        from pykml import parser
        import  csv
        root = parser.parse(open(datafile)).getroot()
        with open(st_node_csv, 'wb') as w_csv:
            wr = csv.writer(w_csv)
            wr.writerow(('id','stop_name', 'longitude','latitude'))
            for i in range(len(root.Document.Folder.Placemark)):
                try: 
                    st_name = root.Document.Folder.Placemark[i].name
                    lat = root.Document.Folder.Placemark[i].LookAt.latitude
                    lon = root.Document.Folder.Placemark[i].LookAt.longitude
                    wr.writerow((i, st_name, lon,lat))
                except:
                    break
            return w_csv
        
    
    def stops_graph(self, conn):
        ''' Make a NX graph with only bus stops connected such as 
        they were the nodes in the network
        conn = directed connectivities between nodes in a list of tuples'''
        import networkx as nx
        import matplotlib.pyplot as plt
        #import pandas as pd
        
        DG = nx.DiGraph()
        #st_df = pd.read_csv('out.csv')
        #stop_name = st_df['stop_name']
        
        #node_coord = zip(st_df['lon'], st_df['lat'])
        DG.add_edges_from(conn)
        nx.draw_networkx(DG)
        plt.show()
   
    def dataframe_UTM_converter(self, data_df, lat_col='latitude', 
                                lon_col='longitude'):
        '''
        data_df = pandas.read_csv()
        df_lat_lon_col = pandas.dataframe with lat, lon columns
        '''
        from MM_AR.GPS_point_cand_point.GPS_point import lat_long_to_UTM_point
        data_df['easting'] = ''
        data_df['northing'] = ''
        for idx in range(len(data_df)):
            lon, lat = data_df.loc[idx, lon_col], data_df.loc[idx, lat_col]
            east, north = lat_long_to_UTM_point(lon, lat)
            data_df.loc[idx, 'easting'] = east 
            data_df.loc[idx,'northing'] = north 
        return data_df
        
    def stop_buffer_list(self, stops_df, distance_m=5):
        '''stops_df = pandas.read_csv(st_node_csv.csv)
        '''
        from shapely.geometry import Point
        
        self.dataframe_UTM_converter(stops_df)
        stp_buf_list = []
        
        for idx in range(len(stops_df)):
            easting = stops_df.loc[idx]['easting']
            northing = stops_df.loc[idx]['northing']
            stp_buf_list.append(Point(easting, northing).buffer(distance=  \
                                                                distance_m))
        return stp_buf_list
    
    
    def data_df_creator(self, datafile):
        from pandas import read_csv
        return read_csv(datafile)[['utc_time_stamp','latitude', 'longitude']]
        
    def extr_dw(self, data_df, stops_df, stop_buffer_list):
        '''extract entry and exit time for the bus stop, n. 
        '''
        from shapely.geometry import Point
        for stop_id in stops_df['id']:
            data_df[str(stop_id)] = ''
        
        for idx in range(len(data_df)):
            for i in stops_df['id']:
                pt = Point(data_df.iloc[idx]['easting'], 
                           data_df.iloc[idx]['northing'])
                if pt.intersects(stop_buffer_list[i]) == True :
                    data_df.iloc[idx][i] = True
                if pt.intersects(stop_buffer_list[i]) == False :
                    data_df.iloc[idx][i] = False
        indices_df = [str(i) for i in range(len(stops_df))]
        dwl_df = data_df[data_df[indices_df].any(axis=1)]
        return dwl_df
        
    def extract_TT_DT(self, dwl_df, conn):
        '''
        Extract dwelling time at bus stop and travel time from bus stop 1 to 2
        '''
        #import pandas as pd
        #buffer(bus_stop)
        #entry_ts(gps_pt):
        #    if gps_pt.intersect(st_buff):
        #        return ent_ts, st_id 
        #can potentially capture vehicles going in the other end
        #exit_ts(gps_pt):
        #    if gps_pt.intersect(st_buff) == False:
        #        return ext_ts, st_id
        
        #return table
        
        



    def estimate(self, test_X, stop_list, tables):
        
        return None
    

if __name__ == '__main__':
    import os
    import pandas as pd
    folder = r"C:\Users\asr13006\Google Drive\UConn MS\Bus Stops\bus_stops_uconn_shuttle"
    os.chdir(folder)
    eta = ETA()
    eta.extract_bus_stops('doc.kml', 'out.csv')
    
    stops = [i for i in range(4, -1, -1)]
    
    conn = [(stops[i-1], stops[i]) for i in range(1,5)]
    eta.stops_graph(conn)
    stops_df = pd.read_csv('out.csv')
    print stops_df
    lst = eta.stop_buffer_list(stops_df, distance_m=50)
    print stops_df
    data_file = os.path.join(r'C:\Users\asr13006\Desktop\Thesis',
                           'Copy of Data Reservoir', 
                'March 2013\March_routes', '032629uconn204.csv')
    data_df = eta.data_df_creator(data_file)
    data_df = eta.dataframe_UTM_converter(data_df)
    extr_dwell = eta.extr_dw(data_df, stops_df, lst)
    