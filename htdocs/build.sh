#!/bin/bash

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
	ln -s htdocs/style `pwd`/style
fi
if [ ! -L "images" ] 
then
	ln -s htdocs/images `pwd`/images
fi
if [ ! -L "build.sh" ]
then
	rm build.sh
	ln htdocs/build.sh ./build.sh
fi

