# -*- coding: utf-8 -*-
# OpenPanel Plugin by Emanuel CLI 2009

from Screens.Screen import Screen
from Screens.InfoBar import InfoBar
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.TextOutUG import TextOut, splitToInt
from Components.ActionMap import NumberActionMap
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.PluginComponent import plugins
from Components.GUIComponent import GUIComponent
from Plugins.Plugin import PluginDescriptor
from Tools.Import import my_import
from OpenPanelList import OPEntryComponent, OpenPanelList
from xml.dom import minidom, Node
from enigma import getDesktop, eSize, ePoint
import os, sys, string, urllib

start_daemon = '/usr/sbin/op-start-daemon'

class OpenPanel(Screen):
	global HD_Res

	try:
		sz_w = getDesktop(0).size().width()
		if sz_w == 1280:
			HD_Res = True
		else:
			HD_Res = False
	except:
		HD_Res = False

	if HD_Res:
		skin = """
		<screen name="OpenPanel" position="240,100" size="800,540" title="OpenPanel">
			<widget name="list" position="10,10" size="780,480" scrollbarMode="showOnDemand" zPosition="0"/>
			<widget name="help" backgroundColor="#220a0a0a" zPosition="2" position="10,500" size="780,38" font="Regular;16" halign="left"/>
		</screen>"""
		
	else:
		skin = """
		<screen name="OpenPanel" position="160,70" size="400,460" title="OpenPanel">
			<widget name="list" position="5,5" size="390,400" scrollbarMode="showOnDemand" zPosition="0"/>
			<widget name="help" backgroundColor="#220a0a0a" zPosition="2" position="5,420" size="390,38" font="Regular;16" halign="left"/>
		</screen>"""
		
	def __init__(self, session, path=None, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.menu = args
		self.e = None
		xml_file = '/etc/openpanel.xml'
		if path:
			xml_file = path
		try:
			self.Desktop_width = getDesktop(0).size().width()
			self.Desktop_height = getDesktop(0).size().height()
		except:
			self.Desktop_width = 720
			self.Desktop_height = 576
#		print "[OpenPanel] Desktop size: ", self.Desktop_width, self.Desktop_height
		self.zapHistory = [None]
		self.pluginlist = plugins.getPlugins([PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_EVENTINFO])
		try:
			parser = minidom.parse(xml_file)
			self.currentNode = parser.documentElement
			self.getList(self.makeEntrys(self.currentNode)[0], self.makeEntrys(self.currentNode)[1])
			self["list"] = OpenPanelList(list = self.list, selection = 0)
			self["summary_list"] = StaticText()
			self.updateSummary()
			
		except Exception, e:
			self.e = e
			self["list"] = OpenPanelList(None)

				
		self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.go,
			"back": self.cancel,
			"1": self.keyNumberGlobal,
			"2": self.keyNumberGlobal,
			"3": self.keyNumberGlobal,
			"4": self.keyNumberGlobal,
			"5": self.keyNumberGlobal,
			"6": self.keyNumberGlobal,
			"7": self.keyNumberGlobal,
			"8": self.keyNumberGlobal,
			"9": self.keyNumberGlobal,
			"0": self.keyNumberGlobal,
			"red": self.keyRed,
			"green": self.keyGreen,
			"yellow": self.keyYellow,
			"blue": self.keyBlue,
			"up": self.up,
			"down": self.down,
			"left": self.keyLeft,
			"right": self.keyRight
		}, -1)
		self["title"] = StaticText()
		self["help"] = Label("")
		self.onExecBegin.append(self.error)
		self.onShown.append(self.updateSize)
		self.onShown.append(self.updateText)

	def error(self):
		if self.e:
			self.session.open(MessageBox,("XML " + _("Error") + ": %s" % self.e),  MessageBox.TYPE_ERROR)
			print "[OpenPanel] ERROR: ",self.e
			self.close(None)
		else:
			print "[OpenPanel]: GUI OK :-)"

	def getSettings(self,node):
		attr = node.attributes
		size = position = None
		if HD_Res:
			for attrName in attr.keys():
				if attrName == 'HD_size':
                	        	attrNode = attr.get(attrName)
					size = attrNode.nodeValue.encode('utf-8')
				
				elif attrName == 'HD_position':
                	        	attrNode = attr.get(attrName)
					position = attrNode.nodeValue.encode('utf-8')
		else:
			for attrName in attr.keys():
				if attrName == 'size':
                	        	attrNode = attr.get(attrName)
					size = attrNode.nodeValue.encode('utf-8')
				
				elif attrName == 'position':
                	        	attrNode = attr.get(attrName)
					position = attrNode.nodeValue.encode('utf-8')
					
		return size, position
				
	def updateSize(self):
		node = self.currentNode
		size = self.getSettings(node)[0]
		position = self.getSettings(node)[1]
		center = True
		if HD_Res:
			HDscale = 2;
		else:
			HDscale = 1;
			
		if splitToInt(position, 0) and splitToInt(position, 1):
			pos_x = splitToInt(position, 0)
			pos_y = splitToInt(position, 1)
			center = False
