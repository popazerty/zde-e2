# for localized messages
from . import _
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox 
from Components.Input import Input
from Components.Language import language
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigLocations, ConfigText, ConfigSelection, getConfigListEntry, ConfigInteger
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext
import os

def localeInit():
	lang = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
	os_environ["LANGUAGE"] = lang # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	gettext.bindtextdomain("ZDE2DownloadCenter", resolveFilename(SCOPE_PLUGINS, "Extensions/ZDE2DownloadCenter/locale"))

def _(txt):
	t = gettext.dgettext("ZDE2DownloadCenter", txt)
	if t == txt:
		print "[ZDE2DownloadCenter] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)


def main(session, **kwargs):
	from Screens.PluginBrowser import PluginBrowser
	if PluginBrowser:
		pb = PluginBrowser(session)
		if pb:
			pb.download()

def mainconf(menuid):
    if menuid != "setup":
        return [ ]
    return [(_("Zebradem Download-Center"), main, "zde2downloadcenter", None)]

def Plugins(**kwargs):
	return [PluginDescriptor(name = _("Zebradem Download-Center"), 
			description = _("Zebradem Plugin Download-Center"), 
			where = PluginDescriptor.WHERE_EXTENSIONSMENU, 
			fnc = main),
		PluginDescriptor(name = _("Zebradem Download-Center"),
                        description = _("Zebradem Plugin Download-Center"),
                        where = PluginDescriptor.WHERE_MENU,
                        fnc = mainconf)]

