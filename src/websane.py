import string
import sys
import sane
import cgi
import urllib
from xml.dom.ext import PrettyPrint
from xml.dom import implementation
from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

basepath='/home/mikko/websane_temp/websane/demo'



class ReqHandler(BaseHTTPRequestHandler):

	
	
	def do_GET(self):
		if self.path == '/favicon.ico': #reroute annoying favicon requests so we don't have to send 404s
			self.path = '/style/images/tmp.ico'
	
		try:
			if self.path=='/snap':
				self.send_response(200)
				self.send_header('Content-type','image/png')
				self.end_headers()
				
				print 'SANE version:', sane.init()
				devs = sane.get_devices()
				print 'Available devices=', devs
				scanner=sane.open(devs[0][0])
				print scanner
				scanner.contrast=170 
				scanner.brightness=150 
				
				scanner.br_x=320
				scanner.br_y=240
				
				scanner.start() #Removing this will cause a segmentation fault!
				im=scanner.snap()
				self.wfile.write(im)
				
			if self.path.find('?')!=-1:	#If the path contains a ? then we should parse it and scan and stuff --> http://www.faqts.com/knowledge_base/view.phtml/aid/4373
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				pathlist, values = urlParse(self.path)
				
				self.wfile.write("<html><head/><body>"+str(values)+"</body></html>")
			
			elif self.path.endswith('.xhtml'):
				f=open(basepath+self.path)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				reader = Sax2.Reader()
				doc=reader.fromStream(f)
				PrettyPrint(doc,self.wfile)
				
				f.close()
			
			else:
				#This is for serving regular files from the hd
				print basepath+self.path
				f=open(basepath+self.path)
				self.send_response(200)
				
				if self.getContentType() == None:
					#Let's not serve unknown stuff
					self.send_header('Content-type','text/plain')
					self.end_headers()
					f.close()
					return
				else:
					self.send_header('Content-type',self.getContentType())
					
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
		except IOError:
			self.send_error(404, 'IOError')
			
	def do_POST(self):
		contentype=self.headers.getheader('content-type')
		if contentype != 'application/x-www-form-urlencoded':
			print 'Error: Uncexpected content-type specified in header: ',contentype
			return
		
		clen = self.headers.getheader('content-length')
		
		if clen:
			clen = string.atoi(clen)
		else:
			print 'Error: Header is missing content-length'
			return
		
		data = self.rfile.read(clen)
		self.path = '%s?%s' % (self.path, data)
		self.do_GET()
		
	def getContentType(self):
		if self.path.endswith('.png'):
			return 'image/png'
		elif self.path.endswith('.gif'):
			return 'image/gif'
		elif self.path.endswith('.jpg') | self.path.endswith('.jpeg'):
			return 'image/jpeg'
		elif self.path.endswith('.css'):
			return 'text/css'
		elif self.path.endswith('.js'):
			return 'text/plain'
		elif self.path.endswith('.html'):
			return 'text/html'
		elif self.path.endswith('.ico'):
			return 'image/x-icon'


	
	

def urlParse(url):
	""" return path as list and query string as dictionary
		strip / from path
		ignore empty values in query string
		for example:
		if url is: /xyz?a1=&a2=0%3A1
		then result is: (['xyz'], { 'a2' : '0:1' } )
		if url is: /a/b/c/
		then result is: (['a', 'b', 'c'], None )
		if url is: /?
		then result is: ([], {} )
	"""
	x = string.split(url, '?')
	pathlist = filter(None, string.split(x[0], '/'))
	d = {}
	if len(x) > 1:
		q = x[-1]                  # eval query string
		x = string.split(q, '&')
		for kv in x:
			y = string.split(kv, '=')
			k = y[0]
			try:
				v = urllib.unquote_plus(y[1])
				if v:               # ignore empty values
					d[k] = v
			except:
				pass
	return (pathlist, d)

	
def main():
	try:
	
		server=HTTPServer(('',5423), ReqHandler)
		
		print 'webserver started'
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Shutting down server'
		server.socket.close()
		
if __name__ == '__main__':
	main()	
