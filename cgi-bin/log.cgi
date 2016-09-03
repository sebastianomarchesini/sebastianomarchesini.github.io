#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;
use XML::LibXML;
require "./checkLog.cgi";

sub logError {
	#carico l'html
	my $htmlPage = "../".$_[0].".html";
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
	
	#aggiungo il messaggio di errore
	my $form = $doc->findnodes('//fieldset[@id = "formadmin"]')->get_node(0);
	my $childString = '<span id="logError">Dati inseriti errati</span>';
	my $child = $parserxml->parse_string($childString); #elimino il tag che identifica la versione dell'xml perché non devo aggiungerlo
	$child = $child->removeChild($child->firstChild());
	$form->insertBefore($child, $form->firstChild);
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	my $css = $doc->findnodes('//link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../public_html/CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

#estraggo le parole del login
my $logString = CGI->new();
my $username = $logString->param('logUsername');
my $password = $logString->param('logPassword');
#my $page = $logString->param('pagina');
my $page = "home_andrea.html";
my $finalDoc;

#estraggo i dati dall'XML
my $filexml = "../XML/profili.xml";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->parse_file($filexml);
my $expectedUsername = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:username');
my $expectedPassword = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:password');

if($username eq $expectedUsername && $password eq $expectedPassword) {
	#creo la sessione
	my $session = new CGI::Session();
	$session->param("utente", "amministratore");
	my $cookie = new CGI;
	my $nome_utente = $cookie->param('utente');
	$finalDoc = &log($page);
} else {
	$finalDoc = &logError($page);
}

print "Content-type: text/html; charset=utf-8\n\n";
print "<phtml>";
print "<body>";
print $finalDoc;
print "</body>";
print "</html>";