'''
Created on Feb 13, 2015

@author: asr13006
'''
import os
import pandas as pd
from matplotlib import pyplot as plt
def plt_err_vs_freq_on_route(dataframe, xvar, yvar, var3, 
                             col, mar, leg):
    uniq_var3 = dataframe[var3].unique()
    for uniq in uniq_var3:
        subset = dataframe[dataframe[var3] == uniq]
        plt.scatter(subset[xvar], subset[yvar], 
             color=col[uniq], marker=mar[uniq], alpha=0.75, label=leg[uniq])
    plt.legend(loc=10, bbox_to_anchor=(1.05, 0.5),
          fancybox=True, shadow=True, ncol=1, 
          fontsize='x-small')
    if yvar == 'Error':
        plt.axhline(y=0,xmin=0,xmax=65,c="k",linewidth=0.5,zorder=0)
    if yvar == 'Score':
        plt.axhline(y=100,xmin=0,xmax=65,c="k",linewidth=0.5,zorder=0)
    plt.title('%{} vs Frequency for {}'.format(yvar, var3))
    plt.xlabel('Frequency')
    plt.ylabel('%{}'.format(yvar))
    plt.show()

out_fldr = os.path.join(r'C:\\Users\\asr13006\\Google Drive\\UConn MS',
            r'Py Codes/HMM_Krumm_Newson_Implementation\\MM_AR_validation',
            r'val_graphs')
#out = os.path.join(out_fldr, "quant_val_out2.csv")
#x = pd.read_csv(out)
#x = x.drop(x.index[[9,18]])
#x = x.drop('Unnamed: 0', 1)


##########################################################################
#     OLD 
##########################################################################
seg1 = 'server1_output_20150225T232216.csv'
seg2 = 'server2_output_20150226T072402.csv'
df1 = pd.read_csv(os.path.join(out_fldr, seg1))
df2 = pd.read_csv(os.path.join(out_fldr, seg2))
all_but4 = df1.append(df2)

##########################################################################
#     VERSION 1.0
##########################################################################
out_datafile = 'version1.0_output_20150316T235427.csv'
out_df = pd.read_csv(os.path.join(out_fldr, out_datafile))
'''
for cat in ['Freq' ,'Route', 'DOW', 'TOD']:
    for metric in ['Error', 'Score']:
        fig = plt.figure()
        ax = plt.axes()
        plt.title('{} for {}'.format(metric, cat) )
        for uniq in [cat].unique():
            seg_data = dataframe[dataframe[cat] == uniq]
            ax.plot(seg_data[metric].values, label=uniq)
            print seg_data.head(2)
            print  seg_data.tail(2)  
            
            plt.legend()
        plt.savefig(os.path.join(r'C:\Users\asr13006\Google Drive',
                        r'UConn MS\Py Codes\HMM_Krumm_Newson_Implementation',
                        r'MM_AR_validation\val_graphs', 
                        '{}_{}.png'.format(metric, cat)))
        plt.show()'''
##########################################################################
#     V3 = ROUTE
##########################################################################

col_rt = {'bl': 'b', 'rd':'r', 'gr':'g', 'yl':'y', 'or':'#FFA500','pl':'#7F00FF'}
mar_rt = {'bl': 'x', 'rd':'+', 'gr':'d', 'yl':'s', 'or':'o','pl':'^'}
leg_rt = {'bl': 'Blue Line', 'rd':'Red Line', 'gr':'Green Line', 
          'yl':'Yellow Line', 'or':'Orange Line','pl':'Purple Line'}

#     OLD 
#=========    
plt_err_vs_freq_on_route(all_but4, xvar='Freq', yvar='Error', var3='Route')
plt_err_vs_freq_on_route(all_but4, xvar='Freq', yvar='Score', var3='Route')
#     VERSION 1.0
#================
plt_err_vs_freq_on_route(out_df, xvar='Freq', yvar='Error', var3='Route', 
                         col_rt, mar_rt, leg_rt)
plt_err_vs_freq_on_route(out_df, xvar='Freq', yvar='Score', var3='Route',
                         col=col_rt, mar=mar_rt, leg=leg_rt)

##########################################################################
#     V3 = DOW
##########################################################################
col_dow = {'tue':'#2eb7ed', 'wed':'#fee529', 'thu':'#cd4236'}
mar_dow = {'tue':'^', 'wed':'o', 'thu':'s'}
leg_dow = {'tue':'Tuesday', 'wed':'Wednesday', 'thu':'Thursday'}
'''
for dow in all_but4['DOW'].unique():
        subset = all_but4[all_but4['DOW'] == dow]
        plt.scatter(subset['Freq'], subset['Error'], 
             color=col[dow], marker=mar[dow], label=leg[dow])
plt.legend()
plt.axhline(y=0,xmin=0,xmax=65,c="k",linewidth=0.5,zorder=0)
plt.title('%Error vs Frequency for Dates of Week')
plt.xlabel('Frequency')
plt.ylabel('%Error')
plt.show()
'''
#     OLD 
#=========
   
plt_err_vs_freq_on_route(all_but4, xvar='Freq', yvar='Score', var3='DOW')
#     VERSION 1.0
#================
plt_err_vs_freq_on_route(out_df, xvar='Freq', yvar='Score', var3='DOW',
                         col=col_dow, mar=mar_dow, leg=leg_dow)
plt_err_vs_freq_on_route(out_df, xvar='Freq', yvar='Error', var3='DOW',
                         col=col_dow, mar=mar_dow, leg=leg_dow)

##########################################################################
#     V3 = TOD
##########################################################################

col_tod = {'mo':'grey', 'af':'red', 'ev':'cyan'}
mar_tod = {'mo':'x', 'af':'*', 'ev':'+'}
leg_tod = {'mo':'Morning', 'af':'Afternoon', 'ev':'Evening'}
'''
for tod in all_but4['TOD'].unique():
        subset = all_but4[all_but4['TOD'] == tod]
        plt.scatter(subset['Freq'], subset['Error'], 
             color=col[tod], marker=mar[tod], label=leg[tod], alpha=0.5)
plt.legend()
plt.axhline(y=0,xmin=0,xmax=65,c="k",linewidth=0.5,zorder=0)
plt.title('%Error vs Frequency for Time of Day')
plt.xlabel('Frequency')
plt.ylabel('%Error')
plt.show()
'''
#     VERSION 1.0

#================
plt_err_vs_freq_on_route(out_df, xvar='Freq', yvar='Error', var3='TOD',
                         col=col_tod, mar=mar_tod, leg=leg_tod)

plt_err_vs_freq_on_route(out_df, xvar='Freq', yvar='Score', var3='TOD',
                         col=col_tod, mar=mar_tod, leg=leg_tod)










