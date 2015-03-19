from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.Console import Console
from Components.Button import Button
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigList
from Components.config import config, configfile, ConfigSubsection, ConfigEnableDisable, \
     getConfigListEntry, ConfigInteger, ConfigSelection, ConfigYesNo 
from Components.ConfigList import ConfigListScreen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import iPlayableService, eServiceCenter, eEnv
from os import path, system
from Plugins.Plugin import PluginDescriptor
from Components.ServiceEventTracker import ServiceEventTracker
from Components.ServiceList import ServiceList
from Screens.InfoBar import InfoBar
from Screens import Standby

class Channelnumber:

	def __init__(self, session):
		self.session = session
		self.onClose = [ ]
		
		self.__event_tracker = ServiceEventTracker(screen=self,eventmap=
			{
				iPlayableService.evUpdatedInfo: self.__eventInfoChanged,
				iPlayableService.evUpdatedEventInfo: self.__eventInfoChanged
			})
		
		config.misc.standbyCounter.addNotifier(self.enterStandby, initial_call = False)

	def __eventInfoChanged(self):
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		if info is None:
			chnr = "---"
		else:
			chnr = self.getchannelnr()
		info = None
		service = None

	def leaveStandby(self):
		print "ZDE2_Notify: leave Standby"
		self.__eventInfoChanged()

	def enterStandby(self,configElement):
		print "ZDE2_Notify: enter Standby"
		Standby.inStandby.onClose.append(self.leaveStandby)

	def getchannelnr(self):
		if InfoBar.instance is None:
			chnr = "---"
			return chnr
		MYCHANSEL = InfoBar.instance.servicelist
		markersOffset = 0
		myRoot = MYCHANSEL.getRoot()
		mySrv = MYCHANSEL.servicelist.getCurrent()
		chx = MYCHANSEL.servicelist.l.lookupService(mySrv)
		if not MYCHANSEL.inBouquet():
			pass
		else:
			serviceHandler = eServiceCenter.getInstance()
			mySSS = serviceHandler.list(myRoot)
			SRVList = mySSS and mySSS.getContent("SN", True)
			for i in range(len(SRVList)):
				if chx == i:
					break
				testlinet = SRVList[i]
				testline = testlinet[0].split(":")
				if testline[1] == "64":
					markersOffset = markersOffset + 1
		chx = (chx - markersOffset) + 1
		rx = MYCHANSEL.getBouquetNumOffset(myRoot)
		chnr = str(chx + rx)
		return chnr

ChannelnumberInstance = None
	
class ZDE2_Notify:
	def __init__(self, session):
		print "ZDE2_Notify initializing"
		self.session = session
		self.service = None
		self.onClose = [ ]

		self.Console = Console()

		cmd = "/etc/rcS.d/S21zdsetskin"
		if path.exists(cmd):
			newskin = "ZD-PLi-Black-HD"                                   
			root = eEnv.resolve("${datadir}/enigma2/")
			skinfile = newskin+"/skin.xml"                                  
			if path.exists(root+skinfile):                                      
				config.skin.primary_skin.value = skinfile                 
				config.skin.primary_skin.save()     
			res = system(cmd)
		
		global ChannelnumberInstance
		if ChannelnumberInstance is None:
			ChannelnumberInstance = Channelnumber(session) 

	def shutdown(self):
		self.abort()

	def abort(self):
		print "ZDE2_Notify aborting"

zdNotify = None
gReason = -1
mySession = None

def controlzdNotify():
	global zdNotify
	global gReason
	global mySession
	
	if gReason == 0 and mySession != None and zdNotify == None:
		print "Starting ZDE2_Notify"
		zdNotify = ZDE2_Notify(mySession)
	elif gReason == 1 and zdNotify != None:
		print "Stopping ZDE2_Notify"
		zdNotify = None

def sessionstart(reason, **kwargs):
	print "AutoStarting ZDE2_Notify"
	global zdNotify
	global gReason
	global mySession

	if kwargs.has_key("session"):
		mySession = kwargs["session"]
	else:
		gReason = reason
	controlzdNotify()

def wakeupstart():
	return

def Plugins(**kwargs):
 	return [ PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART, PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart, wakeupfnc = wakeupstart) ]
