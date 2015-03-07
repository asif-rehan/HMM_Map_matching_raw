'''
Created on Dec 24, 2014

@author: asr13006
'''
import os
import pandas as pd 
import matplotlib.pyplot as plt
from MM_AR.GPS_point_cand_point.GPS_point import lat_long_to_UTM_point
import fiona 

path=r'C:\Users\asr13006\Google Drive\UConn MS\Py Codes\HMM_Krumm_Newson_Implementation\MM_AR_validation'
os.chdir(path)

chunk = r'chunk_032629uconn201.csv'
chunk = pd.read_csv(chunk)

road_net_shp = '../MM_AR/Relevant_files/LineString_Road_Network_UTM.shp'
with fiona.open(road_net_shp) as road_shp:
            for item in road_shp:                
                line = item['geometry']['coordinates']
                (line_easting, line_northing) = zip(*line)
                plt.plot(line_easting, line_northing, 'k')

utm_pts = map(lat_long_to_UTM_point, 
                      chunk['longitude'],
                      chunk['latitude'])
(easting, northing) = zip(*utm_pts)
plt.plot(easting, northing, 'bo')

if __name__ == '__main__':
    pass