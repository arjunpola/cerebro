from django.http import HttpResponse
from django.shortcuts import render
from eeg.models import User, Data


def home(request):
	return render(request, 'index.html')

def dash(request):
	if 'uname' in request.GET and request.GET['uname']:
		uname=request.GET['uname']
		query=User.objects.filter(name=uname)
		query2=Data.objects.filter(name=uname)
		if not query:
			u1= User(name=uname)
			u1.save()
		return render(request, 'dash.html',{'name':uname,'items':query2})

def add(request):
	if 'obname' in request.GET and request.GET['obname']:
		obname=request.GET['obname']
		uname=request.GET['uname']
		namequery=User.objects.get(name=uname)
		query2=Data.objects.filter(name=uname)
		u2= Data(name=namequery,item=obname)
		u2.save()
		return render(request, 'dash.html',{'name':uname,'items':query2})

def dele(request):
	if 'obname' in request.GET and request.GET['obname']:
		obname=request.GET['obname']
		uname=request.GET['uname']
		namequery=User.objects.get(name=uname)
		query=Data.objects.filter(name=namequery,item=obname)
		query.delete()
		query2=Data.objects.filter(name=uname)
		return render(request, 'dash.html',{'name':uname,'items':query2})

def train(request):
	if 'obname' in request.GET and request.GET['obname']:
		obname=request.GET['obname']
		uname=request.GET['uname']
		import random 
		import time
		import ctypes
		import sys
		import os
		from ctypes import *
		from numpy import *
		import numpy as np
		import scipy as sp
		import time
		from ctypes.util import find_library
		ED_COUNTER = 0
		ED_INTERPOLATED=1
		ED_RAW_CQ=2
		ED_AF3=3
		ED_F7=4
		ED_F3=5
		ED_FC5=6
		ED_T7=7
		ED_P7=8
		ED_O1=9
		ED_O2=10
		ED_P8=11
		ED_T8=12
		ED_FC6=13
		ED_F4=14
		ED_F8=15
		ED_AF4=16
		ED_GYROX=17
		ED_GYROY=18
		ED_TIMESTAMP=19
		ED_ES_TIMESTAMP=20
		ED_FUNC_ID=21
		ED_FUNC_VALUE=22
		ED_MARKER=23
		ED_SYNC_SIGNAL=24

		targetChannelList = [ED_COUNTER,ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]
		libEDK = cdll.LoadLibrary(".\\edk.dll")
		
		header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
		write = sys.stdout.write
		eEvent      = libEDK.EE_EmoEngineEventCreate()
		eState      = libEDK.EE_EmoStateCreate()
		userID            = c_uint(0)
		nSamples   = c_uint(0)
		nSam       = c_uint(0)
		nSamplesTaken  = pointer(nSamples)
		da = zeros(128,double)
		data     = pointer(c_double(0))
		user                    = pointer(userID)
		composerPort          = c_uint(1726)
		secs      = c_float(1)
		datarate    = c_uint(0)
		readytocollect    = False
		option      = c_int(0)
		state     = c_int(0)

		if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
			return HttpResponse("Emotiv Engine start up failed.")
           
		#print "Start receiving EEG Data! Press any key to stop logging...\n"
		f = file('EEG.txt', 'w')
		f = open('EEG.txt', 'w')
		#print >> f,header
		    
		hData = libEDK.EE_DataCreate()
		libEDK.EE_DataSetBufferSizeInSec(secs)

		ending=0
		starting = time.time()
		while (1):
			if ending>4:
				break
			state = libEDK.EE_EngineGetNextEvent(eEvent)
			if state == 0:
				eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
				libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
				if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
					#print "User added"
					libEDK.EE_DataAcquisitionEnable(userID,True)
					readytocollect = True

			if readytocollect==True:    
				libEDK.EE_DataUpdateHandle(0, hData)
				libEDK.EE_DataGetNumberOfSample(hData,nSamplesTaken)
				#print "Updated :",nSamplesTaken[0]
				if nSamplesTaken[0] != 0:
					nSam=nSamplesTaken[0]
					arr=(ctypes.c_double*nSamplesTaken[0])()
					ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))
					#libEDK.EE_DataGet(hData, 3,byref(arr), nSam)                         
					data = array('d')#zeros(nSamplesTaken[0],double)
					for sampleIdx in range(nSamplesTaken[0]): 
						for i in range(22): 
							libEDK.EE_DataGet(hData,targetChannelList[i],byref(arr), nSam)
							print >>f,arr[sampleIdx],",",                    
						print >>f,'\n'              
			time.sleep(0.2)
			ending=time.time()-starting #this is supposed to be out of infinite while loop
		f.close()
		#infinite while ends here
		libEDK.EE_DataFree(hData)

		#---------------------------------------------------------------------------------------------------------------------------------------------------------------
		libEDK.EE_EngineDisconnect()
		libEDK.EE_EmoStateFree(eState)
		libEDK.EE_EmoEngineEventFree(eEvent)
		eeg_doc = sp.genfromtxt("EEG.txt", delimiter=" , ")
		e=eeg_doc[:,1:15]
		ea=np.mean(e, axis=0)
		namequery=User.objects.get(name=uname)
		query2=Data.objects.filter(name=uname)
		u=Data.objects.get(name=namequery,item=obname)
		
		[u.e1,u.e2,u.e3,u.e4,u.e5,u.e6,u.e7,u.e8,u.e9,u.e10,u.e11,u.e12,u.e13,u.e14]=ea
		u.save()

		return render(request, 'dash.html',{'name':uname,'items':query2})
		#return HttpResponse("ok")


