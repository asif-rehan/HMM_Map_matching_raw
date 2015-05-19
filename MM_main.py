from MM_AR.GPS_point_cand_point.GPS_point import ObsPoint 
from MM_AR.HMM_procedure.transition_weight \
    import TransitionWeight
import pickle
import numpy as np
import pandas as pd
from MM_AR.HMM_procedure.ReadFile import read_data_point
import time
import sys
import os


this_dir =  os.path.dirname(__file__)


#sys.stdout=open('output_{0}_{1}.txt'.format(time.strftime('%Y-%m-%dT%H.%M.%S', 
#                                            time.localtime()), 
#                                            'orng_20141014'), 'w')

#tart_time = time.time()

def Viterbi(datafile, lon_col_id, lat_col_id, timestamp_col_id, 
            gps_mean=0, gps_std_dev=7, circ_radius=30,
            road_net_shp = os.path.join(this_dir,
                    "MM_AR/Relevant_files/LineString_Road_Network_UTM.shp"),
            road_net_multigraph_pickled = os.path.join(this_dir,
                                        r"MM_AR/Relevant_files/MultiGraph.p"),
            beta=1): 
    '''
    Viterbi decoder of optimum sequence of the candidate road segments.
    Input file should be a csv file with at least three columns for 
    Latitude, Longitude and Time stamp.  

    Parameters
    ==========
    lon_col_id, lat_col_id, timestamp_col_id  are the column numbers counting 
    from left column as zero
    
    Known implementation limitations
    =================================
    1. If the path finder process breaks for two consecutive points then it 
    does not remove them from the sequence as Newson and Krumm did manually.
    
    2. Emission probability does not incorporate the general definition
    for emission probability by Oran and Jaillet (2013)
     
    3. Performance not optimized
    '''   
    #print "MAIN RUNS"
     
    MultiGraph = pickle.load(open(road_net_multigraph_pickled, 'rb'))
    #pointgen for phones
    #PointGenerator = read_data_point(datafile, lon_col_id=5, 
    #                              lat_col_id=4, timestamp_col_id=9)
    #pointgen for whole day data
    PointGenerator = read_data_point(datafile, lon_col_id, 
                                   lat_col_id, timestamp_col_id)
    record = 0
    points = []    
    try:
        for GPSrecord in PointGenerator:
#            print 'rec ', record
            if record == 0:   
                #print "IF starts"
                #print 'rec ', record     
                p1 = ObsPoint( gps_lon = GPSrecord[0], 
                               gps_lat = GPSrecord[1],
                               timestamp = GPSrecord[2], 
                               gps_mean = gps_mean, 
                               gps_std_dev = gps_std_dev,
                               circ_radius= circ_radius, 
                               road_net_shp = road_net_shp )
                
                if len(p1.candidate_points) == 0:
                    #print 'ignore first works!'
                    record = 0 
                    continue
                
                points.append(p1)
                
                #print 'print len(points)',len(points)
                #print 'len p1.candidate points', len(p1.candidate_points)
                
                lnHeadProbVec = np.empty(shape=[0, 1]) #initiate as list. from 2nd GPS 
                                                #point, becomes NumPy array
                WaveHead = []
                WaveHead_dist = []  
                WaveHead_rd_id_len = []          
                for cand_pt_0 in points[record].candidate_points:
                    lnHeadProbVec = np.append(lnHeadProbVec,
                              [[np.log(cand_pt_0.cand_pt_emission_prob)]], 
                              axis = 0)
                    #WaveHead.append(None)
                    WaveHead.append([(cand_pt_0.cand_pt_easting, 
                                     cand_pt_0.cand_pt_northing, 
                                      cand_pt_0.cand_pt_timestamp)])
                    WaveHead_dist.append(0)
                    WaveHead_rd_id_len.append([])
                    #print (cand_pt_0.cand_pt_easting, cand_pt_0.cand_pt_northing)
                #print "lnHeadProbVec", lnHeadProbVec
                #print "WaveHead", WaveHead
                #print 'IF END'
            
            elif record > 0:
                #print "ELIF START"            
                
                if record > 1:
                    del(points[0])
                
                p2 = ObsPoint( gps_lon = GPSrecord[0], 
                               gps_lat = GPSrecord[1],
                               timestamp = GPSrecord[2], 
                               gps_mean = gps_mean, 
                               gps_std_dev = gps_std_dev, 
                               circ_radius= circ_radius, 
                               road_net_shp = road_net_shp )  
                points.append(p2)
                #for p in points:
                    #print 'GPS point', p.gps_easting, p.gps_northing
                row_len = len(points[0].candidate_points)
                col_len = len(points[1].candidate_points)
