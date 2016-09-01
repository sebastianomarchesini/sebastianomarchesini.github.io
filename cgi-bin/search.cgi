#!/usr/bin/perl
use XML::LibXSLT;
use XML::LibXML;
use strict;
use warnings;
use HTML::TreeBuilder;

#Carico tutti i dati che mi servono, come i percorsi dei file xml
my $filexml = "../XML/database.xml";
my $filexslt = "../XML/search.xslt";

#estraggo le parole della ricerca
my $word = "";
my $searchString=$ENV{'QUERY_STRING'};
my @pairs = split(/&/, $searchString);
foreach my $pair(@pairs) {
	(my $name, my $value) = split(/=/, $pair);
	$value =~ tr/+/ /;        
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/g;   
	$name =~ tr/+/ /;        
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/g;         
	if($name eq "ricerca") {
		$word = $value;
	}
}

#creo i parser che mi servono ed effettuo tutte le operazioni necessarie ad ottenere il file html
my $parserxml  = XML::LibXML->new;
my $parserxslt = XML::LibXSLT->new;

my $doc         = $parserxml->parse_file($filexml);
my $xslt         = $parserxml->parse_file($filexslt) || die("Operazione di parsificazione fallita");

#viene creata una copia dell'XML del database da cui elimino i nodi figli, in modo da poterli reinserire secondo l'ordine della ricerca
my $output = $parserxml->parse_file($filexml);
my $root = $output->getDocumentElement;
my @childnodes = $root->childNodes();
my @childsTemp = @childnodes;
foreach my $child (@childnodes) {
	$root->removeChild($child);
}

#estraggo e copio i nodi cercati in "output", per la ricerca prima trovo i nodi che contengono tutta l'espressione e poi quelli che contengono le parole singole, partendo da destra fino a sinistra. Vengono fatte più estrazioni in base alla priorità dei termini, ovviamente il nome e il tipo sono più importanti di tutto il resto
my $xpath="//p:attrezzo[contains(translate(p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]";
my @node = $doc->findnodes("$xpath");
$xpath="//p:attrezzo[contains(translate(p:tipo, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:tipo, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]";
push(@node, $doc->findnodes("$xpath"));
$xpath="//p:attrezzo[contains(translate(p:id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:attrezzo[contains(translate(p:descrizione, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:attrezzo[contains(translate(p:dettagli/p:dato/p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:attrezzo[contains(translate(p:dettagli/p:dato/p:contenuto, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:nome_scientifico, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:descrizione, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:dettagli/p:dato/p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:dettagli/p:nome/p:contenuto, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:piantagione, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:cura, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:altre_info, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$word', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]";
push(@node, $doc->findnodes("$xpath"));
foreach my $i (@node) {
	my $pointer=0;
	while ($pointer <= $#childsTemp) {
		if($i->findvalue('./@id') eq $childsTemp[$pointer]->findvalue('./@id')) {
			$root->addChild($childsTemp[$pointer]);
			splice(@childsTemp, $pointer, 1);
		}
		else {
			$pointer++;
		}
	}
}

my @words = split(/ /, $word);
foreach my $w (@words) {
	my $xpath="//p:attrezzo[contains(translate(p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]";
	@node = $doc->findnodes($xpath);
	$xpath="//p:attrezzo[contains(translate(p:tipo, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:tipo, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]";
	push(@node, $doc->findnodes("$xpath"));
	$xpath="//p:attrezzo[contains(translate(p:id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:attrezzo[contains(translate(p:descrizione, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:attrezzo[contains(translate(p:dettagli/p:dato/p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:attrezzo[contains(translate(p:dettagli/p:dato/p:contenuto, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:nome_scientifico, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:descrizione, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:dettagli/p:dato/p:nome, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:dettagli/p:nome/p:contenuto, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:piantagione, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:cura, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))] | //p:pianta[contains(translate(p:altre_info, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('$w', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]";
	push(@node, $doc->findnodes("$xpath"));
	foreach my $i (@node) {
		my $pointer=0;
		while ($pointer <= $#childsTemp) {
			if($i->findvalue('./@id') eq $childsTemp[$pointer]->findvalue('./@id')) {
				$root->addChild($childsTemp[$pointer]);
				splice(@childsTemp, $pointer, 1);
			}
			else {
				$pointer++;
			}
		}
	}
}

#applico il foglio di stile al file modificato
my $stylesheet  = $parserxslt->parse_stylesheet($xslt);
my $results     = $stylesheet->transform($output);

my $fileToPrint = $stylesheet->output_as_bytes($results);

print "Content-type: text/html; charset=utf-8\n\n";
print "<phtml>";
print "<body>";
print $fileToPrint;
print "</body>";
print "</html>";
