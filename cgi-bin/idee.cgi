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

#######################
# VARIABILI D'AMBIENTE
#######################
$q 	= CGI->new;
$session = &getSession;
$cookie = &getCookie;
$session->param('ableToSend',1);

#######################
# TEMPLATE DECLARATION
#######################
$template_header 		= HTML::Template->new( filename => '../public_html/template/header.tmpl' );
$template_user 			= HTML::Template->new( filename => '../public_html/template/loginbar.tmpl' );
$template_footer 		= HTML::Template->new( filename => '../public_html/template/footer.tmpl' );
$template_content 		= HTML::Template->new( filename => '../public_html/template/idee.tmpl', options => 'global_vars');

#######################
# SETTING MODULE
#######################
$template_header->param(BCUMBS => 'Idee');
&menuSection('IDEE');
&gestUtente('idee.cgi');

#######################
# GEST CONTENT
#######################
$A = &gestNewComment();
$n_idee = &isThereIdea(1);
if($n_idee){
	$template_content->param(IDEE,1);
	$template_content->param(IDEA,&getIdea());
	$template_content->param(N_IDEE,$n_idee);
}
defined $q->param('commenta') ? $session->param('ableToComment',$q->param('id_nuovo_commento')) : $session->param('ableToComment',-1);

########################
# OUTPUT XHTML 
########################
binmode(STDOUT, ":iso-8859-1");
print 	$q->header( -cookie => $cookie )."\n";
print	$q->start_html( 
			-dtd => [ '-//W3C//DTD XHTML 1.0 Strict//EN','http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
			-title=>'Quartiere7 - Idee',
		    -author=>'Tous Les Memes',
		    -meta=> {	
		    		'title'=>'Idee - Quartier7',
					'keywords'=>'Quartiere7, youtuber, divertimento, comico, idee scherzi,idee comiche',
					'description content'=>'Quartiere7 gruppo comico youtube Idee',
					'author'=>'TLM web design',
					},
			-lang=>'it-IT',
		   -style=>{ 'src'=>'../public_html/css/page_idee.css'},
		   -script=>{ 'src'=>'../public_html/js/function_module.js'}
		   ),
		$template_header->output(),
		$template_user->output(),
		$template_content->output(),
		$template_footer->output(), 
		$q->end_html(); 
		$session->flush();
