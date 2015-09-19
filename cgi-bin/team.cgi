#!/usr/bin/perl -w

use CGI::Carp qw(fatalsToBrowser);
use warnings;
use CGI;
use CGI::Session;
use XML::LibXML;
use HTML::Template;

require "function_user.cgi";	
require "function_block.cgi";
require "function_system.cgi";

########################
# VARIABILI D'AMBIENTE
########################
$q 	= CGI->new;
$session = &getSession;
$cookie = &getCookie;
$session->param('ableToSend',1);

########################
# TEMPLATE DECLARATION
########################
$template_header 		= HTML::Template->new( filename => '../public_html/template/header.tmpl' );
$template_user 			= HTML::Template->new( filename => '../public_html/template/loginbar.tmpl' );
$template_footer 		= HTML::Template->new( filename => '../public_html/template/footer.tmpl' );
my $template_content 	= HTML::Template->new( filename => '../public_html/template/team.tmpl' );

########################
# SETTING MODULE
########################
$template_header->param(BCUMBS=> 'Team');
&menuSection('TEAM');
&gestUtente('team.cgi');
$session->param('ableToComment',-1);

my $parser = XML::LibXML->new;
my $doc = $parser->parse_file("../public_html/xml/team.xml");
my $root = $doc->getDocumentElement();
my $root_nodes = $root->find('//persona');
my @template_rows =();
foreach my $node($root_nodes->get_nodelist() ){
	my %attribute = (
			IMG_SRC => $node->findnodes('./srcPath')->[0]->textContent(),
			NOME => $node->findnodes('./nome')->[0]->textContent(),
			DESCR => $node->findnodes('./descr')->[0]->textContent(),
			PRES => $node->findnodes('./presentazione')->[0]->textContent()	);
	push(@template_rows, \%attribute);
}
$template_content->param(TEAM_INFO => \@template_rows);

########################
# OUTPUT XHTML 
########################
binmode(STDOUT, ":iso-8859-1");
print 	$q->header( -cookie => $cookie )."\n";
print	$q->start_html( 
			-dtd => [ '-//W3C//DTD XHTML 1.0 Strict//EN','http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
			-title=>'Il Team - Quartiere7',
		    -author=>'Tous Les Memes',
		    -meta=> {	
		    		'title'=>'Quartiere7 - Team',
					'keywords'=>'Quartiere7,quartier youtuber, divertimento, comici, gruppo, team, ragazzi youtuber',
					'description content'=>'Quartiere7 gruppo comico youtube Home',
					'author'=>'TLM web design',
					},
			-lang=>'it-IT',
		   -style=>{ 'src'=>'../public_html/css/page_team.css'} ,
		   -script=>{ 'src'=>'../public_html/js/function_module.js'}
		   ), 
		$template_header->output(),
		$template_user->output(),
		$template_content->output(),
		$template_footer->output(), 
		$q->end_html(); 
		$session->flush();
