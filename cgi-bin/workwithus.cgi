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

########################
# TEMPLATE DECLARATION 
########################
$template_header 		= HTML::Template->new( filename => '../public_html/template/header.tmpl' );
$template_user 			= HTML::Template->new( filename => '../public_html/template/loginbar.tmpl' );
$template_footer 		= HTML::Template->new( filename => '../public_html/template/footer.tmpl' );
$template_content 		= HTML::Template->new( filename => '../public_html/template/workwithus.tmpl' );

########################
# SETTING MODULE
########################
&menuSection('WORK');
&gestUtente('workwithus.cgi');

########################
# SETTING CONTENT
########################
$template_header->param(BCUMBS=> 'Posta Idea');
&gestNewRequestIdea();
$session->param('ableToComment',-1);
########################
# OUTPUT XHTML 
########################
binmode(STDOUT, ":iso-8859-1");
print 	$q->header( -cookie => $cookie )."\n";
print	$q->start_html( 
			-dtd => [ '-//W3C//DTD XHTML 1.0 Strict//EN','http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
			-title=>'Posta idea - Quartiere7',
		    -author=>'Tous Les Memes',
		    -meta=> {	
		    		'title'=>'Quartiere7 - Home',
					'keywords'=>'Quartiere7, youtube, divertimento, comico, scherzi, idee scherzi, volti nuovi,successo online,',
					'description content'=>'Quartiere7 gruppo comico youtube Home',
					'author'=>'TLM web design',
					'language'=>'italian it' 
					},
			-lang=>'it-IT',
		   -style=>{ 'src'=>'../public_html/css/page_workWithUs.css'} ,
		   -script=>{ 'src'=>'../public_html/js/function_module.js'}
		   ), 
		$template_header->output(),
		$template_user->output(),
		$template_content->output(),
		$template_footer->output(),
		$q->end_html(); 
		$session->flush();





