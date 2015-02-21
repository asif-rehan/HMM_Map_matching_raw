'''
Created on Feb 5, 2015

@author: asif.rehan@engineer.uconn.edu
'''
import MM_main
import os
import pandas as pd
from collections import Counter
import sys
import traceback 
import time
from matplotlib import pyplot as plt

def check_consistency(file_lst):
    
    rout = Counter([title[0:2] for title in file_lst]).most_common()
    dow  = Counter([title[3:6] for title in file_lst]).most_common()
    tod  = Counter([title[7:9] for title in file_lst]).most_common()
    return rout, dow, tod

def total_obs_line(src_files_list):
    tot = reduce(lambda x, y: x+y  , 
           [len(pd.read_csv(os.path.join(src_fldr, f))) for f in src_files])
    return tot

def get_ckt_len(rt):
    lengths_m = {'bl': 9020.7896425582585, 
                 'pl': 16352.730596927651, 
                 'yl': 9991.1998375839721, 
                 'gr': 10439.471668776407, 
                 'or': 5107.5327282622065, 
                 'rd': 7138.3470176287283}
    return lengths_m[rt]

def diagnostic_plot(mm_seq, label, out_fldr, src_file, freq):
    from validation import Validate as Val
    val = Val("")
    fig = plt.figure()
    ax = plt.axes()
    
    val.plot_map_matched_path_points(mm_seq, ax, fig, label)
    val.plot_roadnetwork( ax, fig)
    easting, northing = zip(*mm_seq)
    plt.xlim(min(easting)-200, 200+max(easting))
    plt.ylim(min(northing)-200, 200+max(northing))
    plt.savefig(os.path.join(out_fldr, src_file[:-4]+str(freq)+'.png'))
    val.plot_quiver_seq(mm_seq, ax, fig)
    return None

def err_val(src_fldr, src_file, out_fldr, des_freq=None):
    df = pd.read_csv(os.path.join(src_fldr, src_file), 
                     parse_dates=['utc_time_stamp'], 
                     index_col='utc_time_stamp')
    df.sort_index(axis=0, inplace=True)
    med_freq = pd.Series(df.index).diff().median()
    med_freq_fl = float(med_freq.values.astype('float64')/1e9)
    
    if des_freq == None:
        des_freq = int(med_freq_fl)
    
    jump = int(round(des_freq/med_freq_fl))
    out_file = src_file[:-4]+'_freq{}'.format(des_freq)+'.csv'
    df[::jump].to_csv(os.path.join(out_fldr, out_file))

    mm_out = MM_main.Viterbi(os.path.join(out_fldr, out_file), 
                        lon_col_id=1, 
                        lat_col_id=2, 
                        timestamp_col_id=0,
                        gps_mean=0, gps_std_dev=7, circ_radius=30)
    print mm_out
    diagnostic_plot(mm_out[2], src_file[:-4], out_fldr, src_file, des_freq)
    trav_len = get_ckt_len(out_file[:2])
    err = (mm_out[1] - trav_len)/trav_len*100
    err = round(err, 2)
    score = 100 - abs(err)
    return err, score, med_freq_fl

def quant_score(src_files, src_fldr, out_fldr, des_freq_lst,):
    tab = pd.DataFrame(columns=['Freq', 'Route', 'DOW', 'TOD', 
                                'Error', 'Score','File'])
    for des_freq, src_file in [(i,f) for i in des_freq_lst for f in src_files]:
        try:
            err, score, med_freq_fl = err_val(src_fldr, src_file, 
                                              out_fldr, des_freq)
            if des_freq == None: 
                des_freq = med_freq_fl
            tab = tab.append([{ 'Freq'      :   des_freq, 
                                'Route'     :   src_file[0:2],
                                'DOW'       :   src_file[3:6], 
                                'TOD'       :   src_file[7:9],
                                'Error'     :   err,
                                'Score'     :   score,
                                'File'      :   src_file}], 
                                ignore_index=True)
            print tab.tail(1)
        except TypeError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
            continue
        finally:
            output_file ='output_{0}.csv'.format(time.strftime('%Y%m%dT%H%M%S', 
                                            time.localtime()))
            tab.to_csv(os.path.join(out_fldr, output_file))
    return tab



    
if __name__ == "__main__":

    out_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
      r'Py Codes/HMM_Krumm_Newson_Implementation\MM_AR_validation\val_dataset',
      'val_dataset_output')
    src_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
      r'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR_validation\val_dataset')
    src_files = [f for f in os.listdir(src_fldr)   \
                 if os.path.isfile(os.path.join(src_fldr, f))]
    src_files = src_files[0:6]
    #print err_val(src_fldr, src_file, out_fldr, des_freq=900)
    try:
        sys.stdout = open(os.path.join(out_fldr, "sys.stdout.txt"), 'w')
        print quant_score(src_files, src_fldr, out_fldr, 
                      des_freq_lst=[60, 45, 30, 20, 10])
    finally:
        sys.stdout.close()
        sys.stderr = sys.__stderr__
    