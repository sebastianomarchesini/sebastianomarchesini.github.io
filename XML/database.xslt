<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:g="http://www.ggarden.com"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
exclude-result-prefixes="g">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"
doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>
	<xsl:template match="/">
	<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
		<title>Vendita - GGarden</title>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
		<meta name="title" content="GGarden" />
		<meta name="description" content="Azienda specializzata nella vendita di piante e fiori e nel noleggio e vendita di attrezzi e macchine da giardinaggio" />
		<meta name="keywords" content="piante, fiori, giardinaggio, attrezzi" />
		<meta name="author" content="Andrea Grendene, Pietro Gabelli, Sebastiano Marchesini, Jacopo Guizzardi" />
		<meta name="language" content="italian it" />
  		<link rel="stylesheet" href="../public_html/CSS/vendita.css" type="text/css" media="screen" />
	</head>
	<body>
	<div id="header">
		<span id="logo"><h1>GGarden</h1></span>
	</div>
	<div id="barra">
		<form action="" method="get">
			<fieldset id="formricerca">
				<input type="search" name="ricerca" id="ricerca" placeholder="Cerca un prodotto o un servizio" accesskey="c" tabindex="1" />
				<button type="submit" name="conferma" id="conferma" accesskey="e" tabindex="2">C<span class="accesskey">e</span>rca</button>
			</fieldset>
		</form>
		<form action="" method="get">
			<fieldset id="formadmin">
				<button type="submit" name="log" id="log" accesskey="a" tabindex="3"><span class="accesskey">A</span>ccedi come amministratore</button>
			</fieldset>
		</form>
		</div>

		<div id="piante">
			<xsl:call-template name="piante"/>
		</div>
		<div id="attrezzi">
			<xsl:call-template name="attrezzi"/>
		</div>

		<footer class="footer">
			<div class="footer-left">
				<h3>Company<span>logo</span></h3>

				<p class="footer-nome-azienda">Nome Azienda &amp;copy; 2016</p>
			</div>

			<div class="footer-center">

				<div>
					<i class="fa fa-map-indirizzo"></i>
					<p><span>Via Trieste , 63</span> Padova, Italy</p>
				</div>

				<div>
					<i class="fa fa-telefono"></i>
					<p>+1 555 123456</p>
				</div>

				<div>
					<i class="fa fa-mail"></i>
					<p><a href="mailto:support@company.com">service@ggarden.com</a></p>
				</div>
			</div>

			<div class="footer-right">

				<p class="footer-company-info">
					<span>Gg Garden a servizio</span>
					Non so che scrivere in questo momento ma seconod me ci sta una piccola nostra firma come una frase di battaglia
				</p>

			</div>

		</footer>
	</body>
	</html>
	</xsl:template>


	<xsl:template name="piante">
		<p class="maintitle"><h2>PIANTE</h2></p>
		<xsl:for-each select="g:prodotti/g:pianta">
		<xsl:sort select="g:nome"/>
			<div class="prodotto">
			<form action="" method="post">
				<h3><xsl:value-of select="g:nome"/></h3>
				<p class="id"><xsl:value-of select="@id"/></p>
				<p class="nome_scientifico"><xsl:value-of select="g:nome_scientifico"/></p>
				<p class="tipo"><xsl:value-of select="g:tipo"/></p>
				<xsl:variable name="nome" select="g:nome"/>
				<xsl:variable name="id" select="@id"/>
				<xsl:variable name="formato" select="@formato"/>
				<xsl:if test="$formato!='no_image'">
					<p class="img"><img src="../img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
				</xsl:if>
				<h4>DESCRIZIONE GENERALE</h4>
				<p class="desc"><xsl:value-of select="g:descrizione"/></p>
				<xsl:if test="g:dettagli/g:dato">
				<h4>DATI</h4>
				<p class="dati"><ul>
					<xsl:for-each select="g:dettagli/g:dato">
						<li><span class="formato"><xsl:value-of select="g:nome"/><xsl:if test="g:nome!=''">: </xsl:if></span><span class="contenuto"><xsl:value-of select="g:contenuto"/></span></li>
					</xsl:for-each>
				</ul></p>
				</xsl:if>
				<h4>PIANTAGIONE</h4>
				<p class="desc"><xsl:value-of select="g:piantagione"/></p>
				<h4>CURA</h4>
				<p class="desc"><xsl:value-of select="g:cura"/></p>
				<h4>ALTRE INFORMAZIONI</h4>
				<p class="desc"><xsl:value-of select="g:altre_info"/></p>
				<fieldset class="riquadro_prezzi">
				<p class="prezzo">
					<xsl:if test="count(g:prezzo/g:pacchetto)&lt;=1">
						<span class="prezzo_singolo">€ <xsl:value-of select="g:prezzo/g:pacchetto/g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:prezzo/g:pacchetto/g:formato"/></span>
					</xsl:if>
					<xsl:if test="count(g:prezzo/g:pacchetto)&gt;1">
					<xsl:for-each select="g:prezzo/g:pacchetto">
						<span class="check"><xsl:variable name="num_prezzo" select="position()"/>
						<xsl:if test="$num_prezzo=1"><input type="radio" name="{$id}" id="{$id}{$num_prezzo}" checked="true">€ <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></input></xsl:if>
						<xsl:if test="$num_prezzo&gt;1"><input type="radio" name="{$id}" id="{$id}{$num_prezzo}">€ <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></input></xsl:if>
						<label for="{$num_prezzo}">€ <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></label></span>
					</xsl:for-each>
					</xsl:if>
				</p>
				<span class="submit"><input type="submit" class="subbutton" value="Aggiungi al carrello"/></span>
				</fieldset>
			</form>
			</div>
		</xsl:for-each>
	</xsl:template>
	<xsl:template name="attrezzi">
		<p id="titoloAttrezzi" class="maintitle"><h2>ATTREZZI E MACCHINARI</h2></p>
		<xsl:for-each select="g:prodotti/g:attrezzo">
		<xsl:sort select="g:nome"/>
			<div class="prodotto">
			<form action="" method="post">
				<h3><xsl:value-of select="g:nome"/></h3>	
				<p class="id"><xsl:value-of select="@id"/></p>
				<p class="tipo"><xsl:value-of select="g:tipo"/></p>
				<xsl:variable name="nome" select="g:nome"/>
				<xsl:variable name="id" select="@id"/>
				<xsl:variable name="formato" select="@formato"/>
				<xsl:if test="$formato!='no_image'">
					<p class="img"><img src="../img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
				</xsl:if>
				<h4>DESCRIZIONE</h4>
				<p class="desc"><xsl:value-of select="g:descrizione"/></p>
				<xsl:if test="g:dettagli/g:dato">
				<h4>DATI</h4>
				<p class="dati"><ul>
					<xsl:for-each select="g:dettagli/g:dato">
						<li><span class="formato"><xsl:value-of select="g:nome"/><xsl:if test="g:nome!=''">: </xsl:if></span><span class="contenuto"><xsl:value-of select="g:contenuto"/></span></li>
					</xsl:for-each>
				</ul></p>
				</xsl:if>
				<fieldset class="riquadro_prezzi">
				<p class="prezzo">
					<xsl:if test="count(g:prezzo/g:pacchetto)&lt;=1">
						<span class="prezzo_singolo">€ <xsl:value-of select="g:prezzo/g:pacchetto/g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:prezzo/g:pacchetto/g:formato"/></span>
					</xsl:if>
					<xsl:if test="count(g:prezzo/g:pacchetto)&gt;1">
					<xsl:for-each select="g:prezzo/g:pacchetto">
						<span class="check"><xsl:variable name="num_prezzo" select="position()"/>
						<xsl:if test="$num_prezzo=1"><input type="radio" name="{$id}" id="{$id}{$num_prezzo}" checked="true">€ <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></input></xsl:if>
						<xsl:if test="$num_prezzo&gt;1"><input type="radio" name="{$id}" id="{$id}{$num_prezzo}">€ <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></input></xsl:if>
						<label for="{$num_prezzo}">€ <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></label></span>
					</xsl:for-each>
					</xsl:if>
				</p>
				<span class="submit"><input type="submit" class="subbutton" value="Aggiungi al carrello"/></span>
				</fieldset>
			</form>
			</div>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
