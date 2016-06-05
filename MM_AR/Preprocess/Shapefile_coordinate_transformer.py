
import fiona, pyproj
from fiona.crs import from_string
from shapely.geometry import LineString, mapping


def linestring_shapefile_coordinate_transformer(source_file, destination_file):  
    '''
    input = shapefile with only LineString features in WGS84 (GPS, Google Earth files)
    output = shapefile with only LineString features in UTM18N
    Also adds a GPS_point_cand_point field, Length_meter, to store the length of each LineString feature
    '''
    
    UTM18N = from_string('+proj=utm +zone=18T +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
    
                
    with fiona.open(source_file, driver= 'ESRI Shapefile', crs='WGS84') as source:
        schema_copy = source.schema
        schema_copy['properties'].update({'Length_meter': 'float'})
        transformed_schema = schema_copy
       
        with fiona.open(destination_file,'w', driver='ESRI Shapefile',
                    crs=UTM18N,schema=transformed_schema) as transformed:

            for elem in source:
                LineString_vertices = elem['geometry']['coordinates']
                lon, lat  = zip(*LineString_vertices) #lon = X, lat = Y
                WGS84 = pyproj.Proj("+init=EPSG:4326")
                UTM18N=pyproj.Proj("+init=EPSG:32618")
                easting, northing = pyproj.transform(WGS84, UTM18N, lon, lat)
                transformed_LineString_vertices = zip(easting, northing)
                tranfrormed_linestring = LineString(transformed_LineString_vertices)
                length = LineString(transformed_LineString_vertices).length
                                
                elem['properties'].update({'Length_meter': length})

                transformed.write({'geometry':mapping(tranfrormed_linestring),
                                   'properties':elem['properties']})

                
source_file = "C:/Users/asr13006/Desktop/Thesis/Copy of Data Reservoir/routes/\
County 13/road network micro/nxspatial3/NF/copy/SpliLinesAtVertices-copy.shp"

destination_file = "C:/Users/asr13006/Desktop/Thesis/Copy of Data Reservoir/\
routes/County 13/road network micro/nxspatial3/NF/copy/TransformCRS/\
LineString_Road_Network_UTM.shp"

linestring_shapefile_coordinate_transformer(source_file, destination_file)