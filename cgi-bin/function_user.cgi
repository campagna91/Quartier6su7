#############################################################
# FUNCTION_USER TRATTA TUTTE LE FUNZIONI RELATIVE ALL'UTENTE 
#  					E DI CONTORNO AD ESSO 
##############################################################


###########################
# => GETCOOKIE 
#
# Inizializza il cookie 
# tramite il cookie di 
# default CGISESSID
###########################
sub getCookie{
	$cookie = $session->cookie(CGISESSID => $session->id );
}

##########################
# => ISLOGGED 
#
# subroutine booleana che
# restituisce 0 oppure 1 
# a seconda che l'utente 
# sia visitatore o loggato
###########################
sub isLogged{
	$logged = $session->param('logged') || 0;
	return $logged;
}

###########################
# => EXIT 
#
# Subroutine richiesta 
# dall'utente in caso di 
# logout la quale non fa
# altro che far scadere
# i cookie, eliminando la
# sessione scollegando 
# l'utente
###########################

sub exit{
	$session->delete();
	my $c = CGI::Cookie->new(
						-name    =>  'MEMES',
                        -value   =>  $session->param('nick'),
                        -expires =>  '-3M');
	return $c;
}

###########################
# => ISADMIN 
#
# la subroutine restitui-
# sce 1 in caso in cui l'-
# utente '$nick' sia admin
###########################
sub isAdmin{
	my ($nick) = @_;
	#XML PARSING
	$parser = new XML::LibXML;
	$userFile =  '../public_html/xml/utenti.xml';
	$doc = $parser->parse_file( $userFile ) || die( 'Parsing fail: check the status of DB or contact Webmaster at info@toutlesmemes.it' );
	$utenti = $doc->getDocumentElement;
	$stored_type= $utenti->find( '/utenti/utente[@username=\''.$nick.'\']/tipo' )->[0];
	$type = $stored_type->textContent();
	if($type eq 'admin') { return 1;}
	else { return 0; }
}
###########################
# => NAMEFROMNICK
#
# converte lo username 
# utente nel suo nome di 
# iscrizione 
###########################
sub nameFromNick{
	my $nick = $_[0];
	#print "[".$nick."]";
	#XML PARSING
		$parser = new XML::LibXML;
		$userFile =  '../public_html/xml/utenti.xml';
		$doc = $parser->parse_file( $userFile ) || die( 'Parsing fail: check the status of DB or contact Webmaster at info@toutlesmemes.it' );
		$utenti = $doc->getDocumentElement;
		$stored_name= $utenti->find( '/utenti/utente[@username=\''.$nick.'\']/nome' )->[0];
		$name = $stored_name->textContent();
		return $name; 

}

###########################
# => LOGIN
#
# come da titolo la fun-
# zione permette il login
# per i collaboratori 
###########################
sub login{
	my $username = $_[0];
	my $password = $_[1];

	if( $username and $password){ # e se username e password son definiti
		# SQL INJECTION PREVENT
		if ($username =~ /'/ or $password =~ /'/) { return 0;}
		# XML PARSING
		$parser = new XML::LibXML;
		$userFile =  '../public_html/xml/utenti.xml';
		$doc = $parser->parse_file( $userFile ) || die( 'Parsing fail: check the status of DB or contact Webmaster at info@toutlesmemes.it' );
		$utenti = $doc->getDocumentElement || die ('element get document fail');
		# INFORMATION RECOVERY
		my $stored_password 	= $utenti->find('/utenti/utente[@username=\''.$username.'\']/password')->[0] ;
		my $stored_name 		= $utenti->find('/utenti/utente[@username=\''.$username.'\']/nome')->[0];
		my $stored_type	 		= $utenti->find('/utenti/utente[@username=\''.$username.'\']/tipo')->[0];
		$user = defined $stored_name ? $stored_name->textContent() : undef;
		
		# UTENTE PRESENTE
		if($user){ 
			if($password eq $stored_password->textContent()){ # password ok 
				return 1;
			} else {
				return 0;
			}
		} 
		#UTENTE NON PRESENTE
		else { 
			return 0; 
		} 
	}
	#PARAMETRI NON SETTATI
	else {
		return 0;
	}
}

###########################
# => GESTUTENTE
#
# tale tratta il caso uten-
# te, riconoscendo quindi
# tentativi di login, ac-
# cesso normale o semplice
# logout settando la relati-
# va barra (login bar)
###########################
sub gestUtente(){
	my ($page) = @_;

	if(&isLogged()){
		# RICHIESTA DI LOGOUT
		if($q->param('logout')){
			&exit;
			&setUserBar(0,0,0,$page,0);
		}else{
			# UTENTE ATTUALMENTE LOGGATO
			&setUserBar($session->param('nick'),&isAdmin($session->param('nick')),0,$page,'0');
		}	
	} else {
		# RICHIESTA DI LOGIN
		if($q->param('login')){
			if(&login($q->param('username'),$q->param('password'))){
				$session->param('nick',$q->param('username'));
				$session->param('logged',1);
				&setUserBar($session->param('nick'),&isAdmin($session->param('nick')),0,$page,0);
			} else {
				# LOGIN ERRATO
				&setUserBar(0,0,1,$page,0);
			}
		}else{
			# NESSUNA RICHIESTA
			&setUserBar(0,0,0,$page,0);
		}
	}
}

1;