#			print "[OpenPanel] center = False"

		if splitToInt(size, 0) and splitToInt(size, 1):
			width = splitToInt(size, 0)
			height = splitToInt(size, 1)
				
			self.instance.resize(eSize(width, height))
			self["list"].resize(eSize((width-(10*HDscale)), (height-60)))
			self["help"].resize(eSize((width-(10*HDscale)), 38))
			self["help"].move(ePoint((5*HDscale), (height-40)))
			
			if center:
				pos_x = (self.Desktop_width - width) / 2
				pos_y = (self.Desktop_height - height) / 2
#				print "[OpenPanel] move center position"
				self.instance.move(ePoint(pos_x, pos_y))
			else:
#				print "[OpenPanel] move to position: ",pos_x, pos_y
				self.instance.move(ePoint(pos_x, pos_y))
				
	def updateText(self):
		self.updateHelp()
		attr = self.currentNode.attributes
		for attrName in attr.keys():
			if attrName == 'name':
                	        attrNode = attr.get(attrName)
				self.newtitle = attrNode.nodeValue.encode('utf-8')
				self.setTitle(self.newtitle)
				
	def updateHelp(self):
		help = self["list"].l.getCurrentSelection()[0][3]
		self["help"].setText(help)
			
	def execPlugin(self, name):
		no_plugin = True
		for plugin in self.pluginlist:
			if plugin.name == _(name):
				if InfoBar and InfoBar.instance:
					try:
						no_plugin = False
						InfoBar.runPlugin(InfoBar.instance, plugin)
						break
					except Exception, e:
						self.session.open(MessageBox,("Plugin " + _("Error") + ": %s" % (e)),  MessageBox.TYPE_ERROR)
						print "[OpenPanel] plugin entry: code error exec: %s\n" % (e)
						break
		if no_plugin:
			self.session.open(MessageBox,(_("Error") + " Plugin" + ": %s not found!" % _(name)),  MessageBox.TYPE_ERROR)
			print "[OpenPanel] plugin %s not found!" % _(name)

	def opTextOut(self, text = "", title = "", node = None):
		self.session.open(TextOut, text = text, title = title, size = self.getSettings(node)[0], position = self.getSettings(node)[1])
		print "[OpenPanel] open TextOut: ",title, text,self.getSettings(node)[0],self.getSettings(node)[1]
		
	def closePluginBrowser(self):
		sh = "sleep 1; ebox exit"
