# e2Fetcher by Emanuel CLI 2009
from twisted.web.client import downloadPage
from Screens.MessageBox import MessageBox

class fetchPage(object):
	
	def __init__(self, session, url=None, file=None):
		self.session = session
		self.download(url, file)

	def download(self, url, file):
		downloadPage(url, file).addCallback(self.downloadDone).addErrback(self.downloadError)
			
	def downloadError(self, raw):
		print "[e2Fetcher.fetchPage]: download Error", raw
		self.session.open(MessageBox, text = _("download Error!"), type = MessageBox.TYPE_ERROR)
			
	def downloadDone(self,raw):
		print "[e2Fetcher.fetchPage]: download done", raw
		self.session.open(MessageBox, text =_("download done!"), type = MessageBox.TYPE_INFO)
