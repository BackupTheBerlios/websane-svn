#!/bin/bash

if [ `pwd|sed 's/.*\///'` = 'htdocs' ] 
then 
	echo "Create a symlink in the parent directory and rund from there instead"
	exit
fi

if [ -d "htdocs" ]
then
	svn update htdocs
else 
	svn checkout svn://svn.berlios.de/websane/htdocs
	chmod a+x htdocs/build.sh
fi

xsltproc --xinclude htdocs/xslt/builder.xsl htdocs/xml/site.xml

if [ ! -L "style" ] 
then
	echo "Creating symlink for style"
	ln -s htdocs/style `pwd`/style
fi
if [ ! -L "images" ] 
then
	echo "Creating symlink for style"
	ln -s htdocs/images `pwd`/images
fi
if [ ! -L "build.sh" ]
then
	echo "Removing old build.sh"
	rm build.sh
	echo "Symlinkin to new build.sh"
	ln -s htdocs/build.sh ./build.sh
fi

