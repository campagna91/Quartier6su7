###########################################################
# FUNCTION_BLOCK È UN'INSIEME DI FUNZIONI RESPONSABILI DEL-
# L'INIZIALIZZAZIONE DEI MODULI DI PAGINA COME LOGIN BAR, 
# CONTENUTI, AZIONI SUI CONTENUTI ED ALTRO ANCORA 
###########################################################
require "function_user.cgi";

########################
# => SETUSERBAR
#
# subroutines richiesta 
# per il settaggio della
# login bar utente
########################
sub setUserBar{
	my ($name,$admin,$error,$action,$prev_user) = @_;
	$template_user->param(NAME_USER 	=> 	$name 	);
	$template_user->param(ACTION 		=> 	$action	);
	$template_user->param(ERROR_LOGIN 	=>  $error  );
	return $c;
	}

########################
# => MENUSECTION
#
# subroutines relativa al  
# settaggio del menu con-
# sentendo maggior acces-
# sibilità visiva 
########################
sub menuSection{

	if ($_[0] eq "HOME") 
	{
		$template_header->param('HOME',"actual_section");
		$template_header->param('IDEE',"not_actual_section");
		$template_header->param('WORK',"not_actual_section");
		$template_header->param('TEAM',"not_actual_section");
	}
	if ($_[0] eq "IDEE") 
	{
		$template_header->param('HOME',"not_actual_section");
		$template_header->param('IDEE',"actual_section");
		$template_header->param('WORK',"not_actual_section");
		$template_header->param('TEAM',"not_actual_section");
	}
	if ($_[0] eq "WORK") 
	{
		$template_header->param('HOME',"not_actual_section");
		$template_header->param('IDEE',"not_actual_section");
		$template_header->param('WORK',"actual_section");
		$template_header->param('TEAM',"not_actual_section");
	}
	if ($_[0] eq "TEAM") 
	{
			$template_header->param('HOME',"not_actual_section");
			$template_header->param('IDEE',"not_actual_section");
			$template_header->param('WORK',"not_actual_section");
			$template_header->param('TEAM',"actual_section");
	}
}

########################
# => ISTHEREIDEA
#
# subroutine responsabile
# di appurare se esistono
# o meno idee del DB
########################
sub isThereIdea{
	my ($db) = $_[0];
	$ideaFile = $db == 1 ? '../public_html/xml/idee.xml' : '../public_html/xml/ideeAccept.xml';
	$parser = new XML::LibXML;
	$doc = $parser->parse_file($ideaFile) || die('Error happened reading idee.xml');
	$idee = $doc->getDocumentElement;
	my $aux = $doc->findvalue("count(//idea)");
	return $aux;
}
########################
# => GETIDEAACCEPT
#
# subroutine responsabile
# mostrare a schermo tutte
# le idee proposte sogget-
# te ancora ad accettazione
########################
sub getIdeaAccept{
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file("../public_html/xml/ideeAccept.xml");
	my $root = $doc->getDocumentElement();
	my $idee = $root->findnodes('/idee/idea');
	@rows = ();
	foreach $element ( $idee->get_nodelist)
	{
		my $idi = $element->getAttribute('id');
		my %stack_ideeAccept = (
			ID => $idi,
			NOME => $element->findnodes('./nome')->[0]->textContent(),
			EMAIL => $element->findnodes('./email')->[0]->textContent(),
			TELEFONO => $element->findnodes('./telefono')->[0]->textContent(),
			TITOLO => $element->findnodes('./titolo')->[0]->textContent(),
			TESTO => $element->findnodes('./testo')->[0]->textContent(),
		);
		push @rows, \%stack_ideeAccept;
	}
	return \@rows;
}

########################
# => GETIDEA
#
# subroutine responsabile
# mostrare a schermo tutte
# le idee proposte con re-
# lativi commenti
########################
sub getIdea{
	# INIZIALIZZO IL PARSER
	my $ideaFile = '../public_html/xml/idee.xml';
	my $parser = new XML::LibXML;
	my $doc = $parser->parse_file($ideaFile) || die('Error happened reading idee.xml');
	my $idee = $doc->getDocumentElement;
	my $idea = $idee->find(' /idee/idea');
	my @template_rows = (); 
	foreach my $element ( $idea->get_nodelist())
	{	
		my $idi=$element->getAttribute('id');
		
		# RECUPERO I COMMENTI 
		my @template_rows_commenti = ();
		my $path = '/idee/idea[@id='.$idi.']/discussione/commento';
		my $commenti = $idee->find($path);
		foreach my $commento ($commenti->get_nodelist())
		{
			my %stack_commenti = (
					AUTORE_COMMENTO => $commento->findnodes('./autore')->[0]->textContent(),
					TESTO_COMMENTO => $commento->findnodes('./testo')->[0]->textContent(),
			);
			push (@template_rows_commenti, \%stack_commenti);
		}	
		# RECUPERO L'IDEA
		my %stack_idea = (
			ID => $idi,
			AUTORE_IDEA => $element->findnodes('./nome')->[0]->textContent(),
			TITOLO_IDEA => $element->findnodes('./titolo')->[0]->textContent(), 
			MAIL_IDEA => $element->findnodes('./email')->[0]->textContent(), 
			TELEFONO_IDEA => $element->findnodes('./telefono')->[0]->textContent(), 
			#VIDEO => $element->findnodes('./url')->[0]->textContent() || undef,
			TESTO_IDEA => $element->findnodes('./testo')->[0]->textContent() || undef,
			COMMENTI => \@template_rows_commenti,
		);
		# AGGIUNGO I COMMENTI ALLA LISTA PRECEDENTE
		push(@template_rows , \%stack_idea);
	}
	return \@template_rows;
}