#		print "[OpenPanel] closing extern Pluginbrowser: %s '%s &'\n" % (start_daemon,sh)
		command = "%s '%s &'" % (start_daemon,sh)
		os.system(command)
		
	def noDoubleKeys(self,keylist, key):
		if keylist == []:
			return key
		if key == "":
			return ""
		for x in keylist:
	        	if x == key:
				return ""
		else:
			return key
		
	def makeEntrys(self, currentNode):
		keylist = []
		mnulist = []
		entry_idx = -1
		
		for node in currentNode.childNodes:
        		if node.nodeType == Node.ELEMENT_NODE:
        		# Write out the element name.
				if node.nodeName == 'entry' or node.nodeName == 'shell' or node.nodeName == 'usersh' or node.nodeName == 'plugin' or node.nodeName == 'xmlfile' or node.nodeName == 'text':
					name = shortcut = exit = help = target = code = options = text = ""
					attrs = node.attributes
					for attrName in attrs.keys():
						if attrName == 'name':
                					attrNode = attrs.get(attrName)
							name = attrNode.nodeValue.encode('utf-8')
							
						elif attrName == 'shortcut':
							attrNode = attrs.get(attrName)
							shortcut =  attrNode.nodeValue.encode('utf-8')
							
						elif attrName == 'exit':
							attrNode  =  attrs.get(attrName)
							exit = attrNode.nodeValue.encode('utf-8')
							
						elif attrName == 'help':
							attrNode  =  attrs.get(attrName)
							help = attrNode.nodeValue.encode('utf-8')
							
						elif attrName == 'target':
							attrNode  =  attrs.get(attrName)
							target = attrNode.nodeValue.encode('utf-8')
							
						elif attrName == 'text':
							attrNode  =  attrs.get(attrName)
							text = attrNode.nodeValue.encode('utf-8')
							
						elif attrName == 'options':
							attrNode  =  attrs.get(attrName)
							options = attrNode.nodeValue.encode('utf-8')
						
				if node.nodeName == 'entry':
					entry_idx +=1
					mnulist.append((name, "entry", node, help, entry_idx))
					keylist.append((self.noDoubleKeys(keylist, shortcut))) 
					
				elif node.nodeName == 'usersh':
					entry_idx +=1
					mnulist.append((name, "usersh", target, help, exit, options))
					keylist.append((self.noDoubleKeys(keylist, shortcut)))
					
				elif node.nodeName == 'shell':
					entry_idx +=1
					for node2 in node.getElementsByTagName("sh"):
        					for node3 in node2.childNodes:
							if node3.nodeType == Node.CDATA_SECTION_NODE or node3.nodeType == Node.TEXT_NODE:
								sh = node3.wholeText.encode('utf-8')
								
					mnulist.append((name, "shell", sh, help, exit))
					keylist.append((self.noDoubleKeys(keylist, shortcut)))
				
				elif node.nodeName == 'separator':
					entry_idx +=1
					mnulist.append(("--", "--"))
					keylist.append((""))
					
				elif node.nodeName == 'text':
					entry_idx +=1
					for node2 in node.getElementsByTagName('code'):
						for node3 in node2.childNodes:
							if node3.nodeType == Node.CDATA_SECTION_NODE or node3.nodeType == Node.TEXT_NODE:
								code = node3.wholeText.encode('utf-8')
								
					mnulist.append((name, "text", target, help, exit, code, text, node))
					keylist.append((self.noDoubleKeys(keylist, shortcut)))
					
				elif node.nodeName == 'plugin':
					entry_idx +=1
					code
					for node2 in node.getElementsByTagName('code'):
						for node3 in node2.childNodes:
							if node3.nodeType == Node.CDATA_SECTION_NODE:
								code = node3.wholeText.encode('utf-8')
								
					mnulist.append((name, "plugin", target, help, exit, code))
					keylist.append((self.noDoubleKeys(keylist, shortcut)))
							
				elif node.nodeName == 'xmlfile':
					entry_idx +=1
					for node2 in node.getElementsByTagName('code'):
						for node3 in node2.childNodes:
							if node3.nodeType == Node.CDATA_SECTION_NODE or node3.nodeType == Node.TEXT_NODE:
								code = node3.wholeText.encode('utf-8')
								
					mnulist.append((name, "xmlfile", target, help, node, code, entry_idx))
					keylist.append((self.noDoubleKeys(keylist, shortcut)))
