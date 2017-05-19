from math import *
import math
import serial, time
import socket
import itertools
import os
import fcntl
import struct
import json

class coordinate(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon

def getMyIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

list_of_ip = ["192.168.8.11", "192.168.8.12", "192.168.8.13"]
status = "W"
designated_drone = "192.168.8.11"
max_number_of_all_drone = 3
number_of_all_drone = 3
list_of_active_drone = []
# my_ip = '192.168.8.20'
my_ip = getMyIP("wlan0") #"192.168.8.11"
other_ip = [ip for ip in list_of_ip if ip != my_ip] #["192.168.8.12", "192.168.8.13"]
station_point = coordinate(13.846324, 100.567100)
node_point = coordinate(13.846213, 100.567004)
update_times = 0
state_update = True
first_ND = True
comeback_home = False
comeback_time = time.time()
kmtolatlon = 111 # 111km = 1 lat or lon deg
max_length = 0.000720721 #drone max signal length 80m = 0.08km = 0.08/111 = 0.7 angle lipda
max_distance = 0.22 #maximum distance between station and destination
new_waypoint = []

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
    # arr.append(coordinate(lat1,newlon_3)) this is destination point
    return arr

def calculateWP_mode1():
    list_of_waypoint = []
    for i in xrange(int(number_of_drone_for_create_connection)):
        averate_lat = ( math.fabs(station_point.lat - node_point.lat)/(number_of_drone_for_create_connection+1)*(i+1) ) + min([station_point.lat, node_point.lat])
        averate_lon = ( math.fabs(station_point.lon - node_point.lon)/(number_of_drone_for_create_connection+1)*(i+1) ) + min([station_point.lon, node_point.lon])
        list_of_waypoint.append([round(averate_lat,6), round(averate_lon,6)])
    for i in xrange(int(number_of_all_drone - number_of_drone_for_create_connection)):
        #arctan = math.atan((node_point.lon - station_point.lon)/(node_point.lat - station_point.lat))
        arctan = math.atan((node_point.lat - station_point.lat)/(node_point.lon - station_point.lon))
        middle_lat = (station_point.lat + node_point.lat)/2
        middle_lon = (station_point.lon + node_point.lon)/2
        plus_lat = -0.00005 * (0.25*((-2)*(math.pow(-1,i+1))*(i+1) - (math.pow(-1,i+1)) + 1)) * math.cos(math.pi - arctan)
        plus_lon = -0.00005 * (0.25*((-2)*(math.pow(-1,i+1))*(i+1) - (math.pow(-1,i+1)) + 1)) * math.sin(math.pi - arctan)
        list_of_waypoint.append([round(middle_lat+plus_lat,6), round(middle_lon+plus_lon,6)])
    return list_of_waypoint

def calculateWP_mode2():
    list_of_waypoint = []
    before_rotate = []
    print 'origin point: LAT: ' + str(station_point.lat) + ' LON: ' + str(station_point.lon)
    print 'destination point: LAT: ' + str(node_point.lat) + ' LON: ' + str(node_point.lon)
    angle = GetAngleOfLineBetweenTwoPoints(station_point,node_point)
    dis = get_distance(station_point,node_point)
    before_rotate = CreateTriangleWaypoint(station_point,dis)
    for p in before_rotate:
        list_of_waypoint.append(rotate(station_point, p, math.radians(angle)))
    return list_of_waypoint

def createFormation(formation_list):
    i=0
    match_point = {}
    result = []
    all_active_drone = list_of_active_drone+[my_ip]
    for x in all_active_drone:
        match_point[x] = True
    for x in sorted(all_active_drone):
        if match_point[x]:
            a,b = formation_list[i]
            result.append((x,a,b))
            match_point[x] = False
            i += 1
        else:
            continue
    return result


def combinationDroneAndWaypoint(list_of_waypoint):
    my_gps = readGPS()
    list_of_gps_drone = readGPSFromOtherDrone()+[[my_ip,str(my_gps.lat),str(my_gps.lon),str(update_times)]]
    for ip,lat,lon,update in list_of_gps_drone:
        print "[MESSAGE] LIST_OF_GPS_DRONE : "+ip+" => LAT : "+lat+" LONG : "+lon
    min_of_max_distance = float("inf")

    maching_all = [zip(x,list_of_gps_drone) for x in itertools.permutations(list_of_waypoint,len(list_of_gps_drone))]
    maching_all_add_distance = []
    for match in maching_all:
        combination = []
        max_distance = -float("inf")
        this_match_distance = []
        for wp,dp in match:
            wlat,wlon = wp
            ip,dlat,dlon,update = dp
            distance = math.sqrt( math.pow((float(wlat) - float(dlat)),2) + math.pow((float(wlon) - float(dlon)),2) )
            this_match_distance.append(distance)
        maching_all_add_distance.append([match,sorted(this_match_distance, reverse=True)])

    if len(maching_all_add_distance[0][1]) == 1:
        maching_all_add_distance.sort(key=lambda x: (x[1][0]))
    elif len(maching_all_add_distance[0][1]) == 2:
        maching_all_add_distance.sort(key=lambda x: (x[1][0], x[1][1]))
    elif len(maching_all_add_distance[0][1]) == 3:
        maching_all_add_distance.sort(key=lambda x: (x[1][0], x[1][1], x[1][2]))
    
    result = []
    point,value = maching_all_add_distance[0]
    for wp, dp in point:
        wlat, wlon = wp
        ip, dlat, dlon, update = dp
        result.append([ip, wlat, wlon])

    return result

def genaratePacket(header, message):
    return header+" "+message

def checkActiveDrone():
    global list_of_active_drone
    global number_of_all_drone
    backup = list_of_active_drone
    list_of_active_drone = []
    for x in other_ip:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = s.connect_ex((x, 9999))
            if result == 0:
                print x
                list_of_active_drone.append(x)
        except socket.error as msg:
            continue

    number_of_all_drone = len(list_of_active_drone+[my_ip])

    if len(backup) == len(list_of_active_drone):
        return False # not change
    else:
        return True # change

def checkStatus():
	status = open("status.txt", "r")
	return status.read().split(" ")

def readGPSFromOtherDrone():
    Dlist = []
    for x in list_of_active_drone:
        f = open('gps_'+str(x)+'.txt', 'r')
        Dlist.append(f.read().split(","))
    return Dlist

def readGPS():
    command = open("command.txt", "w")
    command.write("status")
    command.close()

    time.sleep(1)

    with open('gps_location.json') as gps:
        gps_location = json.load(gps)
        lat = gps_location['lat']
        lon = gps_location['lon']

    return coordinate(lat,lon)

def readGPSStation():
    try:
        st = open("station.txt", "r")
        lat,lon = st.read().split(",")    
        return coordinate(float(lat), float(lon))
    except:
        return coordinate(13.846324, 100.567100)

def readGPSDestination():
    try:
        nd = open("destination.txt", "r")
        lat, lon = nd.read().split(",")
        return coordinate(float(lat), float(lon))
    except:
        return coordinate(13.846213, 100.567004)

def sendPacket(ip,message):
    count = 0
    while 1:
        if count == 2: return False
        port = 9999
        buffer_size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
        except socket.error as msg:
            print "[MESSAGE] "+ip+" Request timeout."
            count += 1
            time.sleep(2)
            continue
        try:
            s.send(message)
            print "[MESSAGE] Success send to: " + ip
            s.close()
            break
        except socket.error as msg:
            time.sleep(2)
            continue

    return True

def createWaypointFile(lat,lon):
    index = 0 

    f = open('wp.txt', 'w')
    f.write("")
    f.close()

    f = open('wp.txt', 'a')
    f.write("QGC WPL 110\n")

    home_lat, home_lon = lat,lon

    try:
        home = open("home_"+my_ip+".txt", "r")
        home_lat, home_lon = home.read().split(",")
        home.close
    except:
        home_lat, home_lon = lat, lon

    f.write(str(index)+"\t1\t0\t16\t0\t0\t0\t0\t"+home_lat+"\t"+home_lon+"\t10.000000\t1\n")
    index+=1
    f.write(str(index)+"\t0\t0\t16\t0\t0\t0\t0\t"+lat+"\t"+lon+"\t10.000000\t1\n")
    index+=1
    f.write(str(index)+"\t0\t0\t17\t0\t0\t0\t0\t"+lat+"\t"+lon+"\t10.000000\t1\n")
    f.close()

def createComebackHomeFile():
    try:
        print "home_"+my_ip+".txt"
        home = open("home_"+my_ip+".txt", "r")
        home_lat, home_lon = home.read().split(",")
        home.close
    except:
        print "NOT SET HOME POINT"
        return 0

    index = 0

    f = open('wp.txt', 'w')
    f.write("")
    f.close()

    f = open('wp.txt', 'a')
    f.write("QGC WPL 110\n")

    f.write(str(index)+"\t1\t0\t16\t0\t0\t0\t0\t"+home_lat+"\t"+home_lon+"\t10.000000\t1\n")
    index+=1
    f.write(str(index)+"\t0\t0\t16\t0\t0\t0\t0\t"+home_lat+"\t"+home_lon+"\t10.000000\t1\n")
    index+=1
    f.write(str(index)+"\t0\t0\t17\t0\t0\t0\t0\t"+home_lat+"\t"+home_lon+"\t10.000000\t1\n")
    f.close()

def sendCommandToMavproxy(command):
    f = open("command.txt", "w")
    f.write("\n".join(command))
    f.close()    

def writeStatus(s):
    f = open("status.txt", "w")
    f.write(s)
    f.close

def waitFirstACK():
    count = 0
    if list_of_active_drone == []:
        return True
    while True:
        for x in list_of_active_drone:
            try:
                f = open('gps_'+str(x)+'.txt', 'r')
            except:
                count = 0
                break
            data = f.read().split(",")
            if int(data[3]) < 2:
                return True
        count += 1
        if count == 3:
            return False
            break
        time.sleep(1)

def checkMode():
    mode = open('mode.txt','r')
    return mode.read()


writeStatus('W')
while 1:

    time.sleep(2)

    e = readGPS()

    status = checkStatus()

    if status[0] == "D":
        designated_drone = status[1]
        checkActive = checkActiveDrone()
        if checkActive == True:
            first_ND = True
            update_times = 0
            state_update = True
            comeback_home = False
            if designated_drone not in list_of_active_drone + [my_ip]:
                if min(list_of_active_drone + [my_ip]) == my_ip:
                    writeStatus("D "+my_ip)
                else:
                    writeStatus("W")
            else:
                writeStatus("D "+designated_drone)

    status = checkStatus()

    if status[0] == "D" and status[1] == my_ip:

        print '[MESSAGE] STATUS : D'
        designated_drone = my_ip
        message = genaratePacket("public", my_ip)
        public_message_station = readGPSStation()
        public_message_node = readGPSDestination()
        message_station = genaratePacket("station", str(public_message_station.lat)+","+str(public_message_station.lon))
        message_node = genaratePacket("node", str(public_message_node.lat)+","+str(public_message_node.lon))
        for x in list_of_active_drone:
            sendPacket(x, message+" "+message_station+" "+message_node)

        if first_ND == True:
            if waitFirstACK() == True:
                first_ND = False
            else:
                continue

        if comeback_home == True:
            if time.time() - comeback_time > 3:
                for ip in list_of_active_drone+[my_ip]:
                    if ip == my_ip:
                        createComebackHomeFile()
                        sendCommandToMavproxy(["mode auto", "wp load wp.txt", "wp set 1"])
                        print "[MESSAGE] MOVE LOOPBACK ! (HOME)"
                    else:
                        message = genaratePacket("move", "home")
                        if sendPacket(ip, message) == False:
                            break
                writeStatus("W")
                comeback_home = False

        new_station_point = readGPSStation()
        d = get_distance(new_station_point, station_point)*1000
        if d < 1 and state_update :
            print "[MESSAGE] First Same Station Point"
            station_point = new_station_point
            state_update = False
        elif d < 1 :
            print "[MESSAGE] Same Station Point"
            continue
        else:
            print "[MESSAGE] Moving Station Point"
            station_point = new_station_point
            state_update = True
            continue

        formation_mode = checkMode()
        node_point = readGPSDestination()

        if (formation_mode == '1'):
            station_node_distance = get_distance(station_point, node_point)*1000
            if station_node_distance < 40:
                number_of_drone_for_create_connection = 1
            else:
                number_of_drone_for_create_connection = math.ceil((station_node_distance-40+1)/40)
            if number_of_drone_for_create_connection > number_of_all_drone:
                if comeback_home == False:
                    comeback_home = True
                    comeback_time = time.time()
                print "[MESSAGE] Impossible to Form Network"
                continue
            else:
                comeback_home = False
            list_of_waypoint = calculateWP_mode1()
            result_combination = combinationDroneAndWaypoint(list_of_waypoint)
            
        elif (formation_mode == '2'):
            d = get_distance(station_point,node_point)
            print 'Distance : ' + str(d)
            if d > max_distance:
                if comeback_home == False:
                    comeback_home = True
                    comeback_time = time.time()
                print '[ERRMSG] Impossible to Form Network : distance is too far'  
            else:                  
                list_of_waypoint = calculateWP_mode2()
                result_combination = createFormation(list_of_waypoint)
                # print result_combination

        for ip,lat,lon in result_combination:
            print "[MESSAGE] RESULT : "+ip+" => LAT : "+str(lat)+" LONG : "+str(lon)
            for ip,lat,lon in result_combination:
                if ip == my_ip:
                    createWaypointFile(str(lat),str(lon))
                    sendCommandToMavproxy(["mode auto", "wp load wp.txt", "wp set 1"])
                    print "[MESSAGE] MOVE LOOPBACK ! "+str(lat)+","+str(lon)
                else:
                    message = genaratePacket("move", str(lat)+","+str(lon))
                    if sendPacket(ip, message) == False:
                        break

    elif status[0] == "D" and status[1] != my_ip:
        print '[MESSAGE] STATUS : ND'
        designated_drone = status[1]
        currentGPS = readGPS()
        message = genaratePacket("forward", str(my_ip)+","+str(currentGPS.lat)+","+str(currentGPS.lon)+","+str(update_times))
        update_times += 1
        if sendPacket(designated_drone, message) == False:
            continue

    elif status[0] == 'W':
        print '[MESSAGE] STATUS : W'


