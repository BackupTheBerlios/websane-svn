<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet 
		version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
		xmlns="http://www.w3.org/1999/xhtml">
	
	
	<xsl:template match="tasks">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<xsl:call-template name="createHTMLHead" />
			<body>
				<xsl:call-template name="createMenu" />
			
				<div class="leftbar">
					
					<xsl:call-template name="createHeader" />
									
					<div class="content">
						<xsl:apply-templates select="subproject" />
					</div>
					
					<xsl:call-template name="createFooter" />
				</div>
			</body>
		</html>
	
	</xsl:template>
	
	<xsl:template match="subproject">
		<h3><xsl:value-of select="subproject_name" /></h3>
		<p><xsl:value-of select="description" /></p>
		<div class="task">
			<xsl:apply-templates select="task" />
		</div>
	</xsl:template>
	
	<xsl:template match="task">
		<h4><xsl:value-of select="summary" /></h4>
		<p><xsl:value-of select="details" /></p>
	</xsl:template>
	
</xsl:stylesheet>