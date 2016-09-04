#!/usr/bin/perl
use strict;
use warnings;
use CGI::Session;
use CGI;

my $session = CGI::Session->load() or die CGI::Session->errstr;
if ( $session->is_expired ) {
    die "Your session expired. Please refresh your browser to re-start your session";
}
if ( $session->is_empty ) {
    print "New session needed";
}
	