<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:t="http://www.tei-c.org/ns/1.0"
  xmlns:eg="http://www.tei-c.org/ns/Examples"
  exclude-result-prefixes="t eg"
  version="1.0">
  <xsl:output method="html" indent="no"/>

  <xsl:param name="section"></xsl:param>

  <xsl:key name="names" match="*" use="name()"/>

  <xsl:template match="/">
    <xsl:variable name="els"><xsl:call-template name="elements"/></xsl:variable>
    <script type="text/javascript">
      var els = [<xsl:value-of select="substring($els,1, string-length($els)-1)"/>];
    </script>
    <div id="tei">
      <xsl:choose>
        <xsl:when test="$section = ''">
          <xsl:apply-templates select="node()|comment()"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates select="id($section)"/>
        </xsl:otherwise>
      </xsl:choose>
    </div>
    <xsl:if test="$section != '' and $section != 'front'">
      <div style="display:none">
        <xsl:apply-templates select="//t:front"/>
      </div>
    </xsl:if>
  </xsl:template>

  <xsl:template match="node()|@*|comment()">
    <xsl:copy><xsl:apply-templates select="node()|@*|comment()"/></xsl:copy>
  </xsl:template>

  <xsl:template match="t:*">
    <xsl:element name="tei-{translate(local-name(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')}" >
      <xsl:if test="namespace-uri(parent::*) != namespace-uri(.)"><xsl:attribute name="data-xmlns"><xsl:value-of select="namespace-uri(.)"/></xsl:attribute></xsl:if>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id"><xsl:value-of select="@xml:id"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="@xml:lang">
        <xsl:attribute name="lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="rendition">
        <xsl:attribute name="class"><xsl:value-of select="substring-after(@rendition, '#')"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="not(node())">
        <xsl:attribute name="data-empty">data-empty</xsl:attribute>
      </xsl:if>
      <xsl:attribute name="data-teiname"><xsl:value-of select="local-name(.)"/></xsl:attribute>
      <xsl:for-each select="@*">
        <xsl:choose>
          <xsl:when test="local-name(.) = 'target' and starts-with(., '#')">
            <xsl:variable name="target" select="id(substring-after(.,'#'))"/>
            <xsl:choose>
              <xsl:when test="$target/ancestor::t:front"><xsl:attribute
                name="target"><xsl:value-of select="$target/ancestor::t:front/@xml:id"/><xsl:value-of select="."/></xsl:attribute></xsl:when>
              <xsl:when test="$target/ancestor::t:div[@xml:id]"><xsl:attribute
                name="target"><xsl:value-of select="$target/ancestor::t:div[@xml:id]/@xml:id"/><xsl:value-of select="."/></xsl:attribute></xsl:when>
              <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>
            <xsl:copy-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
      <xsl:apply-templates select="node()|comment()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="eg:egXML">
    <teieg-egxml>
      <xsl:if test="namespace-uri(parent::*) != namespace-uri(.)"><xsl:attribute name="data-xmlns"><xsl:value-of select="namespace-uri(.)"/></xsl:attribute></xsl:if>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id"><xsl:value-of select="@xml:id"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="@xml:lang">
        <xsl:attribute name="lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="rendition">
        <xsl:attribute name="class"><xsl:value-of select="substring-after(@rendition, '#')"/></xsl:attribute>
      </xsl:if>
      <xsl:attribute name="data-teiname"><xsl:value-of select="local-name(.)"/></xsl:attribute>
      <xsl:for-each select="@*">
        <xsl:copy-of select="."/>
      </xsl:for-each>
      <xsl:apply-templates select="node()|comment()"/>
    </teieg-egxml>
  </xsl:template>

  <xsl:template match="eg:*">
    <xsl:element name="teieg-{translate(local-name(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')}" >
      <xsl:if test="namespace-uri(parent::*) != namespace-uri(.)"><xsl:attribute name="data-xmlns"><xsl:value-of select="namespace-uri(.)"/></xsl:attribute></xsl:if>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id"><xsl:value-of select="@xml:id"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="@xml:lang">
        <xsl:attribute name="lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
      </xsl:if>
      <xsl:if test="rendition">
        <xsl:attribute name="class"><xsl:value-of select="substring-after(@rendition, '#')"/></xsl:attribute>
      </xsl:if>
      <xsl:attribute name="data-teiname"><xsl:value-of select="local-name(.)"/></xsl:attribute>
      <xsl:for-each select="@*">
        <xsl:copy-of select="."/>
      </xsl:for-each>
      <xsl:apply-templates select="node()|comment()"/>
    </xsl:element>
  </xsl:template>

  <xsl:template name="elements">
    <xsl:for-each select="//t:*">
      <xsl:if test="generate-id() = generate-id(key('names',name(.))[1])">
        <xsl:text>"</xsl:text><xsl:value-of select="local-name(.)"/><xsl:text>",</xsl:text>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>


</xsl:stylesheet>
