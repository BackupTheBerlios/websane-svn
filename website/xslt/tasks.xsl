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
						<!--<h2>Tasks</h2>-->
						<p>
						The tasks within the subprojects are sorted according to priority,
						</p>
						<xsl:apply-templates select="subproject" />
					</div>
					
					<xsl:call-template name="createFooter" />
				</div>
			</body>
		</html>
	
	</xsl:template>
	
	<xsl:template match="subproject">
		<h3 class="subproject_title"><xsl:value-of select="subproject_name" /></h3>
		<p class="subproject_description"><xsl:value-of select="description" /></p>
		<div class="tasks">
			<xsl:apply-templates select="task" ><xsl:sort  select="priority" order="descending" /></xsl:apply-templates>
		</div>
	</xsl:template>
	
	<xsl:template match="task">
		<xsl:variable name="taskURL">
			http://developer.berlios.de/pm/task.php?func=detailtask&amp;project_task_id=<xsl:value-of select="@id" />&amp;group_id=<xsl:value-of select="../group_id" />&amp;group_project_id=<xsl:value-of select="../@id" />
		</xsl:variable>
		<xsl:varible name="statusname"><xsl:apply-templates select="status_id" mode="getStatusName" /></xsl:varible>
		<xsl:if test="$statusname = 'Open'" >
			<div>
				<xsl:attribute name="class">taskbox state_<xsl:value-of select="$statusname" /></xsl:attribute>
				<table class="task">
					<tr>
						<td class="task_title">
							<a href="{$taskURL}"><xsl:value-of select="summary" /></a>
						</td>
						<td>
							Assigned to: 
							<xsl:for-each select="assigned_to" > 
								<xsl:value-of select="@name" />
								<xsl:if test="position()!=last()">, </xsl:if><!-- Last name doesn't get a comment after it-->
							</xsl:for-each> 
						</td>
					</tr><tr>
						<td>Status: <span class="status"><xsl:apply-templates select="status_id" mode="getStatusName" /></span> (<xsl:value-of select="percent_complete" />% done)</td>
					</tr><tr>
						<td class="task_description" colspan="2">
							<xsl:value-of select="details" />
						</td>
					</tr>
				</table>
			</div>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="*" mode="getStatusName">
		<xsl:if test=". = '1'">Open</xsl:if>
		<xsl:if test=". = '2'">Closed</xsl:if>
	</xsl:template>
	
</xsl:stylesheet>
