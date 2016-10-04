#!/usr/bin/perl
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use XML::LibXML;
use Net::SMTP;

#Carico i dati trasmessi dalla pagina e l'email del gruppo
my $logString = CGI->new();
my $name = $logString->param('first_name');
my $surname = $logString->param('last_name');
my $userEmail = $logString->param('email');
my $email = 'ggardengroup@gmail.com';
my $text = $logString->param('comments');

#Carico contattaci.html in modo da modificarla per comunicare all'utente se l'operazione ha avuto successo o no
my $htmlPage = "../public_html/contattaci.html";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);

#Aggiorno il link ai CSS
my $string = $doc->findnodes('//link[@href="CSS/home.css"]')->get_node(0);
$string->setAttribute("href", '../CSS/home.css');
$string = $doc->findnodes('//link[@href="css/print.css"]')->get_node(0);
$string->setAttribute("href", '../css/print.css');

#Aggiorno il link dell'immagine di Google Mpas
$string = $doc->findnodes('//img[@id="fotoMappa"]')->get_node(0);
$string->setAttribute("src", '../img/mappa.png');

#Aggiorno il link dello script JavaScript
$string = $doc->findnodes('//script')->get_node(0);
$string->setAttribute("src", '../SCRIPT/script.js');

#Aggiorno i link alle altre pagine
my @links = $doc->findnodes('//a[@href="home.html"]');
foreach my $link(@links){
	$link->setAttribute("href", '../home.html');
}
@links = $doc->findnodes('//a[@href="realizzazioni.html"]');
foreach my $link(@links){
	$link->setAttribute("href", '../realizzazioni.html');
}
@links = $doc->findnodes('//a[@href="cgi-bin/checkLog.cgi"]');
foreach my $link(@links){
	$link->setAttribute("href", 'checkLog.cgi');
}
@links = $doc->findnodes('//a[@href="contattaci.html"]');
foreach my $link(@links){
	$link->setAttribute("href", '../contattaci.html');
}
$string = $doc->findnodes('//form[@action="cgi-bin/search.cgi"]')->get_node(0);
$string->setAttribute("action", 'search.cgi');
$string = $doc->findnodes('//form[@action="../cgi-bin/email.cgi"]')->get_node(0);
$string->setAttribute("action", 'email.cgi');

if($name eq '' || $surname eq '' || $userEmail eq '' || $userEmail =~ /^[a-z0-9]([a-z0-9.]+[a-z0-9])?\@[a-z0-9.-]+$/ || $text eq '') {

}

#Il codice seguente è stato tratto dalla pagina https://www.studenti.math.unipd.it/index.php?id=corsi_tecweb.
my $smtp = Net::SMTP->new('smtp.studenti.math.unipd.it',
						   Hello => 'studenti.math.unipd.it',
						   Timeout => 30,
						   Debug => 1,
);

$smtp->mail($userEmail);
$smtp->to($email);
$smtp->data();
$smtp->datasend($name." ".$surname." ha posto la seguente domanda:\n".$text);

my $redirect=0;
if($redirect) {
	print "Status: 302 Moved\r\nLocation: perltestCARP.pl\r\n\r\n";
	$smtp->datasend("Lo script ha solo ridiretto il browser...\n");
} else {

#stampa contattaci.html

print "Content-type: text/html; charset=utf-8\n\n";
print "<phtml>";
print "<body>";
print $doc;
print "</body>";
print "</html>";
}
$smtp->dataend();
$smtp->quit;
