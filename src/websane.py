import string
import sys
from xml.dom import ext
from xml.dom import implementation
from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class ReqHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		try:
			if self.path.endswith('.xhtml'):
				basepath='/home/koody/python'
				f=open(basepath+self.path)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				
				reader = Sax2.Reader()
				doc=reader.fromStream(f)
				import xml.dom.ext
				xml.dom.ext.PrettyPrint(doc,self.wfile)
				
				f.close()
			elif self.path=='/favicon.ico':
				self.send_error(404, 'No favicon')
			else:
				basepath='/home/koody/python'
				f=open(basepath+self.path)
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
		except IOError:
			self.send_error(404, 'IOError')
			
	def do_POST(self):
		return

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
