#!/usr/bin/env python
#
# nagios_text_summary.py - This program produces a plain-text summary
# similar to that found on the Service Detail page of nagios.
#
# I use this script to generate daily email reports from a cron job.

# http://your.nagios.server/cgi-bin/nagios3/nagios_summary.py
#
import os, time, re, xlwt, time
from xlutils.copy import copy
from xlrd import open_workbook 
from  threading import Timer
from datetime import datetime 
# Map the host and service enumerations to readable text
HOST_STATE_MAP = {"0": "UP", "1": "DOWN"}
STATE_MAP = {"0": "OK", "1": "WARNING", "2": "CRITICAL", "3": "UNKNOWN"}

def parse_objects_file(filepath):
   """Parse a nagios objects.dat file.  Returns
   a list of dictionaries, one dictionary per object."""
   OBJECTS=open(filepath)
   objects = []
   while 1:
       line = OBJECTS.readline()
       if not line:
           break

       line = line.strip()
       if line.startswith("#"):
           # A Comment
           pass

       elif line.startswith("define") and line.find('{') != -1:
           type = line[0:line.find('{')].strip().split(" ")[1]
           object = {}

           # Now read all the details
           while 1:
               line = OBJECTS.readline()
               line = line.strip()
               if not line:
                   break
               elif line.find("\t") != -1:
                   name, value = line.split("\t", 1)
                   name = name.strip()
                   value = value.strip()
                   object[name] = value
               elif line.find("}") != -1:
                   objects.append((type, object))
                   break
   return objects
n = 0
m = 0
j = 1
k = 0
l = 0
def parse_status_file(filepath):
   """Parse a nagio status.dat file.  Returns a
   dictionary where the primary keys are the hostnames.  For each
   host all of the services are listed in the 'services' key; the other
   key elements are used for host details."""
   STATUS=open(filepath)
   summary = {}
   while 1:
       line = STATUS.readline()
       if not line:
           break
       line = line.strip()
       if line.startswith("#"):
           # A Comment
           pass

       elif line.find('{') != -1:
           statustype = line[0:line.find('{')]
           if statustype.strip() == "hoststatus":
               # We except host_name and service_description first
               line = STATUS.readline()
               name, hostname = line.split("=", 1)
               name = name.strip()
               hostname = hostname.strip()
               if name != "host_name":
                   continue
               if not summary.has_key(hostname):
                   summary[hostname] = {}
                   summary[hostname]['services'] = {}
               # Now read all the details
               while 1:
                   line = STATUS.readline()
                   if not line:
                       break
                   elif line.find("=") != -1:
                       name, value = line.split("=", 1)
                       name = name.strip()
                       value = value.strip()
                       summary[hostname][name] = value
                   elif line.find("}") != -1:
                       break

           elif statustype.strip() == "servicestatus":
               # We except host_name and service_description first
               line = STATUS.readline()
               name, hostname = line.split("=", 1)
               name = name.strip()
               hostname = hostname.strip()
#	       if hostname not in list1:
#	       		list1.append(hostname)
               line = STATUS.readline()
               name, service_desc = line.split("=", 1)
               name = name.strip()
               service_desc = service_desc.strip()
               if name != "service_description":
                   continue
               summary[hostname]['services'][service_desc] = {}
               # Now read all the details
               while 1:
                   line = STATUS.readline()
                   if not line:
                       break
                   elif line.find("=") != -1:
                       name, value = line.split("=", 1)
                       name = name.strip()
                       value = value.strip()
                       summary[hostname]['services'][service_desc][name] = value
                   elif line.find("}") != -1:
                       break
   return summary
#book = xlwt.Workbook(encoding="utf-8")
#sh = book.add_sheet(sheet)

test = "/home/priyanshu/Desktop/test.xls"
def pretty_print_status():
   """Produce a pretty printed textual representation of the nagios service
   detail summary."""
   # This program assumes it is installed in the nagios cgi-bin directory
   objects = parse_objects_file("/var/cache/nagios3/objects.cache")
   summary = parse_status_file("/var/cache/nagios3/status.dat")

   # Pretty print the status
   hosts = summary.keys()
   hosts.sort()
   list1 = []
   list2 = [] 
   list3 = []
   list4 = []
   dict1 = {}
   state = []
   for host in hosts:
       if host not in list1:
     		list1.append(host)     
       status = summary[host]
       host_state = HOST_STATE_MAP[status['current_state']]
       last_checked = time.asctime(time.gmtime(int(status['last_check'])))
       ack = ""
       if host_state != "UP" and status['problem_has_been_acknowledged'] == "1":
           ack = "YES"
       elif host_state != "UP" and status['problem_has_been_acknowledged'] == "0":
           ack = "NO"
       # Use pretty print host aliases
       hostalias = host
       for objtype, object in objects:
           if objtype == "host" and object['host_name'] == host:
               try:
                   hostalias = object['alias']
               except KeyError:
                   hostalias = host
       state.append(host_state)
       
       services = summary[host]['services'].keys()
       services.sort()
       list4.append(len(services))
       for service in services:
           status = summary[host]['services'][service]
           current_state = STATE_MAP[status['current_state']]
