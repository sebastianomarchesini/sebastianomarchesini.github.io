#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;

sub log {
	#carico l'html
	my $htmlPage = "../".$_[0];
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
	
	#modifico il form
	my $legend = $doc->findnodes('//div[@id = "login"]//legend/text()')->get_node(0);
	$legend->setData('Modifica dati amministratore');
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	my $css = $doc->findnodes('//link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../public_html/CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

my $doc = &log("public_html/home.html");
print $doc;

1;
