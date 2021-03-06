#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005: Mikko Virkkil�
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import string
import sys
import sane
import cgi
import urllib
from time import time
from time import sleep
#from xml.dom.ext import PrettyPrint
#from xml.dom import implementation
#from xml.dom.ext.reader import Sax2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

#Not completely implemented. YOU SHOULD PROBABLY CHANGE THIS TO READ extbase=''
extbase='/'

#Path for where the static content is
basepath='../demo'
#Preview resolution
previewres=30.0
#This is a constant and shouldn't be modified
inchinmm=25.4

#The preview file is stored here
previewfile='/tmp/preview.png'

#Undocumented but very important features.
#These are actually how to convert the websane representation of the 
#width of the image in to mm. Since I haven't implemented reading the
#bounds yet, these are here just for reference.
magicint=65536
pwidth=14149222/magicint #The 14149222 is the width of the page as reported by python sane. Not used.
pheight=19475988/magicint #pheight is the height of the page in mm. Not used.

class ReqHandler(BaseHTTPRequestHandler):
	scanner=None

	#Convenience method for getting the first scanner available
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


	#Updates the preview file.
	def update_preview(self):
		scanner=self.get_scanner()

		scanner.quality_cal=False
		scanner.depth=4
		scanner.resolution=previewres
		scanner.preview=True
		
		self.scan_and_save(previewfile, 'PNG')

	#Scans a file with the assigned settings and saves it.
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
	
	#Handle a http request for a file
	def do_GET(self):
		if self.path == '/favicon.ico': #reroute annoying favicon requests so we don't have to send 404s
			self.path = '/style/images/tmp.ico'
	
		try:	
			#If the path contains a ? then we should parse it and scan and stuff --> http://www.faqts.com/knowledge_base/view.phtml/aid/4373		
			if self.path.find('?')!=-1:
				pathlist, values = self.urlParse(self.path)
				
				#Handle a refresh of the preview
				if values['button'] == 'snap':
					self.update_preview()
					self.path=extbase+'/demo.html'
				#Handle a scan
				elif values['button'] == 'scan':
					self.send_response(200)
					self.send_header('Content-type','image/png')
					self.end_headers()
					
					scanner=self.get_scanner()
					
					
					if values['imgtype'] == 'BW':
						scanner.mode='Lineart'
					elif values['imgtype'] == 'GRAY':
						scanner.mode='Gray'
					else:
						scanner.mode='Color'
					
					if values['resolution'] == 'OTHER':
						scanner.resolution=string.atof(values['custom_resolution'])
					else:
						scanner.resolution=string.atof(values['resolution'])
					
					#Translate the pixel locations in to realworld coordinates (in to mm)
					scanner.tl_x=string.atof(values['left']) * inchinmm / previewres 
					scanner.tl_y=string.atof(values['top']) * inchinmm / previewres
					scanner.br_x=scanner.tl_x + string.atoi(values['width']) * inchinmm / previewres 
					scanner.br_y=scanner.tl_y + string.atoi(values['height']) * inchinmm / previewres
					
					self.scan_and_save(self.wfile, values['filetype'])
					return
				#Error, print some debugging info
				else:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					self.wfile.write("<html><head/><body>Error. Form has no button value. ",str(values),"</body></html>")
					return

			#Snap a preview image and send it directly to the browser
			if self.path==extbase+'/snap':
				self.send_response(200)
				self.send_header('Content-type','image/png')
				self.end_headers()

				scanner=self.get_scanner()

				scanner.preview=True
				scanner.quality_cal=False
				scanner.depth=4
				scanner.resolution=previewres

				self.scan_and_save(self.wfile, 'PNG')

			#Do a scan and return the image directly to the browser
			elif self.path==extbase+'/scan':
				self.send_response(200)
				self.send_header('Content-type','image/png')
				self.end_headers()
				
				scanner=self.get_scanner()
				
				scanner.resolution=300.0
				
				self.scan_and_save(self.wfile, 'PNG')
				
			#FIXME!
#			elif self.path.endswith('.xhtml'):
#				f=open(basepath+self.path)
#				self.send_response(200)
#				self.send_header('Content-type','text/html')
#				self.end_headers()
#				
#				reader = Sax2.Reader()
#				doc=reader.fromStream(f)
#				PrettyPrint(doc,self.wfile)
#				
#				f.close()
#			
			#Used for debugging. Displays info about scanner.
			elif self.path==extbase+'/info':
				self.send_response(200)
				self.send_header('Conent-type','text/plain')
				self.end_headers()
				self.wfile.write( '\n\nSANE version:\n'+ str(sane.init()))
				devs = sane.get_devices()
				self.wfile.write( '\n\nAvailable devices:\n'+str(devs))
				scanner = sane.open(devs[0][0])
				self.wfile.write( '\n\nParameters of first device:\n'+str(scanner.get_parameters()) )
				self.wfile.write( '\n\nOptions:\n'+str(scanner.get_options()) )
			
			#We replace chair.jpg with the preview file.
			elif self.path==extbase+'/chair.jpg':
				f=open(previewfile)
				self.send_response(200)
				self.send_header('Content-type','image/png')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
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
		#If we cant open the file (=can't find the file) we send a 404
		except IOError:
			self.send_error(404, 'IOError')

	
	#This handles a "post" from the browser by translating the post request to a get 
	#request, which will be handled in the do_GET method.
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
	
	#This really should be in a config file. It just maps extensions to mime types
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

	#This method is not written by me and as such is not licensed under the GPL
	#Refer to the original code for the copyright holder and license.
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
		
		print 'Webserver started'
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()	
