#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;

my $htmlPage = "../home_andrea.html";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
my $form = $doc->findnodes('//fieldset[@id = "formadmin"]')->get_node(0);
my $childString = '<span id="logError">Dati inseriti errati</span>';
my $child = $parserxml->parse_string($childString); #elimino il tag che identifica la versione dell'xml perché non devo aggiungerlo
$child = $child->removeChild($child->firstChild());
$form->insertBefore($child, $form->firstChild);

print $form;