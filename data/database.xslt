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
                <link rel="stylesheet" href="../CSS/vendita.css" type="text/css" media="screen" />
                <link rel="stylesheet" href="../CSS/print.css" type="text/css" media="print" />
            </head>
            <body>
                <div id="header">
                    <h1><span id="logo" xml:lang="en" class="nascosto">GGarden</span></h1>
                    <div id="contenitore-login">
                        <input id="button_admin" type="button" onclick="nascondi();" value="Accedi come amministratore"/>
                        <div id="login">
                            <form action="../cgi-bin/log.cgi" method="get">
                                <fieldset>
                                    <legend>Login amministratore</legend>
                                    <div class="modal hide fade in">
                                        <div class="control-group">
                                            <label for="inputUsername">Username:</label>
                                            <input type="text" name="inputUsername" id="inputUsername" value="Username" tabindex="-1"/>
                                        </div>
                                        <div class="control-group">
                                            <label for="inputPassword">Password :</label>
                                            <input type="password" name="inputPassword" id="inputPassword" value="Password" tabindex="-2" />
                                        </div>
                                        <input type="hidden" name="update" value="no"/>
                                        <button type="submit" id="accedi">Accedi</button>
                                    </div>
                                </fieldset>
                            </form>
                        </div>
                    </div>
                </div>
                <div id="breadcrumbs">
                    <form class="headersearch" action="../cgi-bin/search.cgi" method="get">
                        <fieldset>
                            <span id="rifnav" >Ti trovi in: <a href="home.html" xml:lang="en">Home</a> / <b>Vendita</b></span>
                            <label for="ricerca" class="nascosto">Cerca un prodotto o un servizio</label>
                            <input type="text" name="ricerca" id="ricerca" class="ricerca" accesskey="s" tabindex="1" />
                            <input type="submit" name="conferma" id="conferma" class="ricerca" value="Cerca" accesskey="c" tabindex="2"/>
                        </fieldset>
                    </form>
                </div>
                
                <div id="contenitore-menu">
                    <ul class="menu">
                        <li><a href="../public_html/home.html" id="home" class="nav" xml:lang="en">Home </a></li>
                        <li><a href="../public_html/realizzazioni.html" id="real" class="nav">Realizzazioni </a></li>
                        <li><a href="database.xml" id="vend" class="vnav">Vendita </a></li>
                        <li><a href="../public_html/contattaci.html" id="cont" class="nav">Contattaci</a></li>
                    </ul>
                </div>
                
                
                
                
                <div id="content">
                    
                    <div id="piante">
                        <xsl:call-template name="piante"/>
                    </div>
                    <div id="attrezzi">
                        <xsl:call-template name="attrezzi"/>
                    </div>
                </div>
                
                <div id="footer" class="footer">
                    <div class="footer-left">
                        <h3><span id="logo_mini">Ggarden</span></h3>
                        <p class="footer-menu">
                            <a href="home.html">Home</a>
                            
                            <a href="../data/database.xml">Vendita</a>
                            
                            <a href="contattaci.html">Contattaci</a>
                        </p>
                        
                        <p class="footer-nome-azienda">Ggarden &#169; 2016</p>
                    </div>
                    
                    <div class="footer-center">
                        <div>
                            <i class="fa fa-map-indirizzo"></i>
                            <p id="testo-footer"><span>Via Trieste , 63</span> Padova, Italy</p>
                        </div>
                        
                        <div>
                            <i class="fa fa-telefono"></i>
                            <p id="testo-footer">+1 555 123456</p>
                        </div>
                        
                        <div>
                            <i class="fa fa-mail"></i>
                            <p><a href="mailto:support@company.com">service@ggarden.com</a></p>
                        </div>
                    </div>
                    
                    <div class="footer-right">
                        <p class="footer-company-info">
                            <span id="testo-footer">Gg Garden a servizio</span>
                            <span id="testo-footer">L'erba del tuo vicino è sempre più verde. Sii come il tuo vicino,
                                chiama G Garden Group</span>
                        </p>
                    </div>
                </div>
                
                <script type="text/javascript" src="public_html/SCRIPT/script.js"></script>
                
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
                        <p class="img"><img src="public_html/img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
                    </xsl:if>
                    <h4>DESCRIZIONE GENERALE</h4>
                    <p class="desc"><xsl:value-of select="g:descrizione"/></p>
                    <xsl:if test="g:dettagli/g:dato">
                        <h4>DATI</h4>
                        <p class="dati"><ul>
                            <xsl:for-each select="g:dettagli/g:dato">
                                <li class="info"><span class="formato"><xsl:value-of select="g:nome"/><xsl:if test="g:nome!=''">: </xsl:if></span><span class="contenuto"><xsl:value-of select="g:contenuto"/></span></li>
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
                                        <xsl:if test="$num_prezzo=1"> € <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                        <xsl:if test="$num_prezzo&gt;1"> € <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                        </span>
                                </xsl:for-each>
                            </xsl:if>
                        </p>
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
                        <p class="img"><img src="public_html/img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
                    </xsl:if>
                    <h4>DESCRIZIONE</h4>
                    <p class="desc"><xsl:value-of select="g:descrizione"/></p>
                    <xsl:if test="g:dettagli/g:dato">
                        <h4>DATI</h4>
                        <p class="dati"><ul>
                            <xsl:for-each select="g:dettagli/g:dato">
                                <li class="info"><span class="formato"><xsl:value-of select="g:nome"/><xsl:if test="g:nome!=''">: </xsl:if></span><span class="contenuto"><xsl:value-of select="g:contenuto"/></span></li>
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
                                        <xsl:if test="$num_prezzo=1"> € <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                        <xsl:if test="$num_prezzo&gt;1"> € <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                        </span>
                                </xsl:for-each>
                            </xsl:if>
                        </p>
                    </fieldset>
                </form>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
