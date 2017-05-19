import math
import time
import json
from math import *
my_arr = []
new_arr = []
kmtolatlon = 111 # 111km = 1 lat or lon deg
max_length = 0.000720721 #drone max signal length 80m = 0.08km = 0.08/111 = 0.7 angle lipda
max_distance = 0.22 #maximum distance between station and destination

class coordinate(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon

def get_distance(origin, destination):
    lon1, lat1 = origin.lon,origin.lat
    lon2, lat2 = destination.lon,destination.lat
    radius = 6371 # km
    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dis = radius * c

    return dis

def GetAngleOfLineBetweenTwoPoints(point1,point2):
    lon1, lat1 = point1.lon,point1.lat
    lon2, lat2 = point2.lon,point2.lat
    lonDiff = lon2 - lon1
    latDiff = lat2 - lat1
    return degrees(atan2(latDiff, lonDiff))

def rotate(origin, point, angle):

    ox, oy = origin.lon,origin.lat
    px, py = point.lon,point.lat

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    if 'e' in str(qx):
    	qx = 0
    if 'e' in str(qy):
    	qy = 0
    return qy, qx

def CreateTriangleWaypoint(origin,distance):
    arr = []
    lon1,lat1 = origin.lon,origin.lat
    dis = distance/kmtolatlon
    newlon_3 = lon1+dis
    newlon_1 =  lon1+dis/3
    newlon_2 =  lon1+dis*2/3
    newlat_1_up = lat1+(distance/max_distance*max_length)
    newlat_1_down = lat1-(distance/max_distance*max_length)

    arr.append(coordinate(newlat_1_up,newlon_1))
    arr.append(coordinate(newlat_1_down,newlon_1))
    arr.append(coordinate(lat1,newlon_2))
    arr.append(coordinate(lat1,newlon_3))
    return arr


def sim_drone_gps(src,des1,des2,des3):
	i = 0
	lat0,lon0 = src.lat,src.lon
	lat1,lon1 = des1.lat,des1.lon
	lat2,lon2 = des2.lat,des2.lon
	lat3,lon3 = des3.lat,des3.lon
	lat_dif1 = lat1-lat0
	lon_dif1 = lon1-lon0
	lat_dif2 = lat2-lat0
	lon_dif2 = lon2-lon0
	lat_dif3 = lat3-lat0
	lon_dif3 = lon3-lon0
	new_point1 = coordinate(lat0,lon0)
	new_point2 = coordinate(lat0,lon0)
	new_point3 = coordinate(lat0,lon0)
	print '===================*'
	print new_point1.lat
	print new_point2
	print new_point3
	while get_distance(new_point3,des3) > 0.0001:
		print i
		w1 = open('gps_location1.json','w')
		w2 = open('gps_location2.json','w')
		w3 = open('gps_location3.json','w')
		print get_distance(new_point3,des3)
		if get_distance(new_point1,des1) > 0.0001:
			print '================================*'
			new_point1.lat = new_point1.lat+lat_dif1/60
			new_point1.lon = new_point1.lon+lon_dif1/60
			print new_point1.lat,new_point1.lon
			result1['lat'] = round(new_point1.lat,6)
			result1['lon'] = round(new_point1.lon,6)
			print json.dumps(result1)
			w1.write(json.dumps(result1))
			w1.close()
		if get_distance(new_point2,des2) > 0.0001:
			print '================================**'
			new_point2.lat = new_point2.lat+lat_dif2/60
			new_point2.lon = new_point2.lon+lon_dif2/60
			print new_point2.lat,new_point2.lon
			result2['lat'] = round(new_point2.lat,6)
			result2['lon'] = round(new_point2.lon,6)
			print json.dumps(result2)
			w2.write(json.dumps(result2))
			w2.close()
		print '================================***'
		new_point3.lat = new_point3.lat+lat_dif3/60
		new_point3.lon = new_point3.lon+lon_dif3/60
		print new_point3.lat,new_point3.lon
		result3['lat'] = round(new_point3.lat,6)
		result3['lon'] = round(new_point3.lon,6)
		print json.dumps(result3)
		w3.write(json.dumps(result3))
		w3.close()
		
		i += 1
		time.sleep(0.5)
	
	# while True:
	# 	if  

def calculateWP_mode1(station_point,node_point,number_of_drone_for_create_connection,number_of_all_drone):
    list_of_waypoint = []
    for i in xrange(int(number_of_drone_for_create_connection)):
        averate_lat = ( math.fabs(station_point.lat - node_point.lat)/(number_of_drone_for_create_connection+1)*(i+1) ) + min([station_point.lat, node_point.lat])
        averate_lon = ( math.fabs(station_point.lon - node_point.lon)/(number_of_drone_for_create_connection+1)*(i+1) ) + min([station_point.lon, node_point.lon])
        list_of_waypoint.append((round(averate_lat,7), round(averate_lon,7)))
    for i in xrange(int(number_of_all_drone - number_of_drone_for_create_connection)):
        #arctan = math.atan((node_point.lon - station_point.lon)/(node_point.lat - station_point.lat))
        arctan = math.atan((node_point.lat - station_point.lat)/(node_point.lon - station_point.lon))
        middle_lat = (station_point.lat + node_point.lat)/2
        middle_lon = (station_point.lon + node_point.lon)/2
        plus_lat = -0.00005 * (0.25*((-2)*(math.pow(-1,i+1))*(i+1) - (math.pow(-1,i+1)) + 1)) * math.cos(math.pi - arctan)
        plus_lon = -0.00005 * (0.25*((-2)*(math.pow(-1,i+1))*(i+1) - (math.pow(-1,i+1)) + 1)) * math.sin(math.pi - arctan)
        list_of_waypoint.append((round(middle_lat+plus_lat,6), round(middle_lon+plus_lon,6)))
    return list_of_waypoint

station_point = coordinate(13.846680 ,100.565630)
node_point = coordinate(13.847526 ,100.566111)

# node_point = coordinate(13.847526 ,100.560011)

d = {}
s = open('station.json','w')
d['lat'] = station_point.lat
d['lon'] = station_point.lon
print '==================='
print json.dumps(d)
s.write(json.dumps(d))
s.close()

e = {}
n = open('destination.json','w')
e['lat'] = node_point.lat
e['lon'] = node_point.lon
print '==================='
print json.dumps(e)
n.write(json.dumps(e))
n.close()

number_of_drone_for_create_connection = 3
drone_mode1 = calculateWP_mode1(station_point,node_point,number_of_drone_for_create_connection,3)
print drone_mode1

angle = GetAngleOfLineBetweenTwoPoints(station_point,node_point)
dis = get_distance(station_point,node_point)
arr =  CreateTriangleWaypoint(station_point,dis)
drone_mode2 = []
for x in arr:
	drone_mode2.append(rotate(station_point, x, math.radians(angle)))
print drone_mode2

result1 = {}
result2 = {}
result3 = {}

# drone_list = drone_mode1
drone_list = drone_mode2

src = station_point
des1 = coordinate(drone_list[0][0],drone_list[0][1])
des2 = coordinate(drone_list[1][0],drone_list[1][1])
des3 = coordinate(drone_list[2][0],drone_list[2][1])

sim_drone_gps(src,des1,des2,des3)

		
