#!/usr/bin/perl
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser);
use Mail::Sendmail;
use CGI;
use XML::LibXML;

my $logString = CGI->new();
my $name = $logString->param('first_name');
my $surname = $logString->param('last_name');
my $userEmail = $logString->param('email');
my $email = 'ggardengroup@gmail.com';
my $text = $logString->param('comments');

#costruisce e invia l'email
sendmail(
	From 	=> $userEmail;
	To		=> $email;
	Subject	=> 'Domanda di '.$name.' '.$surname;
	Message => $name.' '.$surname.' ha posto la seguente domanda:\n'.$text;
);

#stampa contattaci.html
my $htmlPage = "../databaseManager.html";
my $parserxml  = XML::LibXML->new;
my $doc = $parserxml->load_html(location => $htmlPage, recover => 1);
print "Content-type: text/html; charset=utf-8\n\n";
print "<phtml>";
print "<body>";
print $doc;
print "<\body>";
print "<\html>";

