from gps_parse import gps_parse
from haversine import haversine
import os
import matplotlib.pyplot as plt
import math

# import data
gps_data = gps_parse("activity_9401851735.gpx")

# define an interval in meters over which to compute average quantities, like slope, to avoid fluctuations due to gps accuracy
interval = 100 # in meters

# variables for total data
tot_dist = 0.0
tot_ele = 0.0
tot_time = 0

# variables for maximum and minimums
max_v = -float('inf')
max_ele = -float('inf')
min_ele = float('inf')

max_avg_v = -float('inf')
max_avg_slope = -float('inf')
min_avg_slope = float('inf')

# list for plotting
list_dist = []
list_ele = []
list_v = []
list_time = []

list_avg_v = []
list_avg_slope = []

# loop over the gps points
for i in range(len(gps_data)):
    crd = gps_data[i]
    if i == 0:
        # define variables to save data of previous point and compute differences. assign also initial values
        old_lon = crd.lon
        old_lat = crd.lat

        old_ele = crd.ele; 
        ini_ele = old_ele
        
        aux_dist = 0.0
        aux_time = 0
        aux_ele = ini_ele
        
        old_time = crd.time.split(":")
        old_hr = int(old_time[0])
        old_mn = int(old_time[1])
        old_sec = int(old_time[2])
        # convert time in seconds after the midnight. assumes that the activity doesn't happen at 00:00:00
        old_abs_time = old_sec + 60*old_mn + 60*60*old_hr
        ini_abs_time = old_abs_time
        
    else:
        dx = 1E3*haversine(crd.lon, crd.lat  , old_lon, old_lat) # space interval between gps points in meters
        tot_dist = tot_dist + dx # total distance in meters
        
        time = crd.time.split(":")
        hr = int(time[0])
        mn = int(time[1])
        sec = int(time[2])   
        abs_time = sec + 60*mn + 60*60*hr  
        
        dt = abs_time - old_abs_time # time interval between gps points in seconds
        tot_time = tot_time + dt # total time in seconds
        
        dh = crd.ele - old_ele # altitude gain/loss between gps points in meters
        if dh>0:
            tot_ele = tot_ele + dh # total ascent in meters
            
        if crd.ele > max_ele:
            max_ele = crd.ele # maximum quote in meters
        if crd.ele < min_ele:
            min_ele = crd.ele # minimum quote in meters    
        
        v = 3.6*dx/dt # average speed between gps points in km/h
        if v>max_v:
            max_v = v # maximum speed in km/h 
            
        # save current coordinates for next iteration     
        old_lat = crd.lat
        old_lon = crd.lon 
        old_abs_time = abs_time
        old_ele = crd.ele
        
        # appending data for plot
        list_dist.append(1E-3*tot_dist)
        list_ele.append(crd.ele)
        list_v.append(v)
        list_time.append(tot_time)
        
        #compute the average over a given interval
        if tot_dist - aux_dist > interval:
            avg_v = 3.6*(tot_dist - aux_dist)/(tot_time - aux_time) # average speed in km/h
            avg_slope = 100*(crd.ele-aux_ele)/(tot_dist - aux_dist) # average slope in %
            # save maximum and minimum values
            if avg_v > max_avg_v:
                max_avg_v = avg_v
            if avg_slope > max_avg_slope:
                max_avg_slope = avg_slope   
            if avg_slope < min_avg_slope:
                min_avg_slope = avg_slope   
                
            # appending data for plot
            list_avg_slope.append(avg_slope)
            list_avg_v.append(avg_v)                                 
            
            # save current coordinates for next iteration    
            aux_dist = tot_dist
            aux_time = tot_time
            aux_ele = crd.ele

        
# conver seconds into hh:mm:ss        
mn, sec = divmod(tot_time,60)
hr, mn = divmod(mn, 60)

# print the results
print
print("#############################")
print("#- Summary of the activity -#")
print("#############################")
print()
print("Total distance = {0} km".format(round(1E-3*tot_dist,3)))
print("Total time = {0}h:{1}m:{2}s - includes stops".format(hr,mn,sec))
print("Maximum speed = {0} km/h".format(round(max_v,2)))
print("Minimum altitude = {0}m".format(round(min(min_ele,ini_ele),2)))
print("Maximum altitude = {0}m".format(round(max_ele,2)))
print("Total ascent = {0}m".format(round(tot_ele,2)))
print()
print("Average quantities over {0} m".format(interval))
print()
print("Maximum speed = {0} km/h".format(round(max_avg_v,2)))
print("Maximum slope = {0} %".format(round(max_avg_slope,2)))
print("Minimum slope = {0} %".format(round(min_avg_slope,2)))


# # This is useful for the average pase in a run
# sec, mn = math.modf(1/((3.6*tot_dist/tot_time)/60))
# sec = int(round(sec*60,0))
# print("Average pase = {0}:{1} min/km".format(int(mn),sec))

        
# here we can plot        
plt.figure()       
plt.plot(list_dist, list_ele); plt.xlabel('Distance [km]'); plt.ylabel('Altitude [m]'); plt.title(''); plt.savefig('distance_elevation.pdf')

plt.figure()
plt.plot(list_dist, list_v); plt.xlabel('Distance [km]'); plt.ylabel('Speed [km/m]'); plt.title(''); plt.savefig('distance_speed.pdf')

plt.figure()
plt.plot(list_time, list_v); plt.xlabel('Time [s]'); plt.ylabel('Speed [km/m]'); plt.title(''); plt.savefig('time_speed.pdf')

plt.figure()
list_avg_slope.sort(); list_avg_v.sort(reverse=True);
plt.plot(list_avg_slope, list_avg_v); plt.xlabel('Slope [%]'); plt.ylabel('Speed [km/m]'); plt.title(''); plt.savefig('slope_velocity.pdf')



