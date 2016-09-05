#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;
use XML::LibXML;

sub update {
	my $doc = &log();
	my $form = $doc->findnodes('//div[@id="login"]/form/fieldset')->get_node(1);
	my $parserxml  = XML::LibXML->new;
	my $childString;
	if($username ne $expectedUsername && $password ne $expectedPassword) {
		my $childString = '<span id="updateOk">Modifica dei dati avvenuta con successo</span>';
		my $filexml = "../data/profili.xml";
		my $xml = $parserxml->parse_file($filexml);
		my $xnode = $xml->findnodes("//p:profilo[\@id = 'amministratore']/p:username")->get_node(1);
		$xnode = $xnode->removeChildNodes();
		$xnode->appendTextNode($username);
		$xnode = $xnode->findnodes("../p:password")->get_node(1);
		$xnode = $xnode->removeChildNodes();
		$node->appendTextNode($password);
	} else {
		my $childString = '<span id="updateError">Dati inseriti errati</span>';
	}
	my $child = $parserxml->parse_string($childString);
	$child = $child->removeChild($child->firstChild());
	$form->insertBefore($child, $form->firstChild);
	return $doc;
}

sub log {
	my $htmlPage = "../data/vendita.xslt";
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->parse_file($htmlPage);

	#modifico il form
	my $node = $doc->findnodes("//div[\@id = 'contenitore-login']/input")->get_node(1);
	$node->setAttribute('value', 'Modifica dati amministratore');
	$node = $node->findnodes("../div/form")->get_node(1);
	$node->setAttribute('action', '../cgi-bin/log.cgi');
	$node = $node->findnodes("fieldset/legend/text()")->get_node(1);
	$node->setData('Modifica dati amministratore');
	$node = $doc->findnodes("../div/input")->get_node(1);
	$node->setAttribute('value', 'yes');
	$node = $doc->findnodes("../button/text()")->get_node(1);
	$node->setData("Modifica");

	#inserisco i pulsanti per la gestione del database
	$node = $doc->findnodes("//div[\@id = 'piante']")->get_node(1);
	my $string = "<div id='createButtons'>
						<button type='submit' value='Inserisci nuova pianta'/>
						<button type='submit' value='Inserisci nuovo attrezzo'/>
				  </div>";
	my $child = $parserxml->parse_string($string);
	$node = $node->parentNode()->insertBefore($child, $node);
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	my $css = $doc->findnodes('//link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

sub logError {
	#carico l'html
	my $htmlPage = "../data/vendita.xslt";
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->parse_file($htmlPage);
	
	#aggiungo il messaggio di errore
	my $form = $doc->findnodes('//div[@id="login"]/form/fieldset')->get_node(1);
	my $childString = '<span id="logError">Dati inseriti errati</span>';
	my $child = $parserxml->parse_string($childString); #elimino il tag che identifica la versione dell'xml perché non devo aggiungerlo
	$child = $child->removeChild($child->firstChild());
	$form->insertBefore($child, $form->firstChild);
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	my $css = $doc->findnodes('//link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

#estraggo le parole del login
my $logString = CGI->new();
#my $username = $logString->param('inputUsername');
#my $password = $logString->param('inputPassword');
my $username = 'Admin';
my $password = 'password';
my $update = $logString->param('update');
my $finalDoc;

#estraggo i dati dall'XML
my $filexml = "../data/profili.xml";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->parse_file($filexml);
my $expectedUsername = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:username');
my $expectedPassword = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:password');

if($update eq "yes") {
	$finalDoc = &update;
} else {
	if($username eq $expectedUsername && $password eq $expectedPassword) {
		#creo la sessione
		my $session = new CGI::Session() or die CGI::Session->errstr;
		print $session->header(-charset=>'utf-8');
		$session->param('username', 'amministratore');
		$session->expire('+1h');
		$session->flush();
		$finalDoc = &log();
	} else {
		$finalDoc = &logError();
		print "Content-type: text/html; charset=utf-8\n\n";
	}
}
print "<phtml>";
print "<body>";
print $finalDoc;
print "</body>";
print "</html>";