#		print "[OpenPanel] MENU/KEY LISTS: ",mnulist,keylist
		return mnulist,keylist
		
	def getList(self,list,keys):
		self.list = []
		self.summarylist = []
		if keys is None:
			self.__keys = [""] * 14 + (len(list) - 10) * [""]
		else:
			self.__keys = keys + (len(list) - len(keys)) * [""]
			
		self.keymap = {}
		pos = 0
		for x in list:
			strpos = str(self.__keys[pos])
			self.list.append(OPEntryComponent(key = strpos, text = x))
			if self.__keys[pos] != "":
				self.keymap[self.__keys[pos]] = list[pos]
			self.summarylist.append((self.__keys[pos],x[0]))
			pos += 1
				
	def keyLeft(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.pageUp)
				self.updateSummary(self["list"].l.getCurrentSelectionIndex())
				if self["list"].l.getCurrentSelection()[0][0] != '--' or (self["list"].l.getCurrentSelectionIndex() == 0 and self["list"].l.getCurrentSelection()[0][0] != '--'):
					self.updateHelp()
					break
	
	def keyRight(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.pageDown)
				self.updateSummary(self["list"].l.getCurrentSelectionIndex())
				if self["list"].l.getCurrentSelection()[0][0] != '--' or (self["list"].l.getCurrentSelectionIndex() == len(self["list"].list) - 1 and self["list"].l.getCurrentSelection()[0][0] != '--'):
					self.updateHelp()
					break
	
	def up(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.moveUp)
				self.updateSummary(self["list"].l.getCurrentSelectionIndex())
				if self["list"].l.getCurrentSelection()[0][0] != '--' or (self["list"].l.getCurrentSelectionIndex() == 0 and self["list"].l.getCurrentSelection()[0][0] != '--'):
					self.updateHelp()
					break
				
	def down(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.moveDown)
				self.updateSummary(self["list"].l.getCurrentSelectionIndex())
				if self["list"].l.getCurrentSelection()[0][0] != '--' or (self["list"].l.getCurrentSelectionIndex() == len(self["list"].list) - 1 and self["list"].l.getCurrentSelection()[0][0] != '--'):
					self.updateHelp()
						
					break
				
	# runs a number shortcut
	def keyNumberGlobal(self, number):
		self.goKey(str(number))

	# runs the current selected entry
	def go(self):
		cursel = self["list"].l.getCurrentSelection()
		if cursel:
			self.goEntry(cursel[0])
		else:
			self.cancel()

	# runs a specific entry
	def goEntry(self, entry):
#		print self["list"].l.getCurrentSelectionIndex() #[0][1]
		if entry[1] == "entry":
			self.currentNode = entry[2]
			self.zapHistory.append(entry[4])
			self.getList(self.makeEntrys(self.currentNode)[0], self.makeEntrys(self.currentNode)[1])
			self["list"].l.setList(self.list)
			self["list"].instance.moveSelectionTo(0)
			self["summary_list"] = StaticText()
			self.updateSummary()
			self.updateSize()
			self.updateText()
			
		elif entry[1] == "plugin":
			if entry[5] <> "" and entry[5] <> "\n" and entry[5] <> None:
				try:
					exec(entry[5])
				except Exception, e:
					self.session.open(MessageBox,("Code " + _("Error") + ": %s" % e),  MessageBox.TYPE_ERROR)
#					print "[OpenPanel] plugin entry: code error exec: %s\n" % (e)
					
			if entry[2] <> "":
#				print "[OpenPanel] start plugin", entry[2]
				self.execPlugin(entry[2])
			if entry[4] == "no":
				pass
			else:
				self.close(None)
			
		elif entry[1] == "shell":
			command = "%s '%s &'" % (start_daemon,entry[2])
			try:
				debug = os.popen(command)
				print "[OpenPanel] shell entry exec: begin\n"
				for line in debug:
					print line
					
				print "[OpenPanel] shell entry exec: end\n"
			except Exception, e:
				self.session.open(MessageBox,("Shell " + _("Error") + ": %s" % e),  MessageBox.TYPE_ERROR)
#				print "[OpenPanel] shell entry: code error exec: %s\n" % (e)
				
			if entry[4] == "no":
				pass
			else:
				self.close(None)
			
		elif entry[1] == "usersh":
			if os.path.isfile(entry[2]):
				if entry[5] <> None:
					com = entry[2] + " " + entry[5]
				else:
					com = entry[2]
					
				self.session.open(Console, _("Executing User shell"), [com])
				if entry[4] == "no":
					pass
				else:
#					self.closePluginBrowser()
					self.close(None)
			else:
				self.session.open(MessageBox,(_("file %s\n not found") % entry[2]), MessageBox.TYPE_ERROR)
		
		elif entry[1] == "xmlfile":
#			print "[OpenPanel] xml entry:", entry
			tmp_xml = None
			if entry[2][:1] == "/":
				tmp_xml = entry[2]
				
			elif entry[2][:7] == "file://":
				tmp_xml = entry[2][7:]
					
			elif entry[2][:4] == "http" or entry[2][:3] == "ftp":
				try:
#					print "[OpenPanel] urllib.urlopen(entry[2]) ", entry[2]
					f = urllib.urlopen(entry[2])
					userxml = f.read()
					tmp_xml = "/tmp/.openpanel.xml"
