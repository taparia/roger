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
       state.append(host_state)
   return list1, state