########################
# => GESTNEWCOMMENT
# 
# subroutines la quale cat-
# tura in caso sia stato
# inoltrato il nuovo commento
# aggiungendolo al nodo 
# competente 
########################
sub gestNewComment{
	if($q->param('commenta')){
		if($session->param('ableToComment') != $q->param('id_nuovo_commento'))
		{
			if($q->param('autore_nuovo_commento') eq '' || $q->param('autore_nuovo_commento') eq 'Tuo nome')
			{
				# NOME AUTORE NUOVO COMMENTO VUOTO
					$template_content->param(ERROR_COMMENT,1);
					$template_content->param(ID_FAIL=>$q->param('id_nuovo_commento'));
					$template_content->param(TITOLO_IDEA_FAIL,$q->param('titolo_idea_hidden'));
				return -2;
			} else {
				if($q->param('testo_nuovo_commento') eq '' || $q->param('testo_nuovo_commento') eq 'Testo del commento')
				{	
					# TESTO COMMENTO VUOTO
					$template_content->param(ERROR_COMMENT,1);
					$template_content->param(ID_FAIL=>$q->param('id_nuovo_commento'));
					$template_content->param(TITOLO_IDEA_FAIL,$q->param('titolo_idea_hidden'));
					return -1;
				} else {
					# RECUPERO ID COMMENTO
					my $id = $q->param('id_nuovo_commento');
					# ISTANZIO IL PARSER
					my $ideaFile = '../public_html/xml/idee.xml';
					my $parser = new XML::LibXML;
					my $doc = $parser->parse_file($ideaFile) || die('Error happened reading idee.xml');
					my $idee = $doc->getDocumentElement;
					my $node = $idee->findnodes('/idee/idea[@id='.$id.']/discussione')->[0];

					# CREAO ED APPENDO IL NUOVO COMMENTO
					my $commento = $node->ownerDocument->createElement('commento');
					my $autore = $node->ownerDocument->createElement('autore');
					my $testo = $node->ownerDocument->createElement('testo');
					$autore->appendText( $q->param('autore_nuovo_commento'));
					$testo->appendText( $q->param('testo_nuovo_commento'));
					$commento->appendChild($autore);
					$commento->appendChild($testo);
					$node->appendChild($commento);
					my $state = $doc->toFile('../public_html/xml/idee.xml');
					# SCRITTURA ANDATA A BUON FINE
					$session->param('ableToComment',$id);
					$template_content->param(RIGHT_COMMENT=>1);
					return 1;
				}
			}
		} else { 
			# REFRESH PAGE OR SIMPLE ACCESS 
			return 0; 
		}
	}
}
########################
# => ACCETTAIDEAREQUEST
#
# competente nel trattare
# le richieste doveìute a
# nuove idee
########################
sub gestRequestForIdea{
		my $dest = "../public_html/xml/ideeAccept.xml";
		my $parser = XML::LibXML->new;
		my $doc = $parser->parse_file($dest);
		my $root = $doc->getDocumentElement();
		my $idee = $root->find('/idee')->[0];
		# CREO I NODI
		my $idea = $idee->ownerDocument->createElement('idea');
		my $nome = $idea->ownerDocument->createElement('nome');
		my $email = $idea->ownerDocument->createElement('email');
		my $titolo = $idea->ownerDocument->createElement('titolo');
		my $telefono = $idea->ownerDocument->createElement('telefono');
		my $descrizione = $idea->ownerDocument->createElement('testo');
		# NE DEFINISCO I VALORI
		$nome->appendText($q->param('nome'));
		$email->appendText($q->param('email'));
		$titolo->appendText($q->param('titolo'));
		$telefono->appendText($q->param('telefono'));
		$descrizione->appendText($q->param('descrizione'));
		# CREO IL NODO IDEA
		$idea->appendChild($nome);
		$idea->appendChild($email);
		$idea->appendChild($titolo);
		$idea->appendChild($telefono);
		$idea->appendChild($descrizione);
		# STABILISCO IL NUOVO E GIUSTO ID UNIVOCO
		if(&isThereIdea(0) > 0){
			$max = $idee->findnodes('./idea[last()]')->[0]->getAttribute('id');
		} else { 
			$max = -1; 
		}
		$max = $max + 1;
		$idea->setAttribute('id',$max);
		# APPENDO E SCRIVO
		$idee->appendChild($idea);
		my $state = $doc->toFile($dest);	
}

