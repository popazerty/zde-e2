from Screens.Screen import Screen
from enigma import getDesktop, eSize, ePoint
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.ScrollLabel import ScrollLabel

def splitToInt(text, split):
    try:
        res = int(text.split(',')[split])
    except:
        res = None

    return res


class TextOut(Screen):
    global HD_Res
    try:
        sz_w = getDesktop(0).size().width()
    except:
        sz_w = 720

    if sz_w == 1280:
        HD_Res = True
    else:
        HD_Res = False
    if HD_Res:
        skin = '\n\t<screen name="TextOut" position="100,70" size="1080,600" title="TextOut...">\n\t\t<widget name="text" position="10,10" size="1070,580" font="Regular;20" />\n\t</screen>'
    else:
        skin = '\n\t<screen name="TextOut" position="50,60" size="620,480" title="TextOut...">\n\t\t<widget name="text" position="5,5" size="610,460" font="Regular;18" />\n\t</screen>'

    def __init__(self, session, text = '', title = '', size = None, position = None):
        Screen.__init__(self, session)
        self.text = text
        self.newtitle = title
        self.size = size
        self.position = position
        try:
            self.Desktop_width = getDesktop(0).size().width()
            self.Desktop_height = getDesktop(0).size().height()
        except:
            self.Desktop_width = 720
            self.Desktop_height = 576

        self['text'] = ScrollLabel(self.text)
        self['actions'] = ActionMap(['OkCancelActions', 'DirectionActions'], {'cancel': self.cancel,
         'ok': self.ok,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self['title'] = StaticText()
        self.onShown.append(self.updateSize)
        self.onShown.append(self.updateTitle)

    def updateSize(self):
        center = True
        if HD_Res:
            HDscale = 2
        else:
            HDscale = 1
        if splitToInt(self.position, 0) and splitToInt(self.position, 1):
            pos_x = splitToInt(self.position, 0)
            pos_y = splitToInt(self.position, 1)
            center = False
        if splitToInt(self.size, 0) and splitToInt(self.size, 1):
            width = splitToInt(self.size, 0)
            height = splitToInt(self.size, 1)
            self.instance.resize(eSize(width, height))
            self['text'].resize(eSize(width - 10 * HDscale, height - 20))
            if center:
                pos_x = (self.Desktop_width - width) / 2
                pos_y = (self.Desktop_height - height) / 2
                self.instance.move(ePoint(pos_x, pos_y))
            else:
                self.instance.move(ePoint(pos_x, pos_y))

    def updateTitle(self):
        self.setTitle(self.newtitle)
        self['title'].setText(self.newtitle)

    def ok(self):
        self.close()

    def cancel(self):
        self.close()
