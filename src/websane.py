import string
import sys
from xml.dom.ext import PrettyPrint
from xml.dom import implementation
from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class ReqHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			
			if self.path.endswith('.xhtml'):
				basepath='/home/mikko/websane_temp/websane/demo'
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
				basepath='/home/mikko/websane_temp/websane/demo'
				print basepath+self.path
				f=open(basepath+self.path)
				self.send_response(200)
				
				if getContentType( self.path ) == None:
					#Let's not serve unknown stuff
					self.send_header('Content-type','text/plain')
					self.end_headers()
					f.close()
					return
				else:
					self.send_header('Content-type',getContentType( self.path ))
					
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
		except IOError:
			self.send_error(404, 'IOError')
			
	def do_POST(self):
		return




def getContentType(urlpath):
	if urlpath.endswith('.png'):
		return 'image/png'
	elif urlpath.endswith('.gif'):
		return 'image/gif'
	elif urlpath.endswith('.jpg') | urlpath.endswith('.jpeg'):
		return 'image/jpeg'
	elif urlpath.endswith('.css'):
		return 'text/css'
	elif urlpath.endswith('.js'):
		return 'text/plain'
	elif urlpath.endswith('.html'):
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
