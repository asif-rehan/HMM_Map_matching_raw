import csv

def read_data_point(datafile, lon_col_id, lat_col_id, timestamp_col_id):
    '''Generator object creating GPS Point'''
    csvfile = open(datafile, 'rb')
    
    
    reader = csv.reader(csvfile)

               
    rownum = 0   
     
    for row in reader:
        # Save header row.
        if rownum == 0:
            #header = row
            pass
        else:
            #colnum = 0
            #for col in row:
            #order in csv file 
            #for 20140307.csv     ['lat', 'lon', 'ele', 'time', 'course', 'speed', 'src', 'sat', 'hdop']
            
            yield (row[lon_col_id], row[lat_col_id],row[timestamp_col_id])
            
            #colnum += 1                
        rownum += 1

    csvfile.close()
    
    #yield (gps_lon, gps_lat, timestamp)

#datafile = r'C:\Users\asr13006\Google Drive\UConn MS\Data Collection\test20140218_upto154700.csv'
#datafile = datafile.replace("\\", "/")
#print datafile

#for i in read_data_point(datafile):
#    print i