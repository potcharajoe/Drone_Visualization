import json
with open('gps_location1.json') as data_file:
	data = json.load(data_file)
	print str(data['lat']) + '======' + str(data['lon'])
	print data['lat'] + data['lon']