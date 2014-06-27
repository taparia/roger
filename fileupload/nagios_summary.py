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
   print "%-20s%-25s%-10s%-20s%-20s" % ("Host", "Service", "Status", "Acknowledged", "Plugin Output")
   hosts = summary.keys()
   hosts.sort()
   list1 = []
   list2 = [] 
   list3 = []
   list4 = []
   state = []
   for host in hosts:
       print "-------------------------------------------------------------------------------------------"
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
#       print "%-14s%-25s%-10s%-20s%-20s" % (hostalias, "", host_state, ack, last_checked)
       state.append(host_state)
       print "%-20s%-25s%-10s%-20s" % (hostalias, "", host_state, ack)
       
       services = summary[host]['services'].keys()
       services.sort()
       list4.append(len(services))
       for service in services:
           status = summary[host]['services'][service]
           current_state = STATE_MAP[status['current_state']]
#	   plugin_output = status['plugin_output'] 	   
	   performance_data = status['performance_data'] 	   
           if host == "localhost":
       	       list2.append(service)
#           m = re.search("\d", plugin_output)
	   if host == "localhost":
		   try:
			if service == "Current Load":
				m = re.findall("[-+]?\d*\.\d+|\d+", performance_data)
				list3.append(m[1])
			elif service == "HW Info":
				list3.append(0)
				plugin_output = status["plugin_output"]
				list2.append("No of CPU's installed")
				m = plugin_output.split(":")[2].split("[")[1]
				list3.append(m)
				list2.append("Processor Type")
				m = plugin_output.split(":")[3]
				list3.append(m)
				list2.append("CPU clock speed")
				m = plugin_output.split(":")[4].strip(" MHz")
				list3.append(m)
				list2.append("Total Memory Installed")
				m = plugin_output.split(":")[6].split("[")[1].strip(" M")
				print m
				list3.append(m)
                                list2.append("Size of the disc")
				m = plugin_output.split(":")[8].split("=")[1].strip(" G")
				list3.append(m)
				list2.append("OS installed")
				m = plugin_output.split(":")[9].split("[")[1]
				list3.append(m)
				list2.append("Kernel Version")
				m = plugin_output.split(":")[10]
				list3.append(m)
			else:
				m = re.search("\d+", performance_data)
				list3.append(m.group(0))
		   except:
			print "Problem"
			list3.append(0)
	#	   list3.append(m)
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
#           print "%-14s%-25s%-25s%-10s%-20s%-20s" % ("", service, current_state, plugin_output, ack, last_checked)
#           print "%-20s%-25s%-25s%-10s%-20s" % ("", service, current_state, plugin_output, ack)
           print "%-20s%-25s%-25s%-10s%-20s" % ("", service, current_state, performance_data, ack)

   list2.append("Last Checked")
   list3.append(str(datetime.time(datetime.now())))
   output(test, 0 , list1, list2, list3, list4)
   return list1, state

#  return list1,list2,list3,list4
  
def output(filename, sheet, list1, list2, list3, list4):
#    book = xlwt.Workbook(encoding="utf-8")
#    sh = book.add_sheet(sheet)
    book = open_workbook(filename, formatting_info = True)
#    r_sheet = rb.sheet_by_index(0)
    wb = copy(book)
    sh = wb.get_sheet(0)
#    col1_name = 'Host'
#    col2_name = 'Service'
#    col3_name = 'Output'
    global n,m,j,k,l
#    sh.write(n, 0, col1_name)
#    sh.write(n, 1, col2_name)
#    sh.write(n, 2, col3_name)
    sh.write(0, 0, 'Serial No.')
    m+=1
    n+=1
#   j+=1
    k+=1
    l+=1

#    i = 0
#    for e1 in list1:
#      sh.write(m, 0, e1)
#      m+=1
#      m+= list4[i]
#      i+=1
#    for e2, e3 in zip(list2, list3):
#           sh.write(n, 1, e2)
#	   sh.write(n, 2, e3)
#	   n+=1
    sh.write(j,0,l)
    j+=1
    for e1, (e2, e3) in enumerate(zip(list2,list3)):
	 sh.write(0,e1+1,e2)
	 sh.write(k,e1+1,e3)
#            for e3 in list3:
#	         sh.write(n, 2, e3)
#		 n+=1
#    for e2 in list2:
#        sh.write(n, 1, e2)
#	n+=1
#
#    for e3 in list3:
#        sh.write(n, 2, e3)
#	n+=1
#
#    print filename+'.out'+os.path.splitext(filename)[-1]
    wb.save(filename) 
#    print "All"
#    wb.save(filename + '.out' + os.path.splitext(filename)[-1])
#    print "Haan"

#if __name__ == "__main__":
#    # Print the HTTP header info
#    print "Content-Type: text/plain"
#    print
#
#    # Now print the actual data
#    try:
#	for timer in range(1,10,5):
#	    t = Timer(timer, pretty_print_status)
#       	    t.start()
##        pretty_print_status()
##	    list1 = pretty_print_status()[0]
##	    list2 = pretty_print_status()[1]
##	    list3 = pretty_print_status()[2]
##	    list4 = pretty_print_status()[3]
##            output(test, "Sheet 1", pretty_print_status()[0], pretty_print_status()[1], pretty_print_status()[2], pretty_print_status()[3])
#    except Exception, e:
#       print "Internal Error -", e
