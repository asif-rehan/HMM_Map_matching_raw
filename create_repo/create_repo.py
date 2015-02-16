'''
Created on Jan 4, 2015

@author: asr13006
'''
from shapely.geometry import LineString, Point



class CreateRepo(object):
    '''
    create historical database from shuttle GPS
    '''


    def __init__(self, datafile):
        '''
        Constructor
        '''
        def snapper(self, coords ,std_dev):
            pt = Point(coords[0], coords[1])
            buff = pt.buffer(std_dev)
            