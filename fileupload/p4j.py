import subprocess, sys
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

def merge():
	out = "java -jar /home/priyanshu/git/roger/fileupload/merge.jar /home/priyanshu/git/roger/static/output /home/priyanshu/git/roger/static/files/output.csv"
	p = subprocess.Popen(out, shell=True, stderr=subprocess.PIPE)
	while True:
	    out = p.stderr.read(1)
	    if out == '' and p.poll() != None:
		break
	    if out != '':
		sys.stdout.write(out)
		sys.stdout.flush()

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

#	cmd = "java -jar /home/priyanshu/git/roger/fileupload/sentiment.jar /home/priyanshu/git/roger/static/documents/1in.csv /home/priyanshu/git/roger/static/output/1out.csv"
#	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
#	while True:
#	    out = p.stderr.read(1)
#	    if out == '' and p.poll() != None:
#		break
#	    if out != '':
#		sys.stdout.write(out)
#		sys.stdout.flush()
