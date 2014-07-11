def tsentiment():
	try:
		from subprocess import Popen
#		command1 = 'nohup sh /home/priyanshu/Desktop/scripts/ec2_login.sh'
#		a = subprocess.Popen(command1, shell=True, stderr=subprocess.PIPE)
#		a.wait()
		k = 0
		i = 1 
		while i < 7:
#			soft1 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.86.79.168 sh scripts/java.sh'
#			b = subprocess.Popen(soft1, shell=True, stderr=subprocess.PIPE)
#			b.wait()
			print "Value of i initially is", i
			print "Inside sentiment function"
#			soft2 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.84.179.174 sh scripts/java.sh'
#			c = subprocess.Popen(soft2, shell=True, stderr=subprocess.PIPE)
#       	 	c.wait()
			command2 = 'nohup scp -P 80 -i /home/priyanshu/Downloads/wipstorm01.pem /home/priyanshu/git/roger/static/documents/'+str(i)+'in.csv ec2-user@54.86.79.168:~/static/documents'
			d = subprocess.Popen(command2, shell=True, stderr=subprocess.PIPE)
			d.wait()
			command3 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.86.79.168 java -jar sentiment.jar /home/ec2-user/static/documents/'+str(i)+'in.csv /home/ec2-user/static/output/'+str(i)+'out.csv'
			e = subprocess.Popen(command3, shell=True, stderr=subprocess.PIPE)
		        print "Ok"
			k+=1
			print "Value of k is", k
			p1 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_cpu -t 40']
			p2 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_mem -t 40']
			p3 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_disc -t 40']
			f1 = subprocess.Popen(p1, shell=True, stdout = subprocess.PIPE)
			output1 = f1.stdout.read()
			value1 = output1.split(':')[1].split('|')[0].strip(" idle").strip('%')
			print value1
			f2 = subprocess.Popen(p2, shell=True, stdout = subprocess.PIPE)
			output2 = f2.stdout.read()
			value2 = output2.split(',')[0].split(':')[1].strip(" %")
			print value2
			f3 = subprocess.Popen(p3, shell=True, stdout = subprocess.PIPE)
			output3 = f3.stdout.read()
			value3 = output3.split('/')[1].split('(')[0].strip(" MB")
			print value3

			value = int(float(value))
			print "Server1 is idle", value
			print "Value of i is",i
			j = i
			if j >= 6:
				break
			if value <= 50:
				while j < 7:
					print "In if"
					j+=1
					command6 = 'nohup scp -P 80 -i /home/priyanshu/Downloads/wipstorm01.pem /home/priyanshu/git/roger/static/documents/'+str(j)+'in.csv ec2-user@54.84.179.174:~/static/documents'
					g = subprocess.Popen(command6, shell=True, stderr=subprocess.PIPE)
					g.wait()
					print "File copied"
					command7 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.84.179.174 java -jar sentiment.jar /home/ec2-user/static/documents/'+str(j)+'in.csv /home/ec2-user/static/output/'+str(j)+'out.csv'
					h = subprocess.Popen(command7, shell=True, stderr=subprocess.PIPE)
					print "Done"	
					command8 = ['/usr/local/nagios/libexec/check_nrpe -H 54.84.179.174 -c check_cpu -t 40']
					r = subprocess.Popen(command8, shell=True, stdout = subprocess.PIPE)
					output1 = r.stdout.read()
					value1 = output1.split(':')[1].split('|')[0].strip(" idle").strip('%')
					value1 = int(float(value1))
					print "Server 2 is idle", value1 
					command9 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_cpu -t 40']
					s = subprocess.Popen(command9, shell=True, stdout = subprocess.PIPE)
					output2 = s.stdout.read()
					value2 = output2.split(':')[1].split('|')[0].strip(" idle").strip('%')
					value2 = int(float(value2))
					print value2
					print "Value of j is", j
					if value2 <= value1 and value1 <= 50: 
						while value1 <= 50:
							command10 = ['/usr/local/nagios/libexec/check_nrpe -H 54.84.179.174 -c check_cpu -t 40']
							t = subprocess.Popen(command10, shell=True, stdout = subprocess.PIPE)
							output3 = t.stdout.read()
							value1 = output3.split(':')[1].split('|')[0].strip(" idle").strip('%')
							value1 = int(float(value1))
							print "Second server idle is", value1
						j+=1
					elif value1 <= value2 and value2 <= 50:
						while value2 <= 50:
							command11 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_cpu -t 40']
							u = subprocess.Popen(command11, shell=True, stdout = subprocess.PIPE)
							output3 = u.stdout.read()
							value2 = output3.split(':')[1].split('|')[0].strip(" idle").strip('%')
							value2 = int(float(value2))
							print "First server idle is", value2
						j+=1
						i = j
						print "Inside one of transition", i 
						break 
					elif value2 <= value1 and value1 >= 50:
						j+=1
					elif value1 <= value2 and value2 >= 50:
						j+=1
						print "Value of j inside trans", j
						i = j
						print "Inside one of transition", i
						break
			else:	
				i+=1
				print "In else"
			print "Value of i outside is", i
 	       	return k
	except Exception, e: 
		print "Exception occured", e
		k = 6
		return k

#tsentiment()

