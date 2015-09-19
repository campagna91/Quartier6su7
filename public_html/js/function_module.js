function checkIn(element,default_value){
	if(element.value==default_value){
		element.value = '';
	}
}
function checkOut(element,default_value){
	if(element.value==''){
		element.value = default_value;
	}
}


function checkNewComment(element){

var figli = element.childNodes;
if(figli[1].value=='' || figli[1].value== 'Tuo nome'){
	figli[3].style.visibility="visible";
	if(figli[5].value=='' || figli[5].value=='Testo del commento'){
		figli[9].style.visibility="visible";
		return false;
	}
	return false;
} else {
	return true;
}
}