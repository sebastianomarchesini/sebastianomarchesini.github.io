#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use CGI::Session;
use XML::LibXSLT;
use CGI::Carp qw(fatalsToBrowser);
use Mail::Sendmail;

sub log {
	my $xmlPage = "../data/database.xslt";
	my $parserxml = XML::LibXML->new;
	my $doc = $parserxml->load_xml(location => $xmlPage);
	
	#modifico il form
	my @xslUpperHTML = $doc->findnodes("//xsl:template[\@match='/']")->get_node(1)->childNodes();
	my $HTML = $xslUpperHTML[1];
	my $xpc = XML::LibXML::XPathContext->new($HTML);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	my $node = $xpc->findnodes("//x:div[\@id='contenitore-login']/x:input")->get_node(1);
	$xpc->setContextNode($node);
	$node->setAttribute('value', 'Modifica dati amministratore');
	$node = $xpc->findnodes("../x:div/x:form")->get_node(1);
	$node->setAttribute('action', '../cgi-bin/log.cgi');
	$xpc->setContextNode($node);
	$node = $xpc->findnodes("x:fieldset/x:legend/text()")->get_node(1);
	$node->setData('Modifica dati amministratore');
	$xpc->setContextNode($node);
	$node = $xpc->findnodes("../../x:div/x:input")->get_node(1);
	$node->setAttribute('value', 'yes');
	$xpc->setContextNode($node);
	$node = $xpc->findnodes("../x:button/text()")->get_node(1);
	$node->setData("Modifica");

	#inserisco i pulsanti per la gestione del database
	$xpc->setContextNode($HTML);
	$node = $xpc->findnodes("//x:div[\@id = 'piante']")->get_node(1);
	my $string = "<div id='createButtons'>
						<a href='../cgi-bin/databaseManager.cgi?operation=create&amp;tipo=pianta' class='createButton'>Inserisci nuova pianta</a>
						<a href='../cgi-bin/databaseManager.cgi?operation=create&amp;tipo=attrezzo' class='createButton'>Inserisci nuovo attrezzo</a>
				  </div>";
	my $child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $node->parentNode()->insertBefore($child, $node);
	my @nodes = $doc->findnodes("//fieldset[\@class='riquadro_prezzi']");
	$string = '<div id=\'productButtons\'>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=update&amp;tipo=pianta&amp;id={$id}\' class=\'productButton\'>Modifica prodotto</a>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=delete&amp;id={$id}\' class=\'productButton\'>Elimina prodotto</a>
			   </div>';
	$child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $nodes[0]->insertAfter($child, $nodes[0]->lastChild());
	$string = '<div id=\'productButtons\'>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=update&amp;tipo=attrezzo&amp;id={$id}\' class=\'productButton\'>Modifica prodotto</a>
					<a href=\'../cgi-bin/databaseManager.cgi?operation=delete&amp;id={$id}\' class=\'productButton\'>Elimina prodotto</a>
			   </div>';
	$child = $parserxml->parse_string($string);
	$child = $child->removeChild($child->firstChild());
	$node = $nodes[1]->insertAfter($child, $nodes[1]->lastChild());
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	$xpc->setContextNode($HTML);
	my $css = $xpc->findnodes('//x:link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../public_html/CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

my $session = CGI::Session->load() or die CGI::Session->errstr;
my $doc="";
if(!$session->is_expired && !$session->is_empty) {
	$doc = &log();
} else {
	my $xmlPage = "../data/database.xslt";
	my $parserxml = XML::LibXML->new;
	$doc = $parserxml->load_xml(location => $xmlPage);
}

my $filexml = "../data/database.xml";
my $parserxslt = XML::LibXSLT->new;
my $stylesheet  = $parserxslt->parse_stylesheet($doc);
my $results     = $stylesheet->transform_file($filexml);
my $fileToPrint = $stylesheet->output_as_bytes($results);

print "Content-type: text/html; charset=utf-8\n\n";

	print "<phtml>";
	print "<body>";
	print $fileToPrint;
	print "</body>";
	print "</html>";
