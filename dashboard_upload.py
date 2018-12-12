#!/usr/bin/env python3

import requests
import json
import sys
import os
import datetime

folder = 'dashboards/'
logfile = 'chrono_refresh.log' #Rename this before putting into production
server = sys.argv[1]
chronograf_api_url = 'http://' + server + ':8888/chronograf/v1/dashboards'
jsonhead = {'Content-type': 'application/json'}

def writeLogFile(destination_file,message):
        log = open(destination_file, 'a')
        log.write(str(datetime.datetime.now()) + ' ' + message)
        log.close()

#Pull List of Dashboards from Chronograf API:
try:
        req = requests.get(chronograf_api_url)
except:
        msg = 'Error connecting to {}\n'.format(sys.argv[1])
        print(msg)
        writeLogFile(logfile,msg)
        sys.exit(1)
#
for dash in req.json()['dashboards']:
    dash_name = '{}'.format(dash['name'].replace(' ','_').lower())
    dash_id = '{}'.format(dash['id'])
    try:
        clean = requests.delete(chronograf_api_url + '/' + dash_id)
        if clean.status_code == 204:
            msg = 'Dashboard {} deleted successfully\n'.format(dash_name)
        else:
            msg = 'An issue occured attempting to delete {}. Return code is {}\n'.format(dash_name, clean.status_code)
        writeLogFile(logfile,msg)
    except:
        msg = 'Error connecting to {}\n'.format(sys.argv[1])
        writeLogFile(logfile,msg)

#Get list of files on disk to upload
dirlist = os.listdir(folder)

#print('Files found on disk:\n{}\n'.format(filelist))
for directory in dirlist:
	filelist = os.listdir(folder + directory)

	for filename in filelist:
        	with open(folder + directory + '/' +  filename) as json_file:
                	json_data = json.load(json_file)
                	j = json.dumps(json_data['dashboard'])
        	try:
                	d = requests.post(chronograf_api_url,headers=jsonhead,data=j)
                	if d.status_code == 201:
                        	msg = '{} successfully uploaded\n'.format(filename)
                        	writeLogFile(logfile,msg)
                	else:
                        	msg = '{} failed to load\n'.format(filename)
                        	writeLogFile(logfile,msg)
        	except:
                	msg = 'Connection error when uploading {} to {}\n'.format(filename,sys.argv[1])
                	writeLogFile(logfile,msg)



