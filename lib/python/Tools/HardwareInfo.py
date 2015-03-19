import os
from Tools.Directories import SCOPE_SKIN, resolveFilename

hw_info = None

class HardwareInfo:
	device_name = _("unavailable")
	device_model = None
	device_version = ""
	device_revision = ""
	device_hdmi = True

	def __init__(self):
                global hw_info
		if hw_info is not None:
			return
		hw_info = self

		print "[HardwareInfo] Scanning hardware info"
		# Version
		# Disable on spark because there is only a /proc/stb/info/model
		#if os.path.exists("/proc/stb/info/version"):
			#self.device_version = open("/proc/stb/info/version").read().strip()

		# Revision
		try:
			self.device_revision = open("/proc/stb/info/board_revision").read().strip()
		except:
			pass

		# Name ... bit odd, but history prevails
		try:
			self.device_name = open("/proc/stb/info/model").read().strip()
		except:
			pass

		# Model
		# Disable on spark because there is only a /proc/stb/info/model
		#for line in open((resolveFilename(SCOPE_SKIN, 'hw_info/hw_info.cfg')), 'r'):
			#if not line.startswith('#') and not line.isspace():
				#l = line.strip().replace('\t', ' ')
				#if l.find(' ') != -1:
					#infoFname, prefix = l.split()
				#else:
					#infoFname = l
					#prefix = ""
				#if os.path.exists("/proc/stb/info/" + infoFname):
					#self.device_model = prefix + open("/proc/stb/info/" + infoFname).read().strip()
					#break

		if self.device_model is None:
			self.device_model = self.device_name

		# HDMI capbility
		# Disable on spark
		#self.device_hdmi = (	self.device_name == 'dm7020hd' or
					#self.device_name == 'dm800se' or
					#self.device_name == 'dm500hd' or
					#(self.device_name == 'dm8000' and self.device_version != None))

		print "Detected: " + self.get_device_string()


	def get_device_name(self):
		return hw_info.device_name

	def get_device_model(self):
		return hw_info.device_model

	def get_device_version(self):
		return hw_info.device_version

	def get_device_revision(self):
		return hw_info.device_revision

	def get_device_string(self):
		s = hw_info.device_model
		if hw_info.device_revision != "":
			s += " (" + hw_info.device_revision + "-" + hw_info.device_version + ")"
		elif hw_info.device_version != "":
			s += " (" + hw_info.device_version + ")"
		return s

	def has_hdmi(self):
		return hw_info.device_hdmi
