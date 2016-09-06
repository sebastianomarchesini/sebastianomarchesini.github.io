#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;
use XML::LibXML;
use XML::LibXSLT;

sub update {
	my $username=$_[0];
	my $password=$_[1];
	my $expectedUsername=$_[2];
	my $expectedPassword=$_[3];
	my $doc = &log();
	my $xpc = XML::LibXML::XPathContext->new($doc);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	my $form = $xpc->findnodes('//x:div[@id="login"]/x:form/x:fieldset')->get_node(1);
	my $parserxml  = XML::LibXML->new;
	my $childString;
	if($username ne $expectedUsername || $password ne $expectedPassword) {
		$childString = '<span id="updateOk">Modifica dei dati avvenuta con successo</span>';
		my $filexml = "../data/profili.xml";
		my $xml = $parserxml->parse_file($filexml);
		my $xnode = $xml->findnodes("//p:profilo[\@tipo = 'amministratore']/p:username")->get_node(1);
		$xnode->removeChildNodes();
		$xnode->appendTextNode($username);
		$xnode = $xnode->findnodes("../p:password")->get_node(1);
		$xnode->removeChildNodes();
		$xnode->appendTextNode($password);
		$xml->toFile($filexml);
	} else {
		$childString = '<span id="updateError">Dati inseriti errati</span>';
	}
	my $child = $parserxml->parse_string($childString);
	$child = $child->removeChild($child->firstChild());
	$form->insertBefore($child, $form->firstChild);
	return $doc;
}

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

sub logError {
	#carico l'html
	my $htmlPage = "../data/database.xslt";
	my $parserxml  = XML::LibXML->new;
	my $doc = $parserxml->parse_file($htmlPage);
	my $xpc = XML::LibXML::XPathContext->new($doc);
	$xpc->registerNs('x', 'http://www.w3.org/1999/xhtml');
	
	#aggiungo il messaggio di errore
	my $form = $xpc->findnodes('//x:div[@id="login"]/x:form/x:fieldset')->get_node(1);
	my $childString = '<span id="logError">Dati inseriti errati</span>';
	my $child = $parserxml->parse_string($childString); #elimino il tag che identifica la versione dell'xml perché non devo aggiungerlo
	$child = $child->removeChild($child->firstChild());
	$form->insertBefore($child, $form->firstChild);
	
	#modifico il collegamento al CSS per riuscirlo a caricare
	$xpc->setContextNode($doc);
	my $css = $xpc->findnodes('//x:link[@type="text/css"]')->get_node(0);
	$css->setAttribute("href", '../public_html/CSS/home.css');
	
	#restituisco la pagina modificata
	return $doc;
}

#estraggo le parole del login
my $logString = CGI->new();
my $username = $logString->param('inputUsername');
my $password = $logString->param('inputPassword');
my $update = $logString->param('update');
my $finalDoc;

#estraggo i dati dall'XML
my $filexml = "../data/profili.xml";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->parse_file($filexml);
my $expectedUsername = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:username');
my $expectedPassword = $doc->findnodes('//p:profilo[@tipo = "amministratore"]/p:password');

if($update eq "yes") {
	$finalDoc = &update($username, $password, $expectedUsername, $expectedPassword);
	print "Content-type: text/html; charset=utf-8\n\n";
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

#applico il foglio di stile al file modificato
$filexml = "../data/database.xml";
my $parserxslt = XML::LibXSLT->new;
my $stylesheet  = $parserxslt->parse_stylesheet($finalDoc);
my $results     = $stylesheet->transform_file($filexml);
my $fileToPrint = $stylesheet->output_as_bytes($results);

print "<phtml>";
print "<body>";
print $fileToPrint;
print "</body>";
print "</html>";
