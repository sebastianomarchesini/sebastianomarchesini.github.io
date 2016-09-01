#!/usr/bin/perl
use strict;
use warnings;
use HTML::TreeBuilder;
use HTML::HTML5::Writer;

my $html = HTML::TreeBuilder->new();
$html->parse_file('../home_andrea.html');
my $writer = HTML::HTML5::Writer->new();
