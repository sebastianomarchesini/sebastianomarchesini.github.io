#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use XML::LibXSLT;

sub printPage {
	my $doc = $_[0];
	my $filexslt = "../data/search.xslt";
	my $parserxml  = XML::LibXML->new;
	my $parserxslt = XML::LibXSLT->new;
	my $xslt = $parserxml->parse_file($filexslt) || die("Operazione di parsificazione fallita");
	my $stylesheet = $parserxslt->parse_stylesheet($xslt);
	my $results = $stylesheet->transform($doc);
	my $fileToPrint = $stylesheet->output_as_bytes($results);
	print "Content-type: text/html; charset=utf-8\n\n";
	print "<phtml>";
	print "<body>";
	print $fileToPrint;
	print "</body>";
	print "</html>";
}

sub createPlantItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	#carico il parser e ricavo l'id da usare
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $id = $doc->findnodes('(//@id)[last()]')->get_node(1)->textContent();
	$id = $id + 1;
	for(my $i=length($id); $i<8; $i++) {
		$id = '0'.$id;
	}
	
	#Creo l'oggetto da inserire nell'XML
	my @prices = @{$_[4]};
	my @formats = @{$_[5]};
	my @dataNames = @{$_[7]};
	my @dataContents = @{$_[8]};
	my $item = $parser->parse_string("<p:pianta id='$id' formato='$_[0]' $namespace>
		<p:nome>$_[1]</p:nome>
		<p:nome_scientifico>$_[2]</p:nome_scientifico>
		<p:tipo>$_[3]</p:tipo>
		<p:prezzo></p:prezzo>
		<p:descrizione>$_[6]</p:descrizione>
		<p:dettagli></p:dettagli>
		<p:piantagione>$_[9]</p:piantagione>
		<p:cura>$_[10]</p:cura>
		<p:altre_info>$_[11]</p:altre_info>
	</p:pianta>"); #il namespace mi serve per poter aggiungere direttamente i prefissi, altrimenti lo script non funziona
	my $child = $item->findnodes("//p:prezzo")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());;
		$child->appendChild($string);
	}
	$child = $item->findnodes("//p:dettagli")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$item = $item->removeChild($item->firstChild());
	$child = $doc->getDocumentElement();
	$child = $child->appendChild($item);
	$doc->toFile($filexml);
	&printPage($doc);
}

sub createToolItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	#carico il parser e ricavo l'id da usare
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $id = $doc->findnodes('(//@id)[last()]')->get_node(1)->textContent();
	$id = $id + 1;
	for(my $i=length($id); $i<8; $i++) {
		$id = '0'.$id;
	}
	
	#Creo l'oggetto da inserire nell'XML
	my @prices = @{$_[3]};
	my @formats = @{$_[4]};
	my @dataNames = @{$_[6]};
	my @dataContents = @{$_[7]};
	my $item = $parser->parse_string("<p:attrezzo id='$id' formato='$_[0]' $namespace>
		<p:nome>$_[1]</p:nome>
		<p:tipo>$_[2]</p:tipo>
		<p:prezzo></p:prezzo>
		<p:descrizione>$_[5]</p:descrizione>
		<p:dettagli></p:dettagli>
	</p:attrezzo>"); #il namespace mi serve per poter aggiungere direttamente i prefissi, altrimenti lo script non funziona
	my $child = $item->findnodes("//p:prezzo")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$child = $item->findnodes("//p:dettagli")->get_node(1);
	for (my $i=0; $i<scalar @prices; $i++) {
		my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
		$string = $string->removeChild($string->firstChild());
		$child->appendChild($string);
	}
	$item = $item->removeChild($item->firstChild());
	$child = $doc->getDocumentElement();
	$child = $child->appendChild($item);
	$doc->toFile($filexml);
	&printPage($doc);
}

sub updatePlantItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $item = $doc->findnodes("//p:pianta[\@id='$_[0]']")->get_node(1);
	if($_[1] ne "") { #imageformat
		$item->setAttribute('formato', "$_[1]");
	}
	if($_[2] ne "") { #name
		my $child = $item->findnodes("./p:nome")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[2]);
	}
	if($_[3] ne "") { #scientificName
		my $child = $item->findnodes("./p:nome_scientifico")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[3]);
	}
	if($_[4] ne "") { #type
		my $child = $item->findnodes("./p:tipo")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[4]);
	}
	if($_[5] ne "" && $_[6] ne "") { #prices e formats
		my $pricesNode = $item->findnodes("./p:prezzo")->get_node(1);
		$pricesNode->removeChildNodes();
		my @prices = @{$_[5]};
		my @formats = @{$_[6]};
		for(my $i=0; $i<scalar @prices; $i++) {
			my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
			$string = $string->removeChild($string->firstChild());
			$pricesNode->appendChild($string);
		}
	}
	if($_[7] ne "") { #description
		my $child = $item->findnodes("./p:descrizione")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[7]);
	}
	if($_[8] ne "" && $_[9] ne "") { #dataNames e dataContents
		my $detailsNode = $item->findnodes("./p:dettagli")->get_node(1);
		$detailsNode->removeChildNodes();
		my @dataNames = @{$_[8]};
		my @dataContents = @{$_[9]};
		for(my $i=0; $i<scalar @dataNames; $i++) {
			my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
			$string = $string->removeChild($string->firstChild());
			$detailsNode->appendChild($string);
		}
	}
	if($_[10] ne "") { #plantation
		my $child = $item->findnodes("./p:piantagione")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[10]);
	}
	if($_[11] ne "") { #care
		my $child = $item->findnodes("./p:cura")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[11]);
	}
	if($_[12] ne "") { #otherInfos
		my $child = $item->findnodes("./p:altre_info")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[12]);
	}
	$doc->toFile($filexml);
	&printPage($doc);
}