#	   plugin_output = status['plugin_output'] 	   
	   performance_data = status['performance_data'] 	   
       	   list2.append(service)
#           m = re.search("\d", plugin_output)
	   try:
			if service == "CPU Load":
				m = re.findall("[-+]?\d*\.\d+|\d+", performance_data)
				list3.append(m[1])
				dict1[host] = m[1]
			elif service == "Check CPU":
				plugin_output = status["plugin_output"]
				m = plugin_output.split(":")[1].strip(" idle").strip("%")
				list3.append(m)
			elif service == "Check Memory":
				plugin_output = status["plugin_output"]
				m = plugin_output.split(":")[2].split(",")[0].strip("%")
				list3.append(m)
			elif service == "Root Partition":
				plugin_output = status["plugin_output"]
				m = plugin_output.split("(")[0].split("/")[1].strip(" MB")
				print m
				list3.append(m)
			elif service == "Current Load":
				m = re.findall("[-+]?\d*\.\d+|\d+", performance_data)
				list3.append(m[1])
			elif service == "HW Info":
				list3.append(1)
				plugin_output = status["plugin_output"]
				try:
					list2.append("No of CPU installed")
					m = plugin_output.split(":")[2].split("[")[1]
					list3.append(m)
				except:
					list3.append(0)
				try:
					list2.append("Processor Type")
					m = plugin_output.split(":")[3]
					list3.append(m)
				except:
					list3.append(0)
				try:
					list2.append("CPU clock speed")
					m = plugin_output.split(":")[4].strip(" MHz")
					list3.append(m)
				except:
					list3.append(0)
				try:
					list2.append("Total Memory Installed")
					m = plugin_output.split(":")[6].split("[")[1].strip(" M")
					list3.append(m)
				except:
					list3.append(0)
				try:
       		                        list2.append("Size of the disc")
					m = plugin_output.split(":")[8].split("[")[1].strip(" G")
					list3.append(m)
				except:
					list3.append(0)
				try:
					list2.append("OS installed")
					m = plugin_output.split(":")[9].split("[")[1]
					list3.append(m)
				except:
					list3.append(0)
				try:
					list2.append("Kernel Version")
					m = plugin_output.split(":")[10]
					list3.append(m)
				except:
					list3.append(0)
			else:
				m = re.search("\d+", performance_data)
				list3.append(m.group(0))
	   except:
			print "Problem"
			list3.append(0)
	   last_checked = time.asctime(time.gmtime(int(status['last_check'])))
           ack = ""
           if host_state == 'DOWN':
               # Don't report service status because it would be inaccurate
               current_state = ""
               ack = ""
           else:
               # Only print the ack state if the servie/host actually has a problem
               if current_state != "OK" and status['problem_has_been_acknowledged'] == "1":
                   ack = "YES"
               elif current_state != "OK" and status['problem_has_been_acknowledged'] == "0":
                   ack = "NO"
   list2.append("Last Checked")
   list3.append(str(datetime.time(datetime.now())))
   output(test, 0 , list1, list2, list3, list4)
   return list1,list2,list3,list4,dict1

def output(filename, sheet, list1, list2, list3, list4):
    book = open_workbook(filename, formatting_info = True)
    wb = copy(book)
    sh = wb.get_sheet(0)
    global n,m,j,k,l
    sh.write(0, 0, 'Serial No.')
    m+=1
    n+=1
#   j+=1
    k+=1
    l+=1

    sh.write(j,0,l)
    j+=1
    for e1, (e2, e3) in enumerate(zip(list2,list3)):
	 sh.write(0,e1+1,e2)
	 sh.write(k,e1+1,e3)
    wb.save(filename) 

if __name__ == "__main__":
    # Print the HTTP header info
    print "Content-Type: text/plain"
    print

    # Now print the actual data
    try:
	for timer in range(1,10,10):
	    t = Timer(timer, pretty_print_status)
       	    t.start()
	    "Yesssss"
    except Exception, e:
       print "Internal Error -", e
