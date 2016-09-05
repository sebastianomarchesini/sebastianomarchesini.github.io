#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;

sub log {
	#carico l'html
	my $htmlPage = "../public_html/".$_[0].".html";
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
	
	#modifico il form
	my $legend = $doc->findnodes("//div[\@id = 'login']/form/fieldset/legend/text()")->get_node(1);
	$legend->setData('Modifica dati amministratore');
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	my $css = $doc->findnodes('//link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

my $doc = &log("home");
print "Content-type: text/html; charset=utf-8\n\n";

	print "<phtml>";
	print "<body>";
	print $doc;
	print "</body>";
	print "</html>";
