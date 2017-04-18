'''
For C.L.A.R.A Auto Updater
 - Description : T32 Util
 - Author : Taesung Jung (tjung@qti.qualcomm.com/nkg2502@gmail.com)
 - First release : 12/17/2013
 - modified : 04/05/2014
 - Filename : auto_updater.py
 - Usage : 
        python auto_updater.py 
'''

import urllib2
import urllib
import os
import zipfile
import urllib
import shutil
import time
from datetime import datetime
import json
import sys
import Tkinter
import tkMessageBox

# constants
clara_path = '.'
try:
	clara_path = os.environ['CLARA_PATH']
except:
	pass

current_version_path = r'interface\version.txt'
dev_mode_path = r'interface\dev.txt'
#latest_version_url = r'https://github.qualcomm.com/cheonhop/clara/raw/master/interface/version.txt'
#latest_version_url = r'http://catseye.ap.qualcomm.com/clara/master/interface/version.txt'
latest_version_url = r'http://qctk-harvl23.ap.qualcomm.com/clara/clara/interface/version.txt'

#latest_archive_url = r'https://github.qualcomm.com/cheonhop/clara/archive/master.zip'
#latest_archive_url = r'http://catseye.ap.qualcomm.com/clara/master.zip'
latest_archive_url = r'http://qctk-harvl23.ap.qualcomm.com/clara/clara.zip'
latest_archive_file_name = 'clara.' + time.strftime("%Y.%m.%d[%H.%M.%S]", time.localtime()) + '.zip'
temp_dir_name = time.strftime("%Y%m%d%H%M%S", time.localtime())

latest_json_name = 'latest.json'
update_period = 1 # one day, one execution

current_version = 0
latest_version = 1

# reference : shutil.copytree function
def overwrite_files(src, dst):
	'''Recursively copy
	'''
	names = os.listdir(src)

	try:
		os.makedirs(dst)
	except:
		pass
	for name in names:
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if os.path.isdir(srcname):
				overwrite_files(srcname, dstname)
			else:
				shutil.copy2(srcname, dstname)
		except Exception as e:
			print str(e)

def main():

	os.chdir(clara_path)

	# check dev mode
	if os.path.exists(dev_mode_path):
		print 'DEV MODE Enabled: NO UPGRADE'
		time.sleep(1)
		return

	# check update period 
	is_checked = False

	try:
		with open(latest_json_name, 'r') as check_file:

			latest_json = json.loads(check_file.read())

			today = int(datetime.now().strftime('%Y%m%d'))
			last_checked = int(latest_json['last_checked'])

			if update_period > today - last_checked:
				is_checked = True
	except Exception as e:
		pass

	if not is_checked:
		try:
			with open(latest_json_name, 'w') as check_file:
				latest_json = {}
				latest_json['last_checked'] = int(datetime.now().strftime('%Y%m%d'))
				json.dump(latest_json, check_file)
		except Exception as e:
			pass
	else:
		print 'You have already checked the latest version today.'
		time.sleep(1)
		sys.exit(0)

	# check version
	print 'Checking latest version...'

	# check server connection
	try:
		print 'Trying to connect server...'
		urllib.urlopen(latest_version_url)

	except Exception as e:
		print 'Server Error!'
		# can not connect server
		hidden_root = Tkinter.Tk() 
		hidden_root.withdraw() 
		dialog_msg = ['Server Error!\n'
				'Please check connection!\n',
				'Server URL', latest_version_url]
		tkMessageBox.showerror('Server Error!','\n'.join(dialog_msg), master=hidden_root)
		time.sleep(1)
		return

	# file not exist or conversion error (str -> int)
	try:
		current_version = int(open(current_version_path, 'r').readline())
		latest_version = int(urllib.urlopen(latest_version_url).readline())

	except Exception as e:
		current_version = 0
		latest_version = 1

	if latest_version > current_version:

		print 'Trying to download latest version...'

		# ask upgrade
		hidden_root = Tkinter.Tk() 
		hidden_root.withdraw() 
		dialog_msg = [ 'BEWARE overwrite your files!\n',
				'Do you want to upgrade C.L.A.R.A?\n',
				'Latest Version: ' + str(latest_version),
				'Current Version: ' + str(current_version) ]
		if not tkMessageBox.askokcancel('New Version Upgrade',
				'\n'.join(dialog_msg), master=hidden_root):
			print 'Upgrade Canceled'
			time.sleep(1)
			return

		# keep clara.bat
		try:
			os.rename('clara.bat', 'clara.backup.bat')
		except Exception as e:
			pass

		# download latest version
		print 'Downloading latest C.L.A.R.A...'
		f = urllib2.urlopen(latest_archive_url)
		with open(latest_archive_file_name, 'wb') as latest_archive:
			latest_archive.write(f.read())

		# extract and overwrite latest version
		print 'Extracting all files...'
		zip_handler = zipfile.ZipFile(latest_archive_file_name, "r")
		os.mkdir(temp_dir_name)
		zip_handler.extractall(temp_dir_name)
		zip_handler.close()

		print 'Removing old files...'
		shutil.rmtree('cmm')
		shutil.rmtree('elf')
		shutil.rmtree('platforms')

		print 'Updating all files...'
		overwrite_files(temp_dir_name + '/clara', os.getcwd())

		print 'Removing all temporary files...'
		os.remove(latest_archive_file_name)
		shutil.rmtree(temp_dir_name)

		# restore clara.bat
		try:
			#os.remove('clara.bat')
			os.rename('clara.bat', 'clara.new.bat')
			os.rename('clara.backup.bat', 'clara.bat')
		except Exception as e:
			pass

		print 'Complete!'

	else:
		print 'Current Version is Latest! [' + str(current_version) + '] ' + ' Server version [' + str(latest_version) + ']'
	time.sleep(2)

if "__main__" == __name__:
	main()
