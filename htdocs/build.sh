#!/bin/bash
cd ..
svn checkout svn://svn.berlios.de/websane/htdocs
xsltproc --xinclude htdocs/xslt/builder.xsl htdocs/xml/site.xml
ln -s htdocs/style `pwd`/style
ln -s htdocs/images `pwd`/images
