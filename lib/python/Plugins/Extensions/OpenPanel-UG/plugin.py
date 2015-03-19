# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from Components.PluginComponent import plugins
from OpenPanel import OpenPanel
from e2Plugins import e2Plugins

def main(session, **kwargs):
	session.open(OpenPanel)
	
def opug(session, **kwargs):
	session.open(OpenPanel,"/etc/openpanel_ug.xml")


def autostart(reason,**kwargs):
	if reason == 0:
		print "\n" + "-" * 60 + "\n[OpenPanel] generating /etc/plugin.xml\n" + "-" * 60 + "\n"
		xmlPlugins = e2Plugins()
		xmlPlugins.makePluginHelp()
	else:
	    pass

def Plugins(**kwargs):
 	return [PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = autostart), 
	PluginDescriptor(name="OpenPanel Image Menu", description="OpenPanel E2 is a XML Script Interpreter Menu Plugin", where = PluginDescriptor.WHERE_PLUGINMENU, icon=None, fnc=opug),
	PluginDescriptor(name="Zebradem Menü", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=opug)]
