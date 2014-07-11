import server_info
import subprocess, sys
"""@author priyanshu"""

"""Function for splitting the files"""

def split():
	command = "java -jar /home/priyanshu/git/roger/fileupload/split.jar /home/priyanshu/git/roger/media/documents/*"
	p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
	while True:
	    out = p.stderr.read(1)
	    if out == '' and p.poll() != None:
		break
	    if out != '':
		sys.stdout.write(out)
		sys.stdout.flush()

"""Function for merging the files"""

def merge():
	from subprocess import Popen
	cmd1 = 'nohup scp -P 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.86.79.168:~/static/output/* /home/priyanshu/git/roger/static/output'
	a = subprocess.Popen(cmd1, shell=True, stderr=subprocess.PIPE)
	a.wait()
	cmd2 = 'nohup scp -P 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.84.179.174:~/static/output/* /home/priyanshu/git/roger/static/output'
	b = subprocess.Popen(cmd2, shell=True, stderr=subprocess.PIPE)
	b.wait()
	out = "java -jar /home/priyanshu/git/roger/fileupload/merge.jar /home/priyanshu/git/roger/static/output /home/priyanshu/git/roger/static/files/output.csv"
	p = subprocess.Popen(out, shell=True, stderr=subprocess.PIPE)
	while True:
	    out = p.stderr.read(1)
	    if out == '' and p.poll() != None:
		break
	    if out != '':
		sys.stdout.write(out)
		sys.stdout.flush()
#merge()
"""Function for moving from one server to the other based on information from nagios. You can add more checks, see finaltest.py for more info"""

def tsentiment():
	try:
		from subprocess import Popen
		command1 = 'nohup sh /home/priyanshu/Desktop/scripts/ec2_login.sh'
		a = subprocess.Popen(command1, shell=True, stderr=subprocess.PIPE)
		a.wait()
		k = 0
		i = 1 
		while i < 7:
			soft1 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.86.79.168 sh scripts/java.sh'
			b = subprocess.Popen(soft1, shell=True, stderr=subprocess.PIPE)
			b.wait()
			soft2 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.84.179.174 sh scripts/java.sh'
			c = subprocess.Popen(soft2, shell=True, stderr=subprocess.PIPE)
	       	 	c.wait()
			command2 = 'nohup scp -P 80 -i /home/priyanshu/Downloads/wipstorm01.pem /home/priyanshu/git/roger/static/documents/'+str(i)+'in.csv ec2-user@54.86.79.168:~/static/documents'
			d = subprocess.Popen(command2, shell=True, stderr=subprocess.PIPE)
			d.wait()
			command3 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.86.79.168 java -jar sentiment.jar /home/ec2-user/static/documents/'+str(i)+'in.csv /home/ec2-user/static/output/'+str(i)+'out.csv'
			e = subprocess.Popen(command3, shell=True, stderr=subprocess.PIPE)
			k+=1
			command5 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_cpu -t 40']
			f = subprocess.Popen(command5, shell=True, stdout = subprocess.PIPE)
			output = f.stdout.read()
			value = output.split(':')[1].split('|')[0].strip(" idle").strip('%')
			value = int(float(value))
			j = i
			if j >= 6:
				break
			if value <= 50:
				while j < 7:
					j+=1
					command6 = 'nohup scp -P 80 -i /home/priyanshu/Downloads/wipstorm01.pem /home/priyanshu/git/roger/static/documents/'+str(j)+'in.csv ec2-user@54.84.179.174:~/static/documents'
					g = subprocess.Popen(command6, shell=True, stderr=subprocess.PIPE)
					g.wait()
					command7 = 'nohup ssh -p 80 -i /home/priyanshu/Downloads/wipstorm01.pem ec2-user@54.84.179.174 java -jar sentiment.jar /home/ec2-user/static/documents/'+str(j)+'in.csv /home/ec2-user/static/output/'+str(j)+'out.csv'
					h = subprocess.Popen(command7, shell=True, stderr=subprocess.PIPE)
					command8 = ['/usr/local/nagios/libexec/check_nrpe -H 54.84.179.174 -c check_cpu -t 40']
					r = subprocess.Popen(command8, shell=True, stdout = subprocess.PIPE)
					output1 = r.stdout.read()
					value1 = output1.split(':')[1].split('|')[0].strip(" idle").strip('%')
					value1 = int(float(value1))
					command9 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_cpu -t 40']
					s = subprocess.Popen(command9, shell=True, stdout = subprocess.PIPE)
					output2 = s.stdout.read()
					value2 = output2.split(':')[1].split('|')[0].strip(" idle").strip('%')
					value2 = int(float(value2))
					if value2 <= value1 and value1 <= 50: 
						while value1 <= 50:
							command10 = ['/usr/local/nagios/libexec/check_nrpe -H 54.84.179.174 -c check_cpu -t 40']
							t = subprocess.Popen(command10, shell=True, stdout = subprocess.PIPE)
							output3 = t.stdout.read()
							value1 = output3.split(':')[1].split('|')[0].strip(" idle").strip('%')
							value1 = int(float(value1))
						j+=1
					elif value1 <= value2 and value2 <= 50:
						while value2 <= 50:
							command11 = ['/usr/local/nagios/libexec/check_nrpe -H 54.86.79.168 -c check_cpu -t 40']
							u = subprocess.Popen(command11, shell=True, stdout = subprocess.PIPE)
							output3 = u.stdout.read()
							value2 = output3.split(':')[1].split('|')[0].strip(" idle").strip('%')
							value2 = int(float(value2))
						j+=1
						i = j
						break 
					elif value2 <= value1 and value1 >= 50:
						j+=1
					elif value1 <= value2 and value2 >= 50:
						j+=1
						i = j
						break
			else:	
				i+=1
 	       	return k
	except Exception, e: 
		print "Exception occured", e
		k = 6
		return k

#tsentiment()
	
def sentiment():
	from subprocess import Popen

	commands = [
	'java -jar /home/priyanshu/git/roger/fileupload/sentiment.jar /home/priyanshu/git/roger/static/documents/1in.csv /home/priyanshu/git/roger/static/output/1out.csv;date',
	'java -jar /home/priyanshu/git/roger/fileupload/sentiment.jar /home/priyanshu/git/roger/static/documents/2in.csv /home/priyanshu/git/roger/static/output/2out.csv;date',
	'java -jar /home/priyanshu/git/roger/fileupload/sentiment.jar /home/priyanshu/git/roger/static/documents/3in.csv /home/priyanshu/git/roger/static/output/3out.csv;date',
	'java -jar /home/priyanshu/git/roger/fileupload/sentiment.jar /home/priyanshu/git/roger/static/documents/4in.csv /home/priyanshu/git/roger/static/output/4out.csv;date',
	'java -jar /home/priyanshu/git/roger/fileupload/sentiment.jar /home/priyanshu/git/roger/static/documents/5in.csv /home/priyanshu/git/roger/static/output/5out.csv;date',
	]
# run in parallel
	processes = [Popen(cmd, shell=True) for cmd in commands]
# do other things here..
# wait for completion
	for p in processes: p.wait()