def trainupdate(request):
	if 'obname' in request.GET and request.GET['obname']:
		obname=request.GET['obname']
		uname=request.GET['uname']
		import random 
		import time
		import ctypes
		import sys
		import os
		from ctypes import *
		from numpy import *
		import numpy as np
		import scipy as sp
		import time
		from ctypes.util import find_library
		libEDK = cdll.LoadLibrary(".\\edk.dll")
		ED_COUNTER = 0
		ED_INTERPOLATED=1
		ED_RAW_CQ=2
		ED_AF3=3
		ED_F7=4
		ED_F3=5
		ED_FC5=6
		ED_T7=7
		ED_P7=8
		ED_O1=9
		ED_O2=10
		ED_P8=11
		ED_T8=12
		ED_FC6=13
		ED_F4=14
		ED_F8=15
		ED_AF4=16
		ED_GYROX=17
		ED_GYROY=18
		ED_TIMESTAMP=19
		ED_ES_TIMESTAMP=20
		ED_FUNC_ID=21
		ED_FUNC_VALUE=22
		ED_MARKER=23
		ED_SYNC_SIGNAL=24

		targetChannelList = [ED_COUNTER,ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]
		#header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
		write = sys.stdout.write
		eEvent      = libEDK.EE_EmoEngineEventCreate()
		eState      = libEDK.EE_EmoStateCreate()
		userID            = c_uint(0)
		nSamples   = c_uint(0)
		nSam       = c_uint(0)
		nSamplesTaken  = pointer(nSamples)
		da = zeros(128,double)
		data     = pointer(c_double(0))
		user                    = pointer(userID)
		composerPort          = c_uint(1726)
		secs      = c_float(1)
		datarate    = c_uint(0)
		readytocollect    = False
		option      = c_int(0)
		state     = c_int(0)

		if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
			return HttpResponse("Emotiv Engine start up failed.")
           
		#print "Start receiving EEG Data! Press any key to stop logging...\n"
		f = file('EEG.txt', 'w')
		f = open('EEG.txt', 'w')
		#print >> f,header
		    
		hData = libEDK.EE_DataCreate()
		libEDK.EE_DataSetBufferSizeInSec(secs)

		ending=0
		starting = time.time()
		while (1):
			if ending>4:
				break
			state = libEDK.EE_EngineGetNextEvent(eEvent)
			if state == 0:
				eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
				libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
				if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
					#print "User added"
					libEDK.EE_DataAcquisitionEnable(userID,True)
					readytocollect = True

			if readytocollect==True:    
				libEDK.EE_DataUpdateHandle(0, hData)
				libEDK.EE_DataGetNumberOfSample(hData,nSamplesTaken)
				#print "Updated :",nSamplesTaken[0]
				if nSamplesTaken[0] != 0:
					nSam=nSamplesTaken[0]
					arr=(ctypes.c_double*nSamplesTaken[0])()
					ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))
					#libEDK.EE_DataGet(hData, 3,byref(arr), nSam)                         
					data = array('d')#zeros(nSamplesTaken[0],double)
					for sampleIdx in range(nSamplesTaken[0]): 
						for i in range(22): 
							libEDK.EE_DataGet(hData,targetChannelList[i],byref(arr), nSam)
							print >>f,arr[sampleIdx],",",                    
						print >>f,'\n'                
			time.sleep(0.2)
			ending=time.time()-starting #this is supposed to be out of infinite while loop
            
		#infinite while ends here
		f.close()	
		libEDK.EE_DataFree(hData)

		#---------------------------------------------------------------------------------------------------------------------------------------------------------------
		libEDK.EE_EngineDisconnect()
		libEDK.EE_EmoStateFree(eState)
		libEDK.EE_EmoEngineEventFree(eEvent)
		eeg_doc = sp.genfromtxt("EEG.txt", delimiter=" , ")
		e=eeg_doc[:,1:15]
		ea=np.mean(e, axis=0)
		namequery=User.objects.get(name=uname)
		query2=Data.objects.filter(name=uname)
		u=Data.objects.get(name=namequery,item=obname)
		
		ee=[u.e1,u.e2,u.e3,u.e4,u.e5,u.e6,u.e7,u.e8,u.e9,u.e10,u.e11,u.e12,u.e13,u.e14]
		eb=[float(x) for x in ee]
		c=np.concatenate((ea,eb))
		d=c.reshape((2,14))
		ea=np.mean(d,axis=0)
		[u.e1,u.e2,u.e3,u.e4,u.e5,u.e6,u.e7,u.e8,u.e9,u.e10,u.e11,u.e12,u.e13,u.e14]=ea
		u.save()

		return render(request, 'dash.html',{'name':uname,'items':query2})

