<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
		version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
		xmlns="http://www.w3.org/1999/xhtml">
		
	<xsl:template match="*" priority="-1" mode="copy">
		<xsl:element name="{name()}">
		<xsl:copy-of select="@*"/>
		<xsl:apply-templates mode="copy"/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="text()" mode="copy">
		<xsl:value-of select="normalize-space(.)"/>
	</xsl:template>
		
</xsl:stylesheet>