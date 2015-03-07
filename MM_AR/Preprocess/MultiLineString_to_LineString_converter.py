'''
input = shapefile with both LineString and MultiLineString features
output = shapefile with only LineString features

converts each of the component LineStrings in a MultiLineString features into an 
individual LineString feature
'''

# open the original shapefile
import fiona, os
from shapely.geometry import mapping, shape

wrkdir = "C:/Users/asr13006/Desktop/Thesis/Copy of Data Reservoir/routes/County 13/\
road network micro/nxspatial3/NF"
print wrkdir
os.chdir(wrkdir)
original = "SpliLinesAtVertices.shp"
source_path = os.path.join(os.getcwd(), original)
destination = os.path.join(os.getcwd(),'copy',"SpliLinesAtVertices-copy.shp")
with fiona.open(source_path) as source:
    # create the GPS_point_cand_point shapefile
    with fiona.open(destination,'w', driver='ESRI Shapefile',
                    crs=source.crs,schema=source.schema) as ouput:
        # iterate the features of the original shapefile
        for elem in source:
            # iterate the list of geometries in one element (split the MultiLineString)
            reconstruct = shape(elem['geometry']) 
            if elem['geometry']['type'] == 'MultiLineString':
                for line in reconstruct: 
                    # write the line to the GPS_point_cand_point shapefile
                    ouput.write({'geometry':mapping(line),
                                 'properties':elem['properties']})
            elif elem['geometry']['type'] == 'LineString':
                ouput.write({'geometry':mapping(reconstruct),
                             'properties':elem['properties']})
                
                
