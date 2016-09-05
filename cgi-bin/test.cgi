#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;
use XML::LibXML;

my $session = CGI::Session->load() or die CGI::Session->errstr;
print "Content-type: text/html; charset=utf-8\n\n";
print "<phtml>";
print "<body>";
print $session->param('username');
print "</body>";
print "</html>";
	