#                print "(row_len, col_len) = (", row_len, col_len, ")"
                
                
#                for pos in xrange(row_len):
#                    print ('points[0]',
#                    points[0].candidate_points[pos].cand_pt_easting,
#                            points[0].candidate_points[pos].cand_pt_northing) 
#                for pos in xrange(col_len):
#                    print ('points[1]',
#                    points[1].candidate_points[pos].cand_pt_easting,
#                            points[1].candidate_points[pos].cand_pt_northing)
                
                #check and remove the points with no candidate points or if it is 
                # the same as the immediately previous point
                #==============================================================
                # if points[0] == points[1] or col_len == 0:
                #     #print 'ignore current!'
                #     record += 1
                #     points[1] = points[0] 
                #     continue
                #==============================================================
                
                #print (p2.__dict__)          
                #print 'len p2.candidate points', len(p2.candidate_points)
                #print 'print len(points)', "*"*len(points)
                
                TransitionObjMatrix = np.empty_like([[0]*col_len]*row_len, 
                                                    TransitionWeight)
                TransWeightMatrix = np.empty([row_len,col_len], dtype = float)
                lnEmissionProbMatrix = np.empty(col_len, dtype=float)
                #array(cand_pt_t_minus_1  X cand_pt_t)
                #print "len(points[1].candidate_points) = ",  \
                #                len(points[1].candidate_points)
                #print "len(points[0].candidate_points) = ",  \
                #                len(points[0].candidate_points)
                i = 0
                for cand_pt_t in points[1].candidate_points:
                    
                    j = 0
                    lnEmissionProbMatrix[i] = np.log(   
                                               cand_pt_t.cand_pt_emission_prob)
                    for cand_pt_t_minus_1 in points[0].candidate_points:
                        TransitionObjMatrix[j][i] = TransitionWeight(
                                                        cand_pt_t_minus_1, 
                                                        cand_pt_t, MultiGraph, 
                                                        road_net_shp, beta)
                        #######################################################
                        # check for a column completely filled with alien pt
                        #######################################################                                            
                        TransWeightMatrix[j][i] =   \
                                        TransitionObjMatrix[j][i].transition_wt 
                        #(jXi)matrix
                        #print "j = ", j
                        j += 1
                    #print "i = ", i
                    i += 1
                
                if TransWeightMatrix.max() == 0:
                    record += 1
                    points[1] = points[0] 
                    continue
                
#               print "TransWeightMatrix",TransWeightMatrix
#                print record, "EmissionProbMatrix",lnEmissionProbMatrix
                try:
                    
                    sum_row_wt = np.sum(TransWeightMatrix, axis=1)
                    for i in range(row_len):
                        if sum_row_wt[i-1] == 0:
                            sum_row_wt[i-1] = 1.0
                    ln_sum_row_wt = np.log(sum_row_wt)
                                                    #(1xj)),   log(sum(row))
                #for i in range(row_len): 
                #    if log_sum_row_wt[i]  == float('inf'):
                #        log_sum_row_wt[i] = 0
                        #handles divide by zero and overflow warning
                #    print 'record# before crashpoint',record
                    p = np.log(TransWeightMatrix).transpose()
                    lnTransProbMatrix = (p - ln_sum_row_wt).transpose()
                    
                except RuntimeWarning:
                    print RuntimeWarning
                #    print 'p=', p, 'record=', record
                
#                print "log_sum_row_wt \n", ln_sum_row_wt
#                print "lnTransProbMatrix \n", lnTransProbMatrix
                
                
                lnHTE = lnHeadProbVec + lnTransProbMatrix +lnEmissionProbMatrix
