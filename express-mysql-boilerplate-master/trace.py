import subprocess
import json

def use_trace_route(ip_addr):
	s = 'traceroute '  + ip_addr
	cmd = subprocess.Popen(s, shell=True , stdout=subprocess.PIPE)
	r = open('trace_res.json' , 'w')
	# f.write('{')
	for line in cmd.stdout:
		ip[line.split()[1][-1:]] = True
	r.write(json.dumps(ip))

ip = {}
ip["1"] = False
ip["2"] = False
ip["3"] = False
# print json.dumps(ip)
use_trace_route('192.168.8.13')