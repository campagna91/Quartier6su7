########################
# => SESSION MAINTENANCE
#
# Subroutine responsabile
# di restituire la sessio-
# ne attualmente disponi-
# bile
########################
sub getSession() {
	$id = $q->cookie('CGISESSID') || $q->param('CGISESSID') || undef;
	$s = new CGI::Session('driver:File', $id, { Directory=>File::Spec->tmpdir });
	return $s;
}


########################
# => COOKIE MAINTENANCE 
#
# subroutines di settag-
# gio e creazione cookie
########################

sub setCookie{
	my ($user) = @_;
	 my $c = CGI::Cookie->new(-name    =>  'MEMES',
                          -value   =>  "$user",
                          -expires =>  '+3M');
	return $c;
}

1;