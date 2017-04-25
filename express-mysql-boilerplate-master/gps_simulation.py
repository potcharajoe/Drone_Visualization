import math
import time
import json

def get_distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km
    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dis = radius * c

    return dis


def sim_drone_gps(src,des1,des2,des3):
	i = 0
	lat0,lon0 = src
	lat1,lon1 = des1
	lat2,lon2 = des2
	lat3,lon3 = des3
	lat_dif1 = lat1-lat0
	lon_dif1 = lon1-lon0
	lat_dif2 = lat2-lat0
	lon_dif2 = lon2-lon0
	lat_dif3 = lat3-lat0
	lon_dif3 = lon3-lon0
	new_point1 = lat0,lon0
	new_point2 = lat0,lon0
	new_point3 = lat0,lon0
	while get_distance(new_point3,des3) > 0.0001:
		print i
		w1 = open('gps_location1.json','w')
		w2 = open('gps_location2.json','w')
		w3 = open('gps_location3.json','w')
		print get_distance(new_point3,des3)
		if get_distance(new_point1,des1) > 0.0001:
			print '================================'
			new_point1 = new_point1[0]+lat_dif1/200,new_point1[1]+lon_dif1/200
			print new_point1
			result1['lat'] = round(new_point1[0],6)
			result1['lon'] = round(new_point1[1],6)
			print json.dumps(result1)
			w1.write(json.dumps(result1))
			w1.close()
		if get_distance(new_point2,des2) > 0.0001:
			print '================================'
			new_point2 = new_point2[0]+lat_dif2/200,new_point2[1]+lon_dif2/200
			print new_point2
			result2['lat'] = round(new_point2[0],6)
			result2['lon'] = round(new_point2[1],6)
			print json.dumps(result2)
			w2.write(json.dumps(result2))
			w2.close()
		print '================================'
		new_point3 = new_point3[0]+lat_dif3/200,new_point3[1]+lon_dif3/200
		print new_point3
		result3['lat'] = round(new_point3[0],6)
		result3['lon'] = round(new_point3[1],6)
		print json.dumps(result3)
		w3.write(json.dumps(result3))
		w3.close()
		
		i += 1
		time.sleep(1)
	
	# while True:
	# 	if  

result1 = {}
result2 = {}
result3 = {}
src = 13.84668,100.56563
des1 = 13.847134497914118, 100.56548347421271
des2 = 13.846786525691316, 100.56609550020126
des3 = 13.847241023605422, 100.56594897441396

sim_drone_gps(src,des1,des2,des3)

		
