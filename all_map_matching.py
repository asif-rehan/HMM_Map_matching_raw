'''
Created on May 18, 2015

@author: asr13006
'''
import os, sys, time
from MM_main import Viterbi

if __name__ == "__main__":
    out_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                r'Py Codes\ETA_KRR\_files\ETA_map_matched_files')
    src_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
      r'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR_validation\val_dataset')
    src_files = [f for f in os.listdir(src_fldr)   \
                     if os.path.isfile(os.path.join(src_fldr, f))]
        
    for f in src_files[25:26]:
    #f = 'yl_wed_ev_206_20130327_16-35-10.csv'
        datafile = os.path.join(src_fldr, f)
            
        #sys.stdout=open('output_{0}_{1}.txt'.format(time.strftime('%Y-%m-%dT%H.%M.%S', 
        #                                        time.localtime()), 
        #                                        'fc,khckhccl'), 'w')
    
        ret = Viterbi(datafile, lon_col_id=1, lat_col_id=2, timestamp_col_id=0)
            #road_net_shp=r"C:\Users\asr13006\Google Drive\UConn MS\Py Codes\ETA_KRR\_files/LineString_Road_Network_UTM.shp",           
            #road_net_multigraph_pickled = r"C:\Users\asr13006\Google Drive\UConn MS\Py Codes\ETA_KRR\_files\ETA_MultiGraph.p")
        print ret[2]
        print ret[3] 
                      
        #ret[2].to_csv(os.path.join(out_fldr , 'node_whole_' + f))
        #ret[3].to_csv(os.path.join(out_fldr , 'edge_whole _' + f))
        
    #sys.stdout.close()
    #sys.stderr = sys.__stderr__
    