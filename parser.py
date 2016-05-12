#!/usr/bin/python
#Reading statemen list and executing it 

import re
import os
import pwd
import time
import stat

_start = False
_finish = False
_directory = False
_file = False
_readable = False
_writeable = False
_executable = False
file_path = ""
file_owner =""
file_size = ""
file_name = ""
file_access = ""
file_lmod = ""


#Do proper action regarding to statements and Unix commands
def execute(stmt_exp, command):
	l1 = len(stmt_exp)
	c =0
	while c<l1 :
		if stmt_exp[c] == "start":
			global _start
			_start = True
			#stmt_exp = _stmt.replace("start","_start")
		elif stmt_exp[c] == "finish":
			global _finish
			_finish = True
			#stmt_exp = _stmt.replace("finish","_finish")
		elif stmt_exp[c] == "directory":
			global _directory
			_directory = True
			#stmt_exp = _stmt.replace("directory","_dirctory")
		elif stmt_exp[c] == "file":
			global _file
			_file = True
			#stmt_exp = _stmt.replace("file","_file")
		elif stmt_exp[c] == "_readable":
			global _readable
			_readable = True
			#stmt_exp = _stmt.replace("readable","_readable")
		elif stmt_exp[c] == "_writeable":
			global _writeable
			_writeable = True
			#stmt_exp = _stmt.replace("_writeable","_writeable")
		elif stmt_exp[c] == "_executable":
			global _executable
			_executable = True
		elif stmt_exp[c][0] == "/":
			#Check name of the file or dir
			print "name ", nameCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "c":
			#Check items content
			contentCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "o":
			#Check items owner
			print "owner ", ownerCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "p":
			#Check permissions
			print "perm ", permCheck(stmt_exp[c])
			permCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "d":
			#Check date of the item
			print "date ", dateCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "s":
			#Check size of the item
			print "perm ", sizeCheck(stmt_exp[c])
		c = c+1

def nameCheck(stmt_exp):
	length = len(stmt_exp)
	rexp = stmt_exp[1:length-1]
	pattern = re.compile(rexp)
	res = pattern.search(file_name)
	if res is not None:
		return True
	else: 
		return False

def ownerCheck(stmt_exp):
	length = len(stmt_exp)
	rexp = stmt_exp[2:length-1]
	pattern = re.compile(rexp)
	res = pattern.search(file_owner)
	if res is not None:
		return True
	else:
		return False

def contentCheck(stmt_exp):
	length = len(stmt_exp)
	rexp = stmt_exp[2:length-1]
	pattern = re.compile(rexp)
	res = pattern.search(file_content)
	if res is not None:
		return True
	else:
		return False

def permCheck(stmt_exp):
	length = len(stmt_exp)
	rexp = stmt_exp[2:length-1]
	pattern = re.compile(rexp)
	res = pattern.search(file_access)
	if res is not None:
		return True
	else:
		return False

def dateCheck(stmt_exp):
	length = len(stmt_exp)
	if stmt_exp.endswith('/'):
		rexp = stmt_exp[2:length-1]
		mod_time = time.strptime(rexp, '%d-%m-%Y')
		return mod_time == file_lmod
	elif stmt_exp.endswith('a'):
		rexp = stmt_exp[2:length-2]
		mod_time = time.strptime(rexp, '%d-%m-%Y')
		return mod_time < file_lmod
	elif stmt_exp.endswith('b'):
		rexp = stmt_exp[2:length-2]
		mod_time = time.strptime(rexp, '%d-%m-%Y')
		return mod_time > file_lmod

def sizeCheck(stmt_exp):
	length = len(stmt_exp)
	if stmt_exp.endswith('/'):
		rexp = stmt_exp[2:length-1]
		return rexp == file_size
		return mod_time == file_lmod
	elif stmt_exp.endswith('l'):
		rexp = stmt_exp[2:length-2]
		return rexp >= file_size
	elif stmt_exp.endswith('m'):
		return rexp <= file_size


#read statement lines and parse them
def parse(stmt):
	parts =  re.split(r'=>', stmt)
	stmt_exp = re.split(r'[&| ]', parts[0])
	stmt_exp = filter(None, stmt_exp)
	command = re.split(r'[;]', parts[1])
	command = filter(None, command)
	print stmt_exp
	print command
	execute(stmt_exp , command)

def get_info(filename):
	global file_owner,file_size,file_access,file_lmod,file_name
	st = os.stat(filename)
	file_name = re.search(r'/(.*$)', filename).groups()[0]
	file_owner = pwd.getpwuid(st.st_uid).pw_name
	file_size = st.st_size
	file_access = oct(stat.S_IMODE(st.st_mode))[1:]
	#last_modified = time.ctime(os.path.getmtime(filename))
	mod_time = time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(filename)))
	file_lmod = time.strptime(mod_time, '%d/%m/%Y')


def run(sPath , fPath):
	global file_path
	global _stmt 
	file_path = fPath
	f = open( sPath, 'r+')
	_stmt = f.readline()
	get_info(file_path)
	parse(_stmt)
	
	print "start", _start
	print "finish ", _finish
	print "dir", _directory
	print "file", _file
	print "read ", _readable
	print "write ",_writeable
	print "exec ",_executable
	print "access ", file_access

run("testpath.txt" , "./AAA")


