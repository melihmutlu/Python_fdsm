#!/usr/bin/python
#Parser !!

import re
import os
import pwd
import time
import stat

#Default parameters
_stmt = ""
_commands = ""
_start = False
_finish = False
_directory = False
_file = False
_readable = False
_writeable = False
_executable = False
_name = False
_size = False
_owner = False
_perm = False
_content = False
_date = False
file_path = ""
file_owner =""
file_size = ""
file_name = ""
file_access = ""
file_lmod = ""


#Do proper action regarding to statements and Unix commands
def execute(stmt_exp, command):
	global _stmt
	global _name,_owner,_content,_date,_size
	l1 = len(stmt_exp)
	c =0
	while c<l1 :
		if stmt_exp[c] == "start":
			_stmt = _stmt.replace("start","_start")
			if step == 0:
				global _start
				_start = True
		elif stmt_exp[c] == "finish":
			_stmt = _stmt.replace("finish","_finish")
			if step == stop:
				global _finish
				_finish = True
		elif stmt_exp[c] == "directory":
			global _directory
			_directory = os.path.isdir(file_path)
			_stmt = _stmt.replace("directory","_directory")
		elif stmt_exp[c] == "file":
			global _file
			_file = os.path.isfile(file_path)
			_stmt = _stmt.replace("file","_file")
		elif stmt_exp[c][0] == "/":
			#Check name of the file or dir
			_name = nameCheck(stmt_exp[c])
			_stmt = _stmt.replace(stmt_exp[c], "_name")
			#print "name ", nameCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "c":
			#Check items content
			_content = contentCheck(stmt_exp[c])
			_stmt = _stmt.replace(stmt_exp[c], "_content")
		elif stmt_exp[c][0] == "o":
			#Check items owner
			_owner = ownerCheck(stmt_exp[c])
			_stmt = _stmt.replace(stmt_exp[c], "_owner")
			##print "owner ", _owner
		elif stmt_exp[c][0] == "p":
			#Check permissions
			_perm = permCheck(stmt_exp[c])
			_stmt = _stmt.replace(stmt_exp[c], "_perm")
			##print "perm ", permCheck(stmt_exp[c])
			permCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "d":
			#Check date of the item
			_date =  dateCheck(stmt_exp[c])
			_stmt = _stmt.replace(stmt_exp[c], "_date")
			##print "date ", dateCheck(stmt_exp[c])
		elif stmt_exp[c][0] == "s":
			#Check size of the item
			_size = sizeCheck(stmt_exp[c])
			_stmt = _stmt.replace(stmt_exp[c], "_size" )
			##print "size ", _size
		c = c+1


#CChecker functions ...

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

#-------------------------------		
#I don't understand how it works
def contentCheck(stmt_exp):
	length = len(stmt_exp)
	rexp = stmt_exp[2:length-1]
	pattern = re.compile(rexp)
	res = pattern.search(file_content)
	if res is not None:
		return True
	else:
		return False
#------------------------------

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
		return rexp > file_size
	elif stmt_exp.endswith('m'):
		rexp = stmt_exp[2:length-2]
		return rexp < file_size


#read statement lines and parse them
def parse(stmt):
	global _stmt, _commands
	parts =  re.split(r'=>', stmt)
	_stmt = parts[0]
	stmt_exp = re.split(r'[&|() ]', parts[0])
	stmt_exp = filter(None, stmt_exp)
	_commands = parts[1]
	command = re.split(r'[;]', parts[1])
	command = filter(None, command)
	print stmt_exp
	print command
	execute(stmt_exp , command)

#Get info about the file in the given path
def get_info(filename):
	global file_owner,file_size,file_access,file_lmod,file_name
	global _readable, _writeable, _executable
	st = os.stat(filename)
	file_name = re.search(r'/(.*$)', filename).groups()[0]
	file_owner = pwd.getpwuid(st.st_uid).pw_name
	file_size = st.st_size
	file_access = oct(stat.S_IMODE(st.st_mode))[1:]
	_readable = os.access(filename, os.R_OK)
	_writeable =  os.access(filename, os.W_OK)
	_executable = os.access(filename, os.X_OK)
	#last_modified = time.ctime(os.path.getmtime(filename))
	mod_time = time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(filename)))
	file_lmod = time.strptime(mod_time, '%d/%m/%Y')


#Run parser , statementlist path and file or dir path are parameters
def run(sPath , fPath):
	global file_path
	global _stmt,_commands
	file_path = fPath
	f = open( sPath, 'r+')
	get_info(file_path)
	parse(f.readline())
	
	print "start", _start
	print "finish ", _finish
	print "dir", _directory
	print "file", _file
	print "read ", _readable
	print "write ",_writeable
	print "exec ",_executable
	print "access ", file_access

	_stmt = _stmt.replace("&&", "&")
	_stmt = _stmt.replace("||", "|")

	if eval(_stmt):
		return _commands
	else:
		return None

