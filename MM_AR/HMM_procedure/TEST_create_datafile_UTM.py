'''
Created on Sep 10, 2014

@author: asr13006
'''
from ReadFile import read_data_point
import pyproj
import csv

UTM18N = pyproj.Proj("+init=EPSG:32618")
datafile = r'C:\Users\asr13006\Google Drive\UConn MS\Data Collection\test20140217.csv'
datafile = datafile.replace("\\", "/")

        
with open('purple.csv', 'wb') as csvfile: 
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(('easting', 'northing', 'time'))
    
    generator = read_data_point(datafile)
    for point in generator:
        gps_easting, gps_northing = UTM18N(point[0], point[1])
        writer.writerow((gps_easting, gps_northing, point[2]))
