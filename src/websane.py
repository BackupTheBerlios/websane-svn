import string
import sys
import sane
import cgi
import urllib
from time import time
from time import sleep
from xml.dom.ext import PrettyPrint
from xml.dom import implementation
from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

basepath='../demo'



class ReqHandler(BaseHTTPRequestHandler):
	scanner=None

	
	def get_scanner(self):
		if (None == self.scanner) :
			t=time()
			print 'Initializing scanner ', sane.init(),
			print time()-t,'seconds'

			t=time()
			
			devs=sane.get_devices()
			print 'Fetching available devices took ',time()-t,'seconds'

			t=time()
			self.scanner=sane.open(devs[0][0])
			print 'Opening the first available device took ', time()-t,'seconds'

			return self.scanner
		else :
			return self.scanner



	def update_preview(self):
		scanner=self.get_scanner()

		scanner.quality_cal=False
		scanner.depth=4
		scanner.resolution=20.0
		scanner.preview=True
		
		self.scan_and_save('/tmp/preview.png', 'PNG')

	def scan_and_save(self, file, imgtype):
		scanner=self.get_scanner()

		t=time()				
		scanner.start()
		print 'Starting the scanner with the selected options took ',time()-t,'seconds'
		

		t=time()
		im=scanner.snap()
		print 'Scanning image took ',time()-t,'seconds'

		t=time()
		im.save(file, imgtype)
		print 'Converting and saving image took ',time()-t,'seconds\n'
	
	def do_GET(self):
		if self.path == '/favicon.ico': #reroute annoying favicon requests so we don't have to send 404s
			self.path = '/style/images/tmp.ico'
	
		try:	
			#If the path contains a ? then we should parse it and scan and stuff --> http://www.faqts.com/knowledge_base/view.phtml/aid/4373		
			if self.path.find('?')!=-1:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				pathlist, values = self.urlParse(self.path)
				if values['button'] == 'snap':
					self.update_preview()
					f=open(basepath+'demo.html')
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
				
					reader = Sax2.Reader()
					doc=reader.fromStream(f)
					PrettyPrint(doc,self.wfile)
				
					f.close()
					return
				else:
					self.wfile.write("<html><head/><body>"+str(values)+"</body></html>")
					return

			
			
			
			#Snap a preview image and send it directly to the browser
			if self.path=='/snap':
				self.send_response(200)
				self.send_header('Content-type','image/png')
				self.end_headers()

				scanner=self.get_scanner()

				scanner.preview=True
				scanner.quality_cal=False
				scanner.depth=4
				scanner.resolution=20.0

				self.scan_and_save(self.wfile, 'PNG')

			#Do a scan and return the image directly to the browser
			elif self.path=='/scan':
				self.send_response(200)
				self.send_header('Content-type','image/png')
				self.end_headers()
				
				scanner=self.get_scanner()
				
				scanner.resolution=300.0
				
				self.scan_and_save(self.wfile, 'PNG')
			
			#FIXME!
			elif self.path.endswith('.xhtml'):
				f=open(basepath+self.path)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				reader = Sax2.Reader()
				doc=reader.fromStream(f)
				PrettyPrint(doc,self.wfile)
				
				f.close()
			
			#Used for debugging. Displays info about scanner.
			elif self.path=='/info':
				self.send_response(200)
				self.send_header('Conent-type','text/plain')
				self.end_headers()
				self.wfile.write( '\n\nSANE version:\n'+ str(sane.init()))
				devs = sane.get_devices()
				self.wfile.write( '\n\nAvailable devices:\n'+str(devs))
				scanner = sane.open(devs[0][0])
				self.wfile.write( '\n\nParameters of first device:\n'+str(scanner.get_parameters()) )
				self.wfile.write( '\n\nOptions:\n'+str(scanner.get_options()) )
			
			#If nothing special was aksed, just serve the file of the specified name
			else:
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

	
	#Posting will actually translate the post request to a get request, and we'll
	#just handle everything at the get request.
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


	def urlParse(self, url):
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
