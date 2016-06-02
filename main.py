#!/usr/bin/python

import re
import os
import sys
import getopt
import pwd
import time
import Queue

from parser import run
import subprocess

bfs_traverse_opt = False
full_path_opt = False
stmt_file_opt = False
stmt_file_path = ""
amazon_instance_opt = False
amazon_instance_path = ""
root_directory_opt = False
root_directory = ""
toTraverse_path = ""
instance_ip = ""

def parse(argv):
	optlist, args = getopt.getopt(argv[1:], 'bfs:i:')
	for tup in optlist:
		if tup[0] == "-b":
			global bfs_traverse_opt
			bfs_traverse_opt = True
		if tup[0] == "-f":
			global full_path_opt
			full_path_opt = True
		if tup[0] == "-s":
			global stmt_file_opt
			stmt_file_opt = True
			global stmt_file_path
			stmt_file_path = tup[1]
		if tup[0] == "-i":
			global amazon_instance_opt
			amazon_instance_opt = True
			global amazon_instance_path
			amazon_instance_path = tup[1]
		if len(args) == 1:
			global root_directory_opt
			root_directory_opt = True
			global root_directory
			root_directory = args[0]

	if amazon_instance_opt:
		amazonCloud(optlist,args)

def dirTraverse(opt, path):
	if opt:
		dirTraverse_BFS(path)
	else:
		dirTraverse_DFS(path, 0, 0)

def dirTraverse_DFS2(rootDir):
	for dirName, subdirList, fileList in os.walk(rootDir):
	    print dirName
	    for fname in fileList:
	    	fullpath = dirName + "/" + fname
	    	print fullpath

def dirTraverse_DFS(path, step, stop):
	if os.path.exists(path):
		curlist = os.listdir(path)
		curlist.sort()
		#print curlist
		for item in curlist:
			item_path = path + "/" + item
			print item_path
			stop += 1
			commands = run(stmt_file_path, item_path, step, stop)
			runFdsm(commands, item_path)
			if os.path.isdir(item_path):
				dirTraverse_DFS(item_path, step, stop)
			step += 1
		commands = run(stmt_file_path, "", step, stop)
		#print commands
		runFdsm(commands, "")


def amazonCloud(optlist,args):
	import boto3 

	global stmt_file_path
	instance_id = ""
	global instance_ip 
	mark = 0
	ec2 = boto3.resource('ec2')
	#Find AWS instance
	instances = ec2.instances.filter(
	    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	for instance in instances:
		if instance.instance_id == amazon_instance_path:
			instance_ip = instance.public_ip_address
			cmd = " python ./main.py fdsm "
			for tup in optlist:
				if not tup[0] == "-i":
					cmd += tup[0] + " "
					if not (tup[1] == '' or tup[1].isspace()):
						cmd += tup[1] + " "
			print cmd

			keyfile = '-i ./amazon.pem '
			scpstring = r'scp -o StrictHostKeyChecking=no '
			sshstring = r'ssh -o StrictHostKeyChecking=no '
			machine = 'ubuntu@' 
			files = ' ./parser.py ./main.py ' + stmt_file_path + ' '
			target = ':/home/ubuntu' 
			command_scp = scpstring + keyfile + files + machine + instance_ip + target 
			command_ssh = sshstring + keyfile + machine + instance_ip + cmd 

			subprocess.check_output(command_scp,shell=True)
			output = subprocess.check_output(command_ssh,shell=True)
			print output
			
			mark = 1

	if mark == 0:
		print "Error: Id not found"
		

def dirTraverse_BFS(rootDir):
	step = 0
	stop = 0
	dirlist = Queue.Queue()
	dirlist.put(rootDir)
	while not dirlist.empty():
		fullpathname = dirlist.get()
		if os.path.exists(fullpathname):
			curlist = os.listdir(fullpathname)
			curlist.sort()
			stop += len(curlist)
			for fdname in curlist:
				item_path = fullpathname + "/" + fdname
				if os.path.isdir(item_path):
					dirlist.put(item_path)
				print item_path 
				commands = run(stmt_file_path, item_path, step, stop)
				#print commands
				runFdsm(commands, item_path)
				step += 1
	commands = run(stmt_file_path, "", step, stop)
	#print commands
	runFdsm(commands, "")

def runFdsm(commands_str, filepath):
	if commands_str is not None:
		for subcmd in commands_str.split(";"):
			subcmd = subcmd.strip()
			if (not subcmd or subcmd.isspace() or len(subcmd) == 0):
				break
			#print subcmd
			if subcmd[0] == '{' and subcmd[len(subcmd)-1] == '}':
				cmd = subcmd[1:len(subcmd)-1].decode('string_escape')
				exec(cmd) in globals()

			else:
				ul = subcmd.split()
				for temp in ul:
					if temp == "$MATCHED":
						ul[ul.index("$MATCHED")] = filepath
				subprocess.call(ul)

def main():
	global stmt_file_path
	parse(sys.argv[1:])

	if amazon_instance_opt == False:
		if not stmt_file_opt:
			f = open("stdin_stmt","w")
			lines = sys.stdin.readlines() ;
			for line in lines:
				f.write(line)
			f.close()
			stmt_file_path = "./stdin_stmt"

		if full_path_opt:
			toTraverse_path = os.getcwd()
		else:
			toTraverse_path = "."
		if root_directory_opt:
			toTraverse_path = root_directory
		dirTraverse(bfs_traverse_opt, toTraverse_path)
	
	else : 
		com = "ssh -o StrictHostKeyChecking=no -i ./amazon.pem ubuntu@" + instance_ip + " rm main.py parser.py parser.pyc " + stmt_file_path 
		subprocess.check_output(com,shell=True)


if __name__ == '__main__':
	main()