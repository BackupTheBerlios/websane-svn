import string
import sys
import cgi
from xml.dom.ext import PrettyPrint
from xml.dom import implementation
from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

basepath='/home/mikko/websane_temp/websane/demo'



class ReqHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print "Doing GET"
		try:
			if self.path.find('?')!=-1:	#If the path contains a ? then we should parse it and scan and stuff --> http://www.faqts.com/knowledge_base/view.phtml/aid/4373
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				self.wfile.write("<html><head/><body>Hello</body></html>")
			
			elif self.path.endswith('.xhtml'):
				f=open(basepath+self.path)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				reader = Sax2.Reader()
				doc=reader.fromStream(f)
				PrettyPrint(doc,self.wfile)
				
				f.close()
			elif self.path=='/favicon.ico':
				self.send_error(404, 'No favicon')
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
