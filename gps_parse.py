import re
def gps_parse(filename):
    data = open(filename, 'r').readlines()
         
# define the class, where to save the data
    class points:
         def __init__(self, lat,lon,ele,time):
             self.lat = lat
             self.lon = lon
             self.ele = ele
             self.time = time            
    
    # this will be the object returned by the function
    my_list=[]
    
    # define the starting and ending tag for each gps point
    pnt_strt_TAG = "<trkpt"; pnt_end_TAG = "</trkpt>"
    # define the ending segment tag. tipically this is the end of the gps track
    seg_end_TAG = "</trkseg>"


    new_point = False
    # define the regexp to extract the data. this depends on how the data are formatted, so need to hardcode them like this
    lat_TAG = "<trkpt lat=\"(.*?)\" ";   lon_TAG = " lon=\"(.*?)\">";   ele_TAG = "<ele>(.*?)</ele>";   time_TAG = "<time>.*T(.*?).000Z</time>"
    data_lat=None;   data_lon=None;   data_el=None;   data_time=None  

    n_points = 0 # counter for the number of gps points
    for i in range(len(data)):
        # initialize class to dummy variables
        if new_point == False:
            point = points(None, None, None, None)

        if pnt_strt_TAG in data[i]:
            n_points = n_points+1
            new_point = True
        
        if pnt_end_TAG in data[i]:
            new_point = False
        
        auxdata_lat = re.findall(lat_TAG, data[i]);  
        auxdata_lon = re.findall(lon_TAG, data[i])  
        auxdata_ele = re.findall(ele_TAG, data[i])
        auxdata_time = re.findall(time_TAG, data[i])    
        if len(auxdata_lat)>0: data_lat=auxdata_lat
        if len(auxdata_lon)>0: data_lon=auxdata_lon
        if len(auxdata_ele)>0: data_ele=auxdata_ele
        if len(auxdata_time)>0: data_time=auxdata_time

        if seg_end_TAG in data[i]:
            break            
        
        if n_points>0 and new_point == False:
            point = points(float(data_lat[0]),float(data_lon[0]),float(data_ele[0]),data_time[0])
            my_list.append(point)
    return my_list