def test(request):
	if 'uname' in request.GET and request.GET['uname']:
		uname=request.GET['uname']
		import random 
		import time
		import ctypes
		import sys
		import os
		from ctypes import *
		from numpy import *
		import numpy as np
		import scipy as sp
		import time
		from ctypes.util import find_library
		ED_COUNTER = 0
		ED_INTERPOLATED=1
		ED_RAW_CQ=2
		ED_AF3=3
		ED_F7=4
		ED_F3=5
		ED_FC5=6
		ED_T7=7
		ED_P7=8
		ED_O1=9
		ED_O2=10
		ED_P8=11
		ED_T8=12
		ED_FC6=13
		ED_F4=14
		ED_F8=15
		ED_AF4=16
		ED_GYROX=17
		ED_GYROY=18
		ED_TIMESTAMP=19
		ED_ES_TIMESTAMP=20
		ED_FUNC_ID=21
		ED_FUNC_VALUE=22
		ED_MARKER=23
		ED_SYNC_SIGNAL=24

		targetChannelList = [ED_COUNTER,ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]
		libEDK = cdll.LoadLibrary(".\\edk.dll")
		
		header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
		write = sys.stdout.write
		eEvent      = libEDK.EE_EmoEngineEventCreate()
		eState      = libEDK.EE_EmoStateCreate()
		userID            = c_uint(0)
		nSamples   = c_uint(0)
		nSam       = c_uint(0)
		nSamplesTaken  = pointer(nSamples)
		da = zeros(128,double)
		data     = pointer(c_double(0))
		user                    = pointer(userID)
		composerPort          = c_uint(1726)
		secs      = c_float(1)
		datarate    = c_uint(0)
		readytocollect    = False
		option      = c_int(0)
		state     = c_int(0)

		if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
			return HttpResponse("Emotiv Engine start up failed.")
           
		#print "Start receiving EEG Data! Press any key to stop logging...\n"
		f = file('EEG.txt', 'w')
		f = open('EEG.txt', 'w')
		#print >> f,header
		    
		hData = libEDK.EE_DataCreate()
		libEDK.EE_DataSetBufferSizeInSec(secs)

		ending=0
		starting = time.time()
		while (1):
			if ending>4:
				break
			state = libEDK.EE_EngineGetNextEvent(eEvent)
			if state == 0:
				eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
				libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
				if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
					#print "User added"
					libEDK.EE_DataAcquisitionEnable(userID,True)
					readytocollect = True

			if readytocollect==True:    
				libEDK.EE_DataUpdateHandle(0, hData)
				libEDK.EE_DataGetNumberOfSample(hData,nSamplesTaken)
				#print "Updated :",nSamplesTaken[0]
				if nSamplesTaken[0] != 0:
					nSam=nSamplesTaken[0]
					arr=(ctypes.c_double*nSamplesTaken[0])()
					ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))
					#libEDK.EE_DataGet(hData, 3,byref(arr), nSam)                         
					data = array('d')#zeros(nSamplesTaken[0],double)
					for sampleIdx in range(nSamplesTaken[0]): 
						for i in range(22): 
							libEDK.EE_DataGet(hData,targetChannelList[i],byref(arr), nSam)
							print >>f,arr[sampleIdx],",",                    
						print >>f,'\n'              
			time.sleep(0.2)
			ending=time.time()-starting #this is supposed to be out of infinite while loop
		f.close()
		#infinite while ends here
		libEDK.EE_DataFree(hData)

		#---------------------------------------------------------------------------------------------------------------------------------------------------------------
		libEDK.EE_EngineDisconnect()
		libEDK.EE_EmoStateFree(eState)
		libEDK.EE_EmoEngineEventFree(eEvent)
		eeg_doc = sp.genfromtxt("EEG.txt", delimiter=" , ")
		e=eeg_doc[:,1:15]
		ea=np.mean(e, axis=0)
		namequery=User.objects.get(name=uname)
		query=Data.objects.filter(name=uname)
		
		sli=[]
		bli=[]
		nli=[]
		
		for i in query:
			for j in range(1,15):
				exec("sli.append(i.e%d)" % j)
			bli.append(sli)
			nli.append(i.item)
			sli=[]		
		
		from sklearn.neighbors import KNeighborsClassifier

		neigh = KNeighborsClassifier(n_neighbors=1)
		neigh.fit(bli, nli)
		ans=neigh.predict([ea])

		return HttpResponse(ans)



