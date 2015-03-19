from Components.MenuList import MenuList
from Tools.Directories import SCOPE_SKIN_IMAGE, resolveFilename
from enigma import RT_HALIGN_LEFT, eListboxPythonMultiContent, gFont
from Tools.LoadPixmap import LoadPixmap

def OPEntryComponent(key, text):
	res = [ text ]
	if text[0] == "--":
		png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "OpenPanel/opug_separator.png"))
		if png is not None:
			res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 0, 12, 780, 25, png))
	else:
		res.append((eListboxPythonMultiContent.TYPE_TEXT, 45, 00, 780, 25, 0, RT_HALIGN_LEFT, text[0]))
	
		png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/buttons/key_" + key + ".png"))
		if png is not None:
			res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 5, 0, 35, 25, png))
	#print "OPEntryComponent.res: ",res
	return res

class OpenPanelList(MenuList):
	def __init__(self, list, selection = 0, enableWrapAround=False):
		MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", 20))
		self.l.setItemHeight(25)
		self.selection = selection

	def postWidgetCreate(self, instance):
		MenuList.postWidgetCreate(self, instance)
		self.moveToIndex(self.selection)
