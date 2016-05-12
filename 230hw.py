#!/usr/bin/python
#Reading statemen list and executing it 

import re

_stmt = "/junk/ && directory => rm $MATCHED ;"
_start = False
_finish = False
_directory = False
_file = False
_readable = False
_writeable = False
_executable = False


#Do proper action regarding to statements and Unix commands
def execute(stmt_exp, command):
	l1 = len(stmt_exp)
	c =0
	while(c<l1):
		if(stmt_exp[c] == "start"):
			global _start
			_start = True
		else if(stmt_exp[c] == "finish"):
			global _finish
			_finish = True
		else if(stmt_exp[c] == "directory"):
			global _directory
			_directory = True
		else if(stmt_exp[c] == "file")
			global _file
			_file = True
		else if(stmt_exp[c] == "_readable"):
			global _readable
			_readable = True
		else if(stmt_exp[c] == "_writeable"):
			global _writeable
			_writeable = True
		else if(stmt_exp[c] == "_executable"):
			global _executable
			_executable = True
		else if(stmt_exp[c][0] == "/"):
			#Check name of the file or dir 
		else if(stmt_exp[c][0] == "c"):
			#Check items content
		else if(stmt_exp[c][0] == "o"):
			#Check items owner
		else if(stmt_exp[c][0] == "p"):
			#Check permissions
		else if(stmt_exp[c][0] == "d"):
			#Check date of the item
		else if(stmt_exp[c][0] == "s"):
			#Check size of the item


#read statement lines and parse them
def parse(stmt):
	parts =  re.split(r'=>', stmt)
	stmt_exp = re.split(r'[(&&)(||); ]', parts[0])
	stmt_exp = filter(None, stmt_exp)
	command = re.split(r'[;]', parts[1])
	command = filter(None, command)
	print stmt_exp
	print command
	execute(stmt_exp , command)


parse(stmt)
