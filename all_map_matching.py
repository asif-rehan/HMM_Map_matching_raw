'''s
Created on May 18, 2015

@author: asr13006
'''
import os
import pandas as pd
from MM_main import Viterbi

if __name__ == "__main__":
    out_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                r'Py Codes\ETA_KRR\_files\ETA_map_matched_files')
    src_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
      r'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR_validation\val_dataset')
    src_files = [f for f in os.listdir(src_fldr)   \
                     if os.path.isfile(os.path.join(src_fldr, f))]
        
    for f in src_files:
        datafile = os.path.join(src_fldr, f)
        ret = Viterbi(datafile, lon_col_id=1, lat_col_id=2, timestamp_col_id=0,
                      )
        ret[2].to_csv(os.path.join(out_fldr , 'node_' + f))
        ret[3].to_csv(os.path.join(out_fldr , 'edge_' + f))