########################
# => ACCETTAIDEAREQUEST
# subroutines che non fa
# altro che iscrivere l'idea
# inviata nel db da esposizione
# ('idee.xml') cancellandola 
# poi da quello temporaneo
########################
sub accettaIdeaRequest{
	my ($id) = $_[0];
	# DB TEMPORANEO 
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file("../public_html/xml/ideeAccept.xml");
	my $root = $doc->getDocumentElement();
	my $node_accepted = $root->findnodes('/idee/idea[@id='.$id.']')->[0];
	# DB DI DESTINAZIONE
	my $dest = '../public_html/xml/idee.xml';
	my $parser = new XML::LibXML;
	my $doc = $parser->parse_file($dest) || die('Error happened reading idee.xml');
	my $root = $doc->getDocumentElement;
	my $idee = $root->find('/idee')->[0];
	# PER ESSERE UNIVOCO L'ID LO PONGO PARI ALL'ULTIMO+1
	if(&isThereIdea(1) > 0){
		$max = $idee->findnodes('./idea[last()]')->[0];
		$max = $max->getAttribute('id');
	} else {
		$max = -1;
	}
		$max = $max+1;
	#E EVITO PROBLEMI DI REFRESH
	if($node_accepted){
		$new_node = $node_accepted->cloneNode(1);
		$new_node->setAttribute('id',$max);
		my $discussione = $root->ownerDocument->createElement('discussione');
		$new_node->appendChild($discussione);
		$idee->appendChild($new_node);
		my $state = $doc->toFile($dest);
		&eliminaIdeaRequest($id);
	}
}
########################
# => ELIMINAIDEAREQUEST
# elimina l'idea soggetta 
# alla non approvazione del
# personale 
########################
sub eliminaIdeaRequest{
	my ($id) = $_[0];
	my $parser = XML::LibXML->new;
	my $doc = $parser->parse_file("../public_html/xml/ideeAccept.xml");
	my $root = $doc->getDocumentElement();
	my $idee = $root->findnodes('/idee/idea[@id='.$id.']')->[0];
	# EVITO ERRORI DI REFRESH ;) 
	if($idee){
		$idee->unbindNode;
		my $state = $doc->toFile('../public_html/xml/ideeAccept.xml');
	}
	
}
########################
# => GESTNEWREQUESTIDEA
# è una macro subroutines
# responsabile per le richie-
# ste riguardanti accettazioni
# e / o negazioni delle nuove 
# idee
########################
sub gestNewRequestIdea{
	if(&isLogged()){

		$template_content->param(ADMIN,&isAdmin($session->param('nick')));
		if($q->param('accept')){ 
			&accettaIdeaRequest($q->param('id'));	
		}
		else{
			if($q->param('delete')){ 
				&eliminaIdeaRequest($q->param('id')); 
			}
		}
		$template_content->param(IDEAACCEPT,&getIdeaAccept());
	} else {
		if($q->param('invia_idea')){ 
			$ableToSend = defined $session->param('ableToSend') ? $session->param('ableToSend') : 1;
			if($ableToSend){
				my $errorForm = 0; 
				if($q->param('nome') eq 'Tuo nome') { $template_content->param(EMPTY_NAME,1);$errorForm = 1;}
				if($q->param('titolo') eq 'Titolo idea') { $template_content->param(EMPTY_TITOLO,1);$errorForm = 1;}
				if($q->param('descrizione') eq 'Descrizione idea') { $template_content->param(EMPTY_TESTO,1);$errorForm = 1;}
				if($q->param('telefono') eq 'Recapito telefonico' || $q->param('telefono')!~ /^[+-]?\d+$/) { $template_content->param(EMPTY_TEL,1);$errorForm = 1;}
				if($q->param('email') eq 'Email tua' || $q->param('email') !~/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/) { $template_content->param(EMPTY_EMAIL,1);$errorForm = 1;}
				if($errorForm)
				{
					$template_content->param(INVIATO,0);
					$template_content->param(PREVIOUS_NAME,$q->param('nome'));
					$template_content->param(PREVIOUS_EMAIL,$q->param('email'));
					$template_content->param(PREVIOUS_TITLE,$q->param('titolo'));
					$template_content->param(PREVIOUS_TEL,$q->param('telefono'));
					$template_content->param(PREVIOUS_TEXT,$q->param('descrizione'));
				} else {
					&gestRequestForIdea();	
					$template_content->param(INVIATO,1);
					$session->param('ableToSend',0);			
				} 
			}
		} else {
			$template_content->param(ADMIN,0);
			$template_content->param(PREVIOUS_NAME,'Tuo nome');
			$template_content->param(PREVIOUS_EMAIL,'Email tua');
			$template_content->param(PREVIOUS_TEL,'Recapito telefonico');
			$template_content->param(PREVIOUS_TITLE,'Titolo idea');
			$template_content->param(PREVIOUS_TEXT,'Descrizione idea');
		}
	}
}

1; 
