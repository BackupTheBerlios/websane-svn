#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005: Mikko Virkkilä
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
import cgi
import urllib
#from xml.dom.ext import PrettyPrint
#from xml.dom import implementation
#from xml.dom.ext.reader import Sax2
import ConfigParser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import scanhandler

#This is a constant and shouldn't be modified
mmperinch=25.4

#Undocumented but very important features.
#These are actually how to convert the websane representation of the 
#width of the image in to mm. Since I haven't implemented reading the
#bounds yet, these are here just for reference.
magicint=65536
pwidth=14149222/magicint #The 14149222 is the width of the page as reported by python sane. Not used.
pheight=19475988/magicint #pheight is the height of the page in mm. Not used.


config = ConfigParser.ConfigParser()
scanhandler = scanhandler.ScanHandler()

config.read("webserver.cfg")
extbase=config('general','externalbasepath')
basepath=config('general','webserverbase')
previewfile=config('general','previewfile')

class ReqHandler(BaseHTTPRequestHandler):

	#Handle a http request for a file
	def do_GET(self):
		if self.path == extbase+'/':
			self.path='/demo.html'
		try:	
			#If the path contains a ? then we should parse it and scan and stuff
			if self.path.find('?')!=-1:
				pathlist, values = self.urlParse(self.path)
				
				#Handle a refresh of the preview
				if values['action'] == 'snap':
					scanhandler.update_preview(previewfile)
					self.path=extbase+'/demo.html'
				#Handle a scan
				elif values['action'] == 'scan':
					self.sendHeaders('image/png')
									
					scanhandler.reset_settings()
					
					scanhandler.set_mode(values['imgtype'])
					
					if values['resolution'] == 'OTHER':
						scanhandler.set_resolution(string.atof(values['custom_resolution']))
					else:
						scanhandler.set_resolution(string.atof(values['resolution']))
					
					scanhandler.set_scan_bounds_from_preview(values['left'],values['top'],values['width_px'],values['height_px'])
					
					scanhandler.scan_and_save(self.wfile, values['filetype'])
					return
				#Error, print some debugging info
				else:
					self.sendHeaders('text/html')
					self.wfile.write("<html><head/><body>Error. No action value returned. ",str(values),"</body></html>")
					return

			#Snap a preview image and send it directly to the browser
			if self.path==extbase+'/snap':
				print "Taking snapshot"
				self.sendHeaders('image/png')
				scanhandler.update_preview(self.wfile)

			#Do a scan and return the image directly to the browser
			elif self.path==extbase+'/scan':
				self.sendHeaders('image/png')
				scanhandler.set_resolution(300.0)
				
				scanhandler.scan_and_save(self.wfile, 'PNG')
				
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
				self.sendHeaders('text/plain')
				scanhandler.write_info(self.wfile)
			
			#We replace chair.jpg with the preview file.
			elif self.path==extbase+'/chair.jpg':
				f=open(previewfile)
				self.sendHeaders('image/png')
				self.wfile.write(f.read())
				f.close()
			#If nothing special was aksed, just serve the file of the specified name
			else:
				print basepath+self.path
				f=open(basepath+self.path)
				
				if self.getContentType() == None:
					#Let's not serve unknown stuff
					self.sendHeaders('text/plain')
					f.close()
					return
					
				self.sendHeaders( self.getContentType())
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
	
	#Maps extensions to mime types
	def getContentType(self):
		extension = string.split(self.path,'.')[-1]
		try:
			return config.get('mimetypes', extension)
		except NoOptionError:
			return

	def sendHeaders(self, conttype):
		self.send_response(200)
		self.send_header('Content-type',conttype)
		self.end_headers()
		
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
	
		server=HTTPServer(('',string.atoi(config.get('general', 'port'))), ReqHandler)
		
		print 'Webserver started'
		server.serve_forever()
		print 'Serving until keyboard interrupt received (ctrl+c)'
	except KeyboardInterrupt:
		print 'Shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
