'''
Created on Feb 13, 2015

@author: asr13006
'''
import os
import pandas as pd
from matplotlib import pyplot as plt
out_fldr = r'C:\\Users\\asr13006\\Google Drive\\UConn MS\\Py Codes/HMM_Krumm_Newson_Implementation\\MM_AR_validation\\val_dataset\\val_dataset_output'
out = os.path.join(out_fldr, "quant_val_out2.csv")
x = pd.read_csv(out)
x = x.drop(x.index[[9,18]])
x = x.drop('Unnamed: 0', 1)

fig = plt.figure()
ax = plt.axes()

for cat in x.Freq.unique():
    tod_data = x[x.Freq == cat]
    ax.plot(tod_data['Error'].values, label=cat)
    print tod_data
    plt.title('Error for various Freq')
    plt.legend()
plt.savefig(os.path.join(r'C:\Users\asr13006\Google Drive\UConn MS',
                             r'Py Codes\HMM_Krumm_Newson_Implementation',
                             r'MM_AR_validation\val_graphs', \
                             'bl_freq_error.png'))
plt.show()
