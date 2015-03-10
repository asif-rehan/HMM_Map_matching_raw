'''
Created on Mar 9, 2015

@author: asr13006
'''
from MM_AR_validation.validation import Validate as val
from matplotlib import pyplot as plt
import pandas as pd
import os

class AllDatasetQuiverPlot(object):    
    def all_dataset_quiver_plot(self, out_fldr, src_fldr, src_file):
        
        chunk = pd.read_csv(os.path.join(src_fldr, src_file))
        fig = plt.figure()
        ax = plt.axes()
        v = val('')
        v.plot_raw_quiver(chunk, fig, ax)
        plt.title(src_file[:-4])
        plt.savefig(os.path.join(out_fldr, src_file[:-4]+'_qvr'+'.png'))
        plt.close()
    
    

if __name__ == '__main__':
    out_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
      r'Py Codes/HMM_Krumm_Newson_Implementation\MM_AR_validation\val_dataset',
      'val_dataset_plot')
    src_fldr = os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
      r'Py Codes\HMM_Krumm_Newson_Implementation\MM_AR_validation\val_dataset')
    src_files = [f for f in os.listdir(src_fldr)   \
                 if os.path.isfile(os.path.join(src_fldr, f))]
    graph_klass = AllDatasetQuiverPlot()
    for src_file in src_files:
        graph_klass.all_dataset_quiver_plot(out_fldr, src_fldr, src_file)
        