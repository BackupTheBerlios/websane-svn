import string
import sys
from xml.dom.ext import PrettyPrint
from xml.dom import implementation
from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

basepath='/home/mikko/websane_temp/websane/demo'



class ReqHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			
			if self.path.endswith('.xhtml'):
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
		print "sinulle on postia!"
		return

		
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
