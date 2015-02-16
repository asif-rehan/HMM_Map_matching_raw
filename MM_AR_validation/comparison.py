from datetime import datetime
from matplotlib import pyplot as plt
import os
import pandas as pd
from MM_AR_validation.validation import Validate
import pyproj

def shuttle_data2dataframe(f):
    return pd.read_csv(f, usecols=[8, 11, 10, 15], 
        parse_dates=['utc_time_stamp'], 
        keep_date_col=True, 
        index_col='utc_time_stamp')

def plot_seg(bus_id, f, start, end):
    
    road_shp_file = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                                 'Py Codes\HMM_Krumm_Newson_Implementation', 
                                 'MM_AR/Relevant_files',
                                 'LineString_Road_Network_UTM.shp')
    
    df = shuttle_data2dataframe(f)
    df = df[df['username']=='uconn%s' % bus_id].sort_index(0)
    trip = df[start:end]
    WGS84 = pyproj.Proj("+init=EPSG:4326")
    UTM18N=pyproj.Proj("+init=EPSG:32618")
    trnsfm = trip.apply(lambda t: pyproj.transform(WGS84, UTM18N, 
                                    t['longitude'], t['latitude']), 
                                    axis=1)
    eas, nor = zip(*trnsfm[:])
    
    fig = plt.figure()
    ax = plt.axes()
    plt.scatter(eas, nor, c=trip.index, cmap=plt.get_cmap("hot"),
                edgecolor='black', linewidth='0.5')
    val = Validate('')
    val.plot_roadnetwork(road_shp_file, ax, fig)
    plt.xlim(min(eas) - 200, 200 + max(eas))
    plt.ylim(min(nor) - 200, 200 + max(nor))
    plt.colorbar()
    plt.show()
    plt.close()
    return fig, trip[['longitude', 'latitude']]

def write_csv(os, bus_id, start, trip, route, tod):
    date = '%d%02d%02d' % (start.year, start.month, start.day)
    start_str = '%02d-%02d-%02d' % (start.hour - 4, start.minute, start.second)
    #end_str = '%02d-%02d-%02d' % (end.hour-4, end.minute, end.second)
    dow = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    file_name = '%s_%s_%s_%s_%s_%s.csv' % (route, dow[start.weekday()], 
        tod, bus_id, 
        date, start_str) #, end_str)
    save_path = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS', 
        r'Py Codes/HMM_Krumm_Newson_Implementation\MM_AR_validation', 
        'val_dataset')
    trip.to_csv(os.path.join(save_path, file_name))
    return save_path

if __name__ == '__main__':
    #######################################################
    #    March
    #######################################################
    fldr = os.path.join(r'C:\Users\asr13006\Desktop\Thesis', 
                        'Copy of Data Reservoir',
                        'March 2013\March_routes')
    bus_id = 202
    f = fldr+'/032629uconn{}.csv'.format(bus_id)
    #######################################################
    #    April
    #######################################################
    fldr = os.path.join(r'C:\Users\asr13006\Desktop\Thesis',
                        'Copy of Data Reservoir\April 2013')
    f = fldr + r'\20130418_40000-20130420_40000.csv'
    bus_id = 205
    
    #######################################################
    #    slide time window and visualize
    #######################################################
    start = datetime(2013, 3, 27, 16, 15, 10)
    end   = datetime(2013, 3, 27, 16, 50, 50)
    fig, trip = plot_seg(bus_id, f, start, end)
    #######################################################
    #    save csv
    #######################################################
    route = 'yl'
    tod = 'ev'
    save_path = write_csv(os, bus_id, start, trip, route, tod)
    #######################################################
    #    Plot all 
    #######################################################
    file_lst = [f for f in os.listdir(save_path) if os.path.isfile(save_path +
                                                                   '/' + f)]
    for f in file_lst:
        df = pd.read_csv(save_path + '/' + f)
        plt.scatter(df['longitude'], df['latitude'], c=df.index, 
                cmap=plt.get_cmap("hot"), edgecolor='black', linewidth='0.5')
        plt.title(f)
        plt.savefig(os.path.join(save_path, 'val_dataset_plot',   \
                                 f[:-4]+'.jpg'))
        plt.close()
    #######################################################
    #    Clean up username col 
    #######################################################
    file_lst = [f for f in os.listdir(save_path) if os.path.isfile(f)]
    df = pd.read_csv(file_lst[0])
    df.columns
    loc = os.path.abspath(os.path.join(os.path.dirname( os.getcwd() ), os.pardir, 
                                 'val_dataset - Copy'))
    del df['username']
    #######################################################
    #    utc dates in a March datafile
    #######################################################
    for f in [f for f in os.listdir(fldr) if  \
              f[:11]=='032629uconn' and f[-3:]=='csv']:
        try:
            df = shuttle_data2dataframe(os.path.join(fldr,f))
            df.sort_index(axis=0)
            #for unique values in a pd.df
            #print f[11:14], "==>>", pd.Series(df.index.date).unique()
            print f[11:14], "-->", df.index[0], "-->",df.index[len(df)-1]
        except:
            continue

    '''
    201 --> 2013-03-26 04:00:08 --> 2013-03-28 00:01:15
    202 --> 2013-03-26 04:08:55 --> 2013-03-28 20:20:27
    203 --> 2013-03-26 16:39:26 --> 2013-03-28 16:45:54
    204 --> 2013-03-26 04:00:02 --> 2013-03-28 03:58:52
    205 --> 2013-03-27 23:47:57 --> 2013-03-28 00:48:03
    206 --> 2013-03-26 09:58:49 --> 2013-03-28 03:59:55
    214 --> 2013-03-26 09:41:59 --> 2013-03-28 01:19:23
    215 --> 2013-03-26 09:50:43 --> 2013-03-27 23:01:41
    216 --> 2013-03-27 12:40:46 --> 2013-03-27 15:36:10
    227 --> 2013-03-26 12:28:01 --> 2013-03-27 23:21:19
    228 --> 2013-03-26 13:13:47 --> 2013-03-26 18:53:41
    229 --> 2013-03-26 04:00:08 --> 2013-03-27 20:38:25
    230 --> 2013-03-26 04:00:05 --> 2013-03-27 23:15:50
    231 --> 2013-03-26 09:49:59 --> 2013-03-28 03:59:54
    232 --> 2013-03-26 04:03:35 --> 2013-03-28 03:59:13
    '''
    dr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',  \
            'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR_validation',
            'val_dataset')
    files = [f for f in os.listdir(dr) if os.path.isfile(os.path.join(dr, f))]
    dirty_ones = [el for el in files if   \
                 pd.read_csv(os.path.join(dr, el)).columns[1] == 'username']
    for el in dirty_ones:
        df = pd.read_csv(os.path.join(dr, el), index_col=['utc_time_stamp'])
        del df['username']
        df.to_csv(os.path.join(dr, el))
    