#                print 'lnHTE\n', lnHTE
                lnHeadProbVec = np.max(lnHTE, axis = 0).reshape(
                                                            (lnHTE.shape[1],1)) 
                if lnHeadProbVec.max() == -float('inf'):
                    break
                
                #head prob values
                #find the row-column positions of the maximum values for 
                #max-probable cand_pt_t
#                print "lnHeadProbVec \n", lnHeadProbVec
                
                WaveHead_temp = []
                WaveHead_dist_temp = []
                WaveHead_rd_id_len_temp = []
                lnHTE_trnsps = np.transpose(lnHTE)
                for col_argmax in xrange(col_len):
                    row_argmax = np.argmax(lnHTE_trnsps[col_argmax])
                    bridge = TransitionObjMatrix[row_argmax][col_argmax].\
                                                            sp_nodes
                    bridge_dist = TransitionObjMatrix[row_argmax][col_argmax].\
                                                            sp_len
                    bridge_rd_id_len =   \
                                TransitionObjMatrix[row_argmax][col_argmax].\
                                                            sp_rd_id_len
#                    print 'bridge', bridge, bridge_dist
                    if record == 1:
                        WaveHead_temp.append(bridge)
                        WaveHead_dist_temp.append(WaveHead_dist[row_argmax] + 
                                                                bridge_dist)
                        WaveHead_rd_id_len_temp.append(bridge_rd_id_len)
                    elif lnHeadProbVec[col_argmax] == 0:
                        WaveHead_temp.append('out of network')
                    
                    else:
                        WaveHead_temp.append(WaveHead[row_argmax]+bridge[1:])
                        WaveHead_dist_temp.append(WaveHead_dist[row_argmax] + 
                                                                bridge_dist)
                        WaveHead_rd_id_len_temp.append(
                                            WaveHead_rd_id_len[row_argmax] + 
                                                            bridge_rd_id_len)
                WaveHead = WaveHead_temp
                WaveHead_dist = WaveHead_dist_temp
                WaveHead_rd_id_len = WaveHead_rd_id_len_temp
#                print "WaveHead"
#                print zip(WaveHead_dist, WaveHead)
                
            record += 1
            
        max_prob = np.max(lnHeadProbVec)
        pick_max = np.argmax(lnHeadProbVec)
        max_prob_path = WaveHead[pick_max]
        max_prob_path_dist = WaveHead_dist[pick_max]
        max_prob_path_rd_id_len = WaveHead_rd_id_len[pick_max]
      
        edge_output_df = pd.DataFrame(max_prob_path_rd_id_len, 
                     columns=['road_id', 'length'])
        node_output_df = pd.DataFrame(max_prob_path, 
                                      columns=[ 'easting', 'northing', 
                                                'timestamp', 
                                                'node_id'   ])
        
#        print " max_prob_path  \n", max_prob_path
#        print "\n max_prob  ", max_prob
#        print "\n max_prob_dist  ", max_prob_path_dist
#        print "\n max_prob_dist  ", max_prob_path_rd_id_len
#        print "\n node_outout  = \n ", node_output_df, '\n'
#        print "\n edge_outout  = \n ", edge_output_df

        return max_prob, max_prob_path_dist,   \
                node_output_df, edge_output_df
    
    except UnboundLocalError:
#        print 'Stationary object'
        return None
        
    #assumption: no tied value for likelihood calculation

#print "--- {0} seconds ---".format(time.time() - start_time)

if __name__ == '__main__':
    out = Viterbi(datafile="MM_AR/Relevant_files/phnGPS_orng.csv",
        lon_col_id=5, lat_col_id=4, timestamp_col_id=9,
        gps_mean = 0, gps_std_dev=7, circ_radius=30,
        road_net_shp = "MM_AR/Relevant_files/LineString_Road_Network_UTM.shp",
        road_net_multigraph_pickled = "MM_AR/Relevant_files/MultiGraph.p",
        beta=1)
    print out[2], "\n", out[3] 
#    print "--- {0} seconds ---".format(time.time() - start_time)
sys.stdout.close()
sys.stderr = sys.__stderr__
