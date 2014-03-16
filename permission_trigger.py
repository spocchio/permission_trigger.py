#!/usr/bin/python3

#
# permission_trigger.py, Antonio Ragagnin (2014)
#
# permission_trigger.py is a multiplatform tool that checks
# for filesystem changes. Once a change is found a program
# is executed with the file itself as parameter.
#
# usage info: permission_trigger.py --help

import os
import stat
import argparse
import time
import subprocess

def main():
	parser = argparse.ArgumentParser(description='permission_trigger.py execute something when the permission of a file changes.\r\nAntonio Ragagnin (2014)')
	parser.add_argument('--folder', type=str, help='folder to browse (default is current folder)',default='.')
	parser.add_argument('--execute', type=str, help='process to execute when permission change (if not specified, the file tiself is executed)')
	parser.add_argument('--sleep', type=int, help='interval between the checking of change in seconds (default: 10)',default='10')
	parser.add_argument('--permission', type=str, help='permission to check, r: read, w: write, x:execution (default: x)',default='x')
	args = parser.parse_args()

	print ('recursively removing "%s" permission from folder "%s"...'%(args.permission,args.folder))
	toggle_permissions(args.folder,args.permission)
	print ('watching folder "%s" for changes in permission "%s", every %d seconds.'%(args.folder,args.permission,args.sleep))
	try:
		while True:
			file_changed = check_permissions(args.folder,args.permission)
			if(file_changed!=None):
				fullname = args.folder+os.sep+file_changed
				if(not args.execute):
					print('executing: ',' '.join([fullname]));
					subprocess.Popen([fullname])
				else:
					print('executing: ',' '.join([ args.execute,fullname]));
					subprocess.Popen([ args.execute,fullname])
				print ('removing "%s" permission from file/folder "%s"'%(args.permission,fullname))
				toggle_permission(fullname,args.permission)
			time.sleep(args.sleep)
	except KeyboardInterrupt:
		print ('^C received, bye!')
						
def add_flag(stat,flag):
	return bool(stat|flag)

def toggle_flag(stat,flag):
	return bool(not bool((not stat)|flag))

def check_flag(stat,flag):
	return bool(stat & flag)
def char2flags(c):
	if c=='r':	return [stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH]
	if c=='w':	return [stat.S_IWUSR|stat.S_IWGRP|stat.S_IWOTH]
	if c=='x':	return [stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH]

def toggle_permission(file,permission):
	for flag in char2flags(permission):
		os.chmod(file, toggle_flag(os.stat(file).st_mode,flag))

def check_permission(file,permission):
	result = True
	for flag in char2flags(permission):
		result = result & check_flag(os.stat(file).st_mode,flag)
	return result
		
def add_permission(file,permission):
	for flag in char2flags(permission):
		os.chmod(file, add_flag(os.stat(file).st_mode,flag))
	

def toggle_permissions(folder,permission):
		for dp, dn, filenames in os.walk(folder):
			toggle_permission(dp,permission)
			for f in filenames:
				toggle_permission(dp+os.sep+f,permission)

def check_permissions(folder,permission):
		for dp, dn, filenames in os.walk(folder):
			if check_permission(dp,permission): return dn
			for f in filenames:
				if check_permission(dp+os.sep+f,permission): return f
		return None
				
def add_permissions(folder,permission):
		for dp, dn, filenames in os.walk(folder):
			add_permission(dp,permission)
			for f in filenames:
				add_permission(dp+os.sep+f,permission)

if __name__ == "__main__": 
	main()
