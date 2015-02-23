'''
Created on Dec 7, 2014

@author: asif.rehan@engineer.uconn.edu
'''
import numpy as np
import pandas as pd
import MM_main
from dateutil.parser import parse
import pytz
import datetime
import fiona
from MM_AR.GPS_point_cand_point.GPS_point import lat_long_to_UTM_point
import  matplotlib.pyplot as plt
import os
class Validate(object):
    '''Validation class for MM algo'''
    def __init__(self, raw_shuttle_gps_file):
        self.csv_file = raw_shuttle_gps_file
        
    def timezone_converter(self, input_dt, target_tz='US/Eastern', 
                                            current_tz='UTC'):
        '''
        input_dt is an datetime.datetime object
        assumes timezone by default. See parameter values
        '''
        current_tz = pytz.timezone(current_tz)
        target_tz = pytz.timezone(target_tz)
        target_dt = current_tz.localize(input_dt).astimezone(target_tz)
        return target_tz.normalize(target_dt) 

    def create_csv_freq_x(self):
        data_pd = pd.read_csv(self.csv_file)
        return data_pd
    
    def create_parsed_local_time_col(self, data_pd):
        '''
        call the three column file as lean csv file
        '''
        selected_columns_df = data_pd[['latitude','longitude',  
                                       'utc_time_stamp']]
        selected_columns_df = selected_columns_df.sort('utc_time_stamp')
        selected_columns_df.reset_index(drop=True, inplace=True)
        selected_columns_df['local_time_parsed'] = ''
        
        for idx in range(len(selected_columns_df)):
            utc_parsed = parse(selected_columns_df[
                                'utc_time_stamp'].iloc[idx])             
            selected_columns_df.loc[idx, 'local_time_parsed'] = \
                self.timezone_converter(utc_parsed)
        return selected_columns_df 
    
    def create_time_delta_col(self, selected_columns_df):
        selected_columns_df['time_delta'] = ''
        selected_columns_df['time_delta'] = \
            selected_columns_df['local_time_parsed'].diff()
        return selected_columns_df
    
    def get_unique_dates(self, datetime_col):
        '''
        return the unique dates in the dataframe
        '''
        return datetime_col.map(pd.Timestamp.date).unique()
    
    def chunk_data(self, dataframe, start_dt_local, duration):
        '''
        returns data chunk for the given day
        duration in minutes
        
        Parameters
        ==========
        start_dt is datetime.datetime object
        '''
        end_dt_local = start_dt_local + duration
        start_dt_utc = self.timezone_converter(start_dt_local, 
                                target_tz='UTC', 
                                current_tz='US/Eastern') 
        end_dt_utc = self.timezone_converter(end_dt_local, 
                                target_tz='UTC', 
                                current_tz='US/Eastern') 
        
        start_dt_str = start_dt_utc.replace(tzinfo=None).isoformat()
        end_dt_str = end_dt_utc.replace(tzinfo=None).isoformat()
        
        dataframe = dataframe[dataframe['utc_time_stamp'] > start_dt_str]
        chunk = dataframe[dataframe['utc_time_stamp'] < end_dt_str]
        return chunk
        
    def resampler_for_desired_freq(self, chunk, frequency_second):
        '''
        Resamples from the time-chunked dataset to obtain desired frequency
        
        Parameters
        ==========
        frequency in seconds
        start_time = to be input as 'YYYY:mm:ddThh:mm:ss' 
        '''
        chunk_durn_sec = parse(chunk['utc_time_stamp'].max()) -  \
                    parse(chunk['utc_time_stamp'].min())
        start_index = chunk.index[0]
        median_freq = chunk['time_delta'].median()
        print 'frequency_second', frequency_second
        print 'median_freq', median_freq, type(median_freq) 
        jump = frequency_second / (median_freq.astype('timedelta64[s]'))
        print 'jump', jump
        up_to_row = start_index + (chunk_durn_sec.total_seconds() /  
                                                        jump)
        print 'up_to_row' ,up_to_row
        select_rows = range(start_index, chunk.index.max(), int(jump))
        print 'select_rows', select_rows
        #try: 
        resampled = chunk.ix[select_rows]
        return resampled
        #except IndexError:
        #    print 'try another frequency!'
        #    return None
        
    def mapmatch_resampled_chunk(self, resampled_chunk, gps_mean, gps_std_dev, 
                                road_net_shp,road_net_multigraph_pickled,
                                beta):
        csv_file = 'validation_output/Resampled_chunk_{}'.format(self.csv_file)
        resampled_chunk.to_csv(csv_file)
        try:
            map_matched = MM_main.Viterbi(csv_file, 
                            lon_col_id = 2, 
                            lat_col_id = 1, 
                            timestamp_col_id = 3, 
                            gps_mean = gps_mean, 
                            gps_std_dev = gps_std_dev, 
                            road_net_shp = road_net_shp, 
                            road_net_multigraph_pickled =  \
                                                road_net_multigraph_pickled,
                            beta = beta)
            return map_matched[1], map_matched[2]
        except TypeError:
            return None 
        
    def plot_roadnetwork(self, ax, fig, select=False, color='k',
            road_shp_file = os.path.join(os.path.dirname(__file__), os.pardir,
                    r"MM_AR/Relevant_files/LineString_Road_Network_UTM.shp"),
                         zorder=1):
        '''
        plots the road network with matplotlib
        fig = matplotlib.pyplot.figure()
        ax = matplotlib.pyplot.axes()
        id = optional, list of selected roads to be plotted
            
        '''
        
        with fiona.open(road_shp_file) as road_shp:
            if select == False:
                records = xrange(len(road_shp))
            else:
                records = select
            for i in records:                
                line = road_shp[i]['geometry']['coordinates']
                (line_easting, line_northing) = zip(*line)
                ax.plot(line_easting, line_northing, color=color,
                        linewidth=0.5, zorder=zorder)
                        
    def plot_map_matched_path_points(self, map_matched_seq, 
                                     ax, fig, label=None, zorder=3):
        '''
        fig = matplotlib.pyplot.figure()
        ax = matplotlib.pyplot.axes()
        '''
        (easting, northing) = zip(*map_matched_seq)
        plt.scatter(easting, northing, label=label, 
                c=range(len(map_matched_seq)), cmap=plt.get_cmap("hot"),
                zorder=zorder)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5, fontsize='x-small')
        plt.xlim(min(easting)-200, 200+max(easting))
        plt.ylim(min(northing)-200, 200+max(northing))
        
    def unzip_map_match_seq(self, map_match_seq):
        easting, northing = zip(*map_match_seq)
        return easting, northing
    
    
    def plot_quiver_seq(self, map_match_seq, ax, fig, zorder=2):
        '''
        only works when easting, northing both scaled between 0 to 1
        So may not be visualized with other methods on same axis due to 
        different range
        '''

        e, n = self.unzip_map_match_seq(map_match_seq)
        X = np.array([e, n]).T


        ax.quiver(X[:-1, 0], X[:-1, 1], 
                   X[1:, 0] - X[:-1, 0], 
                   X[1:, 1] - X[:-1,1], 
                   scale_units='xy', angles='xy', scale=1, zorder=zorder)
    
    

    def df_lat_lon2_utm_lst(self, chunk):
        utm_pts = map(lat_long_to_UTM_point, 
            chunk['longitude'], 
            chunk['latitude'])
        
        return utm_pts

    def plot_raw_gps_seq(self, chunk, ax, fig, legend='ro', label=None, 
                         zorder=4):
        '''
        fig = matplotlib.pyplot.figure()
        ax = matplotlib.pyplot.axes()
        '''
        utm_pts = self.df_lat_lon2_utm_lst(chunk)
        easting, northing = self.unzip_map_match_seq(utm_pts)
        ax.plot(easting, northing, legend, label=label)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5, fontsize='x-small')
        return min(easting), max(easting), min(northing), max(northing)
    
    def validation_main(self, start_time_local, end_time_local,  
                        road_net_shp, road_net_multigraph_pickled, 
                        gps_std_dev=30, beta=1, duration_minute=60, 
                        freq_sec=60):
        '''start_time_local and end_time_local are datetime.time object'''
        dur_td = datetime.timedelta(minutes=duration_minute)
        
        df = self.create_csv_freq_x()
        df = self.create_parsed_local_time_col(df)
        df = self.create_time_delta_col(df) 
        dates = self.get_unique_dates(df['local_time_parsed'])
        for tgt_date in dates:
            start_datetime = datetime.datetime(tgt_date.year, 
                                               tgt_date.month,
                                               tgt_date.day,
                                               start_time_local.hour,
                                               start_time_local.minute,
                                               start_time_local.second)
            end_datetime = datetime.datetime(tgt_date.year, 
                                               tgt_date.month,
                                               tgt_date.day,
                                               end_time_local.hour,
                                               end_time_local.minute,
                                               end_time_local.second)
            chunk_start_dt = start_datetime
            print 'chunk_start_dt', chunk_start_dt
            while chunk_start_dt < end_datetime :
                chunk_name = '{file}_{year}-{month}-{day}-'  \
                            '{hour}-{minute}-{second}_'  \
                            'dur{dur_min}min_freq{freq_sec}sec'.format(
                                            file=self.csv_file[:-4],
                                            year=chunk_start_dt.year,
                                            month=chunk_start_dt.month,
                                            day=chunk_start_dt.day,
                                            hour=chunk_start_dt.hour,
                                            minute=chunk_start_dt.minute,
                                            second=chunk_start_dt.second,
                                            dur_min=str(duration_minute),
                                            freq_sec=str(freq_sec))
                #print 'chunk_name =', chunk_name
                chunk = self.chunk_data(df, chunk_start_dt, dur_td)
                print chunk
                chunk.to_csv('chunk_{}.csv'.format(chunk_name))
                
                resampled_chunk = self.resampler_for_desired_freq(chunk, 
                                                                  freq_sec)
                print resampled_chunk
                resampled_chunk.to_csv('resampled_chunk_{}.csv'.
                                                    format(chunk_name))
                
                map_matched_seq = self.mapmatch_resampled_chunk(
                                            resampled_chunk, 
                                            gps_mean=0, 
                                            gps_std_dev=gps_std_dev, 
                                            road_net_shp=road_net_shp, 
                                            road_net_multigraph_pickled=  \
                                                road_net_multigraph_pickled,
                                            beta=beta)
                fig = plt.figure()
                ax = plt.axes()
                self.plot_roadnetwork(road_net_shp, ax, fig)
                (east_min, east_max, north_min, north_max) =  \
                        self.plot_raw_gps_seq(chunk, ax, fig, legend='cx', 
                                              label='chunk')
                
                self.plot_map_matched_path_points(map_matched_seq[1], ax, fig,
                                                  label='map-matched')
                self.plot_raw_gps_seq(resampled_chunk, ax, fig, legend='rH',
                                      label='re-sampled chunk')
                plt.xlim(east_min-200, 200+east_max)
                plt.ylim(north_min-200, 200+north_max)
                fig.suptitle(chunk_name, fontsize=10, fontweight='bold')
                fig.savefig('validation_output/plot_{}'.format(chunk_name))
                plt.close()
                
                #while loop control condition
                chunk_start_dt = min(chunk_start_dt + dur_td, end_datetime)
                        
        return None
'''    
if __name__ == '__main__':
    import sys
    lab_rat = '032629uconn231.csv'
    val = Validate(lab_rat)
    start_time_local = datetime.time(15,30,0)
    end_time_local = datetime.time(16,30,0,)
    road_net_shp = '../MM_AR/Relevant_files/LineString_Road_Network_UTM.shp'
    road_net_multigraph_pickled = "../MM_AR/Preprocess/MultiGraph.p"
    
    for lab_rat_id in [231]:
        sys.stdout= open('validation_output/output_032629uconn{}.txt'.format(
                                                            lab_rat_id), 'w')
        for freq_sec in [10]:#, 15, 20, 30, 34, 30, 60]:
            try:
                val.validation_main(start_time_local, end_time_local,  
                                road_net_shp, road_net_multigraph_pickled,
                                gps_std_dev=30, beta=1, duration_minute=30, 
                                freq_sec=freq_sec)
            except AttributeError: 
                continue
        sys.stdout.close()'''