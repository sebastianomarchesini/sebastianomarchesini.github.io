#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;
use XML::LibXML;
#use XML::Writer;
require "./checkLog.cgi";

sub logError {
	my $htmlPage = "../".$_[0];
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
	my $form = $doc->findnodes('//fieldset[@id = "formadmin"]')->get_node(0);
	my $childString = '<span id="logError">Dati inseriti errati</span>';
	my $child = $parserxml->load_xml(string => $childString);
	my $first = $form->childNodes()->get_node(2);
	#$form = $form->insertBefore($child, $first);
	#$form = $form->addChild($child);
	print $first->nodeName();
	return $form;
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