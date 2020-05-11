'''Author = Yatin Kalra
Website : yatinkalra.github.io
Github : www.github.com/yatinkalra
'''

from queue import Queue
import socket, threading, sys
from datetime import datetime

t1 = datetime.now()

print("-" * 60)
print("****************PyPort - Open Ports Scanner****************")
print("-" * 60)
print("What do you wanna scan?")
print("1. Scan Reversed Ports Only")
print("2. Scan All Ports")
print("3. Scan by Custom Range")
print("4. Scan Well Known Ports")
print("5. Scan Specific Port")

try:
	scan_mode = int(input("Enter your option: "))
	if(scan_mode not in [1,2,3,4,5]):
		print("You have chose wrong option")
		sys.exit()
except ValueError:
	print("You have not chose any option")
	sys.exit()

target = input("Enter your target: ")
if(len(target) == 0):
	print("You didn't entered target")
	sys.exit()

print("-"*50)
print("TARGET: ", target)
print("STARTING TIME", t1)
print("-"*60)

def portscan(port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(0.25)
		s.connect((target, port))
		return True
	except:
		return False
	 
queue = Queue()

def get_ports(mode):
	if(mode == 1):
		for port in range(0, 1024):
			queue.put(port)
	elif(mode == 2):
		for port in range(0, 65536):
			queue.put(port)
	elif(mode == 3):
		custom_range = input("Enter your custom range :")
		star, end = custom_range.split
		for port in range(int(start), int(end)):
			queue.put(port)

	elif(mode == 4):
		ports = [20, 21, 22, 23, 25, 53, 8, 110, 169, 443, 445]
		for port in ports:
			queue.put(port)

	elif(mode == 5):
		ports = input("Enter your ports")
		ports = ports.split()
		ports = list(map(int, ports))
		for port in ports:
			queue.put(port)

open_ports = []

def worker():
	while not queue.empty():
		port = queue.get()
		if portscan(port):
			print(f"Port {port} is open")
			open_ports.append(port)


def run_scanner(thread, mode):
	get_ports(mode)
	thread_list = []

	for t in range(thread):
		thread = threading.Thread(target=worker)
		thread_list.append(thread)

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()

	open_ports.sort()
	print("Open Ports: ", open_ports)
	print("-"*60)

run_scanner(500, scan_mode)
t2 = datetime.now()
print(f"Scanning completed in {t2-t1} seconds")
print("-"*60)

