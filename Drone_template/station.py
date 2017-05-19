import socket
import time

list_of_active_drone = []
number_of_all_drone = 3
list_of_all_drone = ["192.168.8.11", "192.168.8.12", "192.168.8.13"]
ins_list = {}


def checkActiveDrone():
    global list_of_active_drone
    global number_of_all_drone
    backup = list_of_active_drone
    list_of_active_drone = []
    for x in list_of_all_drone:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = s.connect_ex((x, 9999))
            if result == 0:
                list_of_active_drone.append(x)
        except socket.error as msg:
            continue

    number_of_all_drone = len(list_of_active_drone)

    if len(backup) == len(list_of_active_drone):
        return False # not change
    else:
        return True # change

def sendCommand(ip, message):
    port = 9999
    buffer_size = 20
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip,port))
    except socket.error as msg:
        print "Request timeout."
        time.sleep(2)
    try:
        s.send("root "+message)
        print "OK"
        s.close()
    except socket.error as msg:
        time.sleep(2)


def main():
    print "\n\t ======================================"
    print "\t|                                      |"
    print "\t|            STATION CONTROL+          |"
    print "\t|                                      |"
    print "\t ======================================"
    print "\t type \"--h\" to show command option\n"

    while 1:
        print "INPUT >> ",
        inp = raw_input()
        if inp == "": 
            continue
        if inp.split()[0] == "exit":
            exit()
        if inp.split()[0] == "--h":
            print "\t ---------- Manual ----------\n"
            print "\t set d [ip]"
            print "\t\t -set initial designated drone"
            print "\t set home [ip] [latitude] [longitude]"
            print "\t\t -set home location of drone"
            print "\t set station [latitude] [longitude]"
            print "\t\t -set station location"
            print "\t set destination [latitude] [longitude]"
            print "\t\t -set destination location"
            print "\t set mode [number]"
            print "\t\t -choose formulation mode"
            print "\t\t\t - 1 : straight line mode"
            print "\t\t\t - 2 : redundant mode"
            print "\t formulate init"
            print "\t\t -start formulation process"
            print "\t --h"
            print "\t\t -show command option"
            continue

        checkActiveDrone()


        if inp.split()[0] == "check":
            print 'active drone is : ' + str(list_of_active_drone)
        else:
            try :
                if inp.split()[1] == 'd' or inp.split()[1] == 'home':
                    if (inp.split()[2] not in list_of_active_drone):
                        print inp.split()[2]+' offline'
                    else:
                        if inp.split()[1] == 'd':
                            ins_list['d'] = inp.lower()
                            ins_list['addr'] = inp.split()[2]
                        elif inp.split()[1] == 'home':
                            ins_list['home'] = inp.lower()
                elif inp.split()[1] == 'mode':
                    ins_list['m'] = inp.lower()
                elif inp.split()[1] == 'station' or inp.split()[1] == 'destination':
                    ins_list[inp.split()[1]] = inp.lower()
                elif inp == 'formulate init':
                    for ins in ins_list:    
                        sendCommand(ins_list['addr'],ins_list[ins])
                        time.sleep(1)
                    for ip in list_of_active_drone:
                        sendCommand(ip, ins_list['station'])
                        time.sleep(1) 
                        sendCommand(ip, inp.list['destination'])
                        time.sleep(1)    
            except: 
                print 'wrong command please use --h for more information'
                continue
            

if __name__ == "__main__":
    main()