#					print "[OpenPanel] file = open "
					file = open(tmp_xml, "w")
					file.write(userxml)
					file.close()
#					print "[OpenPanel] download done ", entry[2]
					
				except Exception, e:
					tmp_xml = None
					self.session.open(MessageBox,("XML Download " + _("Error") + ": %s" % e),  MessageBox.TYPE_ERROR)
#					print "[OpenPanel] error while loading ", entry[2], e
				except:
					tmp_xml = None
			else:
				self.session.open(MessageBox,("Syntax " + _("Error") + ": %s" % entry[2]),  MessageBox.TYPE_ERROR)
				print "[OpenPanel] XML path syntax error!\n"
			
			if tmp_xml <> None:
				if entry[5] <> "" and entry[5] <> "\n" and entry[5] <> None:
					try:
						exec(entry[5])
					except Exception, e:
						self.session.open(MessageBox,("Code " + _("Error") + ": %s" % e),  MessageBox.TYPE_ERROR)
						print "[OpenPanel] xml entry: code error exec: %s\n" % (e)
				try:
					if os.path.isfile(tmp_xml) == False:
						raise StandardError

					parser = minidom.parse(tmp_xml)
					tmpChildNode = parser.documentElement
					self.currentNode.replaceChild(tmpChildNode, entry[4])
					self.getList(self.makeEntrys(self.currentNode)[0], self.makeEntrys(self.currentNode)[1])
					self["list"].l.setList(self.list)
					self["summary_list"] = StaticText()
					self.updateSummary()
					if os.path.isfile("/tmp/.openpanel.xml"):
						os.remove("/tmp/.openpanel.xml")
						
					self["list"].instance.moveSelectionTo(entry[6])
					self.go()
			
				except Exception, e:
					self.session.open(MessageBox,("XML " + _("Error") + ": %s" % e),  MessageBox.TYPE_ERROR)
					print "[OpenPanel] xml entry: code error exec: %s\n" % (e)
					
		elif entry[1] == "text":
			if entry[5] <> "" and entry[5] <> "\n" and entry[5] <> None:
				try:
					exec(entry[5])
				except Exception, e:
					self.session.open(MessageBox,("Code " + _("Error") + ": %s" % e),  MessageBox.TYPE_ERROR)
#					print "[OpenPanel] text entry: code error exec: %s\n" % (e)
					
			if entry[6] <> "" and entry[6] <> None:
				self.opTextOut(text = entry[6], title = entry[0], node=entry[7])
			
			elif entry[2] <> "" and entry[2] <> None:
				file = open(entry[2],'r')
				text = file.read()
				file.close()
				self.opTextOut(text = text, title = entry[0], node=entry[7])
				
			if entry[4] == "no":
				pass
			else:
				self.close(None)
		else:
			print "[OpenPanel] error: No tag entrys found, exit"
			self.close(None)

	# lookups a key in the keymap, then runs it
	def goKey(self, key):
		if self.keymap.has_key(key):
			entry = self.keymap[key]
			self.goEntry(entry)

	# runs a color shortcut
	def keyRed(self):
		self.goKey("red")

	def keyGreen(self):
		self.goKey("green")

	def keyYellow(self):
		self.goKey("yellow")

	def keyBlue(self):
		self.goKey("blue")

	def updateSummary(self, curpos=0):
		pos = 0
		summarytext = ""
		for entry in self.summarylist:
#			print "[OpenPanel].updateSummary: entry: ",entry
			if pos > curpos-2 and pos < curpos+5:
				if pos == curpos:
					summarytext += ">"
				else:
					summarytext += entry[0]
				summarytext += ' ' + entry[1] + '\n'
			pos += 1
		self["summary_list"].setText(summarytext)

	def cancel(self):
		backZap = self.zapHistory.pop(len(self.zapHistory) - 1)
		if backZap > -1:
			self.currentNode = self.currentNode.parentNode
			self.getList(self.makeEntrys(self.currentNode)[0], self.makeEntrys(self.currentNode)[1])
			self["list"].l.setList(self.list)
			self["list"].instance.moveSelectionTo(backZap)
			self["summary_list"] = StaticText()
			self.updateSummary()
			self.updateSize()
			self.updateText()
		else:
			print "[OpenPanel] - exit"
			self.close(None)
