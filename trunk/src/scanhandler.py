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
import sane
import ConfigParser
from time import time


class ScanHandler:
	scanner=None
	scannerdev=None
	
	config = ConfigParser.ConfigParser()

	
	#This is a constant and shouldn't be modified
	mmperinch=25.4
	
	#Updates the preview file.
	def update_preview(self, previewfile):
		self.reset_settings()

		self.scanner.quality_cal=False
		self.scanner.depth=4
		self.scanner.resolution=self.previewres
		self.scanner.preview=True
		
		print 'Resolution',str(self.scanner.resolution)
		self.scan_and_save(previewfile, 'PNG')

	#Scans a file with the assigned settings and saves it.
	def scan_and_save(self, file, imgtype):
		scanner=self.scanner

		t=time()				
		scanner.start()
		print 'Starting the scanner with the selected options took ',time()-t,'seconds'
		

		t=time()
		im=scanner.snap()
		print 'Scanning image took ',time()-t,'seconds'

		t=time()
		im.save(file, imgtype)
		print 'Converting and saving image took ',time()-t,'seconds\n'
	

	def reset_settings(self):
		t=time()
		self.scanner=sane.open(self.scannerdev)
		print 'Opening the selected device took ', time()-t,'seconds'

	def write_info(self,towriteto):
		towriteto.write( '\n\nSANE version:\n'+ str(sane.init()))
		devs = sane.get_devices()
		towriteto.write( '\n\nAvailable devices:\n'+str(devs))
		scanner = sane.open(devs[string.atoi(self.config.get('general','devicenumber'))][0])
		towriteto.write( '\n\nParameters specified device:\n'+str(scanner.get_parameters()) )
		towriteto.write( '\n\nOptions:\n'+str(scanner.get_options()) )
	
	#Translate the pixel locations in the preview to realworld coordinates (in to mm)
	def set_scan_bounds_from_preview(self, x_px, y_px, width_px, height_px, previewres=None):
		if previewres == None:
			previewres=self.previewres
		self.scanner.tl_x=string.atof(x_px) * self.mmperinch / previewres 
		self.scanner.tl_y=string.atof(y_px) * self.mmperinch / previewres
		self.scanner.br_x=self.scanner.tl_x + string.atoi(width_px) * self.mmperinch / previewres
		self.scanner.br_y=self.scanner.tl_y + string.atoi(height_px) * self.mmperinch / previewres
	
	def set_resolution(self, resolution):
		self.scanner.resolution=string.atof(resolution)
	
	''' imagemode:
			BW - for black and white (lineart) scans
			GRAY - for grayscale scans
			COLOR - for color scans
			any other will use COLOR
	'''
	def set_mode(self, imagemode):
		if imagemode == None:
			self.scanner.mode='Color'
		elif imagemode == 'BW':
			self.scanner.mode='Lineart'
		elif imagemode == 'GRAY':
			self.scanner.mode='Gray'
		else:
			self.scanner.mode='Color'	
	
	def __init__(self):
		
		self.config.read("scanner.cfg")
		self.previewres=string.atof(self.config.get('general','previewres'))
		print "Reading config file done"

		t=time()
		print 'Initializing scanner ', sane.init(),
		print time()-t,'seconds'

		t=time()
		devs=sane.get_devices()
		print 'Fetching available devices took ',time()-t,'seconds'
			
		#We just use the first available device
		self.scannerdev=devs[string.atoi(self.config.get('general','devicenumber'))][0]
			
		self.reset_settings()



#	def __name__:
#		return
