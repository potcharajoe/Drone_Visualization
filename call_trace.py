from subprocess import call
import time
def use_trace_route():
	call('python trace.py', shell=True)

while True:
	use_trace_route()
	time.sleep(3)
