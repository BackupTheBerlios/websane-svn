import string
import sys
import sane
import ConfigParser



class ScanHandler:
	scanner=None
	scannerdev=None
	
	config = ConfigParser.ConfigParser()
	
	previewres=string.atof(config.get('general','previewres'))
	
	#This is a constant and shouldn't be modified
	mmperinch=25.4
	
	#Updates the preview file.
	def update_preview(self, previewfile):
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
	

	#Convenience method for getting the first scanner available
	def get_scanner(self):
		if (None == self.scanner) :
			t=time()
			print 'Initializing scanner ', sane.init(),
			print time()-t,'seconds'

			t=time()
			
			devs=sane.get_devices()
			print 'Fetching available devices took ',time()-t,'seconds'
			
			#We just use the first available device
			self.scannerdev=devs[string.atoi(config.get('general','devicenumber'))][0]
			
		t=time()	
		self.scanner=sane.open(self.scannerdev)
		print 'Opening the first available device took ', time()-t,'seconds'

		return self.scanner


	def write_info(self,towriteto):
			towriteto.write( '\n\nSANE version:\n'+ str(sane.init()))
			devs = sane.get_devices()
			towriteto.write( '\n\nAvailable devices:\n'+str(devs))
			scanner = sane.open(devs[string.atoi(config.get('general','devicenumber'))][0])
			towriteto.write( '\n\nParameters specified device:\n'+str(scanner.get_parameters()) )
			towriteto.write( '\n\nOptions:\n'+str(scanner.get_options()) )
	
			
	def __init__(self):
		config.read("scanner.cfg")