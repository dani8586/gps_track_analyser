import re
from bs4 import BeautifulSoup

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
    
    with open('activity_9401851735.gpx', 'r') as file:
        xml_content = file.read()
    soup = BeautifulSoup(xml_content, 'xml')    
    trkpt_elements = soup.find_all('trkpt')
    
    new_point = False
    data_lat=None;   data_lon=None;   data_el=None;   data_time=None  
    
    for trkpt in trkpt_elements:
        lat = trkpt['lat']
        lon = trkpt['lon']
        ele = trkpt.ele.text
        time = trkpt.time.text.split('T')[1].split('.')[0]
        
        point = points(float(lat),float(lon),float(ele),time)
        my_list.append(point)
    

    return my_list        

        

        
