"""
 find RAW files that match JPGs
"""

import os
import time
import glob
import pickle

LiqV = os.path.join("/Volumes","Liq","src")
RawV = os.path.join("/Volumes","pix15","Pix")
dbName = "liq.pkl"

JpgList = []
RawList = []

def find_jpgs():
	names = []
	here = os.getcwd()
	for monthly in os.listdir(LiqV):
		op = os.path.join(LiqV,monthly,"override")
		if os.path.exists(op) and os.path.isdir(op):
			os.chdir(op)
			for jpg in glob.glob("*.[jJ][pP][Gg]"):
				created = os.stat(jpg).st_birthtime
				names.append({'name':jpg,'jpgDir':monthly,'created':created})
	os.chdir(here)
	return names

def find_all_raw():
	names = []
	here = os.getcwd()
	for yearly in ["2014","2015"]:
		yp = os.path.join(RawV,yearly)
		if not (os.path.exists(yp) and os.path.isdir(yp)):
			continue
		for monthly in os.listdir(yp):
			mp = os.path.join(yp,monthly)
			if not (os.path.exists(mp) and os.path.isdir(mp)):
				continue
			for daily in os.listdir(mp):
				dp = os.path.join(mp,daily)
				if not (os.path.exists(dp) and os.path.isdir(dp)):
					continue
				os.chdir(dp)
				for rwf in glob.glob("*.[rR][aAwW][fFwWfF2]"):
					created = os.stat(rwf).st_birthtime
					names.append({'name':rwf,'rawDir':dp,'created':created})
	os.chdir(here)
	return names

def find_files():
	global JpgList, RawList
	here = os.getcwd()
	if os.path.exists(dbName):
		print "reading from stored data ",dbName
		pkl_file = open(dbName, 'rb')
		JpgList = pickle.load(pkl_file)
		RawList = pickle.load(pkl_file)
		pkl_file.close()
	else:
		print "scanning drives... please wait"
		JpgList = find_jpgs()
		RawList = find_all_raw()
		os.chdir(here)
		output = open(dbName, 'wb')
		pickle.dump(JpgList, output)
		pickle.dump(RawList, output)
		output.close()
	print len(JpgList), 'jpgs found'
	print len(RawList), 'raw files found'

def seek_matching_raw(jpObj):
	global RawList
	jc = jpObj['created']
	r = RawList[0]
	d = abs(r['created']-jc)
	for raw in RawList:
		rd = abs(raw['created']-jc)
		if rd<d:
			r = raw
			d = rd
		if rd == jc:
			print "exact match! "
			break
	print "best match for ",jpObj['name'],'is',os.path.join(r['rawDir'],r['name']),', difference was ',d
	return r

def seek_all_matches():
	for jpg in JpgList:
		seek_matching_raw(jpg)

if __name__ == '__main__':
	find_files()
	seek_all_matches()

