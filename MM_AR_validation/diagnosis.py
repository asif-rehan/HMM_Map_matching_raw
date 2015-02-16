'''
Created on Feb 16, 2015

@author: asr13006

Diagnosis of Viterbi. Relevant_files orng datafile
'''
from matplotlib import pyplot as plt
import numpy as np

ax = plt.axes()

ax.plot(728461.183075588, 4631753.351893077, 'ro', zorder=100)
ax.annotate("t=0 cp1",xy=(728461.183075588, 4631753.351893077), 
            xytext=(-40,20), textcoords='offset points')
ax.plot(728481.1384234718, 4631771.503874317, 'ro', zorder=100)
ax.annotate("t=0 cp2",xy=(728481.1384234718, 4631771.503874317), 
            xytext=(-40,20), textcoords='offset points')
ax.plot(728675.4414764805, 4631879.223877374, 'ro', zorder=100)
ax.annotate("t=0 cp1",xy=(728675.4414764805, 4631879.223877374), 
            xytext=(20,20), textcoords='offset points')
bridge = [(728461.183075588, 4631753.351893077), (728418.4471356437, 4631714.499849313), (728418.4471356437, 4631714.499849313), (728481.1384234718, 4631771.503874317), (728544.1972221225, 4631828.679746407), (728579.9923637034, 4631860.566779728), (728633.538580009, 4631908.460396009), (728762.6295774302, 4631843.016164692), (728418.4471356437, 4631714.499849313), (728675.4414764805, 4631879.223877374)]
e, n = zip(*bridge)
e = np.array([e]).T
n = np.array([n]).T
ax.quiver(e[:-1], n[:-1], e[1:]-e[:-1], n[1:]-n[:-1], 
          scale=1, scale_units='xy', angles='xy')
ax.scatter(e, n, c=range(len(bridge)), cmap=plt.get_cmap(), zorder=10)
for (x,y) in bridge:
    ax.annotate("bridge #{}".format(bridge.index((x,y))), xy=(x,y), 
            xytext=(-90,-10), textcoords='offset points')
plt.show()