sub updateToolItem {
	my $filexml = '../data/database.xml';
	my $namespace = "xmlns:p='http://www.ggarden.com'";
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file($filexml);
	my $item = $doc->findnodes("//p:attrezzo[\@id='$_[0]']")->get_node(1);
	if($_[1] ne "") { #imageformat
		$item->setAttribute('formato', "$_[1]");
	}
	if($_[2] ne "") { #name
		my $child = $item->findnodes("./p:nome")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[2]);
	}
	if($_[3] ne "") { #type
		my $child = $item->findnodes("./p:tipo")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[3]);
	}
	if($_[4] ne "" && $_[5] ne "") { #prices e formats
		my $pricesNode = $item->findnodes("./p:prezzo")->get_node(1);
		$pricesNode->removeChildNodes();
		my @prices = @{$_[4]};
		my @formats = @{$_[5]};
		for(my $i=0; $i<scalar @prices; $i++) {
			my $string = $parser->parse_string("<p:pacchetto $namespace><p:valore>$prices[$i]</p:valore><p:formato>$formats[$i]</p:formato></p:pacchetto>");
			$string = $string->removeChild($string->firstChild());
			$pricesNode->appendChild($string);
		}
	}
	if($_[6] ne "") { #description
		$item->findnodes("./p:descrizione/text()")->get_node(1)->setData($_[6]);
		my $child = $item->findnodes("./p:descrizione")->get_node(1);
		$child->removeChildNodes();
		$child->appendTextNode($_[6]);
	}
	if($_[7] ne "" && $_[8] ne "") { #dataNames e dataContents
		my $detailsNode = $item->findnodes("./p:dettagli")->get_node(1);
		$detailsNode->removeChildNodes();
		my @dataNames = @{$_[7]};
		my @dataContents = @{$_[8]};
		for(my $i=0; $i<scalar @dataNames; $i++) {
			my $string = $parser->parse_string("<p:dato $namespace><p:nome>$dataNames[$i]</p:nome><p:contenuto>$dataContents[$i]</p:contenuto></p:dato>");
			$string = $string->removeChild($string->firstChild());
			$detailsNode->appendChild($string);
		}
	}
	$doc->toFile($filexml);
	&printPage($doc);
}


my $operation = 'create';
my $itemType = 'attrezzo';
my $imageFormat = 'png';
my $name = 'Attrezzo quasi inutile';
my $type = 'Quasi inutilità su quasi misura';
my @prices = ('Quasi 2,50');
my @formats = ('quasi al pezzo');
my $description = 'Attrezzo quasi inutile. Se trovi quasi uno scopo adatto sei quasi quasi pregato di comunicarcelo.';
my @dataNames = ('Quasi lunghezza manico', 'Materiale manico', 'Colore manico', 'Quasi lunghezza testa', 'Materiale testa', 'Colore testa');
my @dataContents = ('quasi 10 cm', 'faggio', ' quasi marrone', 'quasi 5 cm', 'acciaio', 'quasi grigio');
	
if($itemType eq "pianta") {
	my $scientificName = 'Quasi quasi';
	my $plantation = 'Le piante sono quasi finte, quindi non hanno quasi bisogno di cure; non provate a toglierle dal loro quasi vaso o altrimenti potrebbero quasi rompersi!';
	my $care = 'Dato che le piante sono quasi finte non è quasi necessaria alcun tipo di cura.';
	my $otherInfos = 'Quasi presto saranno quasi disponibili altri colori, quasi quasi chiedi pure in negozio per ulteriori quasi informazioni!';
	if($operation eq "create") {
		&createPlantItem($imageFormat, $name, $scientificName, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents, $plantation, $care, $otherInfos);
	} elsif($operation eq "update") {
		my $id = '00000011';
		&updatePlantItem($id, $imageFormat, $name, $scientificName, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents, $plantation, $care, $otherInfos);
	}
} elsif($itemType eq "attrezzo") { #inserisco la condizione anche nell'ultimo caso per evitare che un possibile errore, come una chiamata involontaria a questo script, possa compromettere il database
	if($operation eq "create") {
		&createToolItem($imageFormat, $name, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents);
	} elsif($operation eq "update") {
		my $id = '00000011';
		&updateToolItem($id, $imageFormat, $name, $type, \@prices, \@formats, $description, \@dataNames, \@dataContents);
	}
}
