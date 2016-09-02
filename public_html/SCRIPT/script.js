function logform() {
	// if(document.getElementById('log').clicked{
	// prompt(“Inserisci la login:”,“guest”);
	// }
}

// funzione per rendere a scomparsa il login dell'amministratore
function nascondi(){
//salvo sulla variabile nasc, lo style dell'elemento passato

   var e = document.getElementById('login');
   if(e.style.display != 'block')
      e.style.display = 'block';
   else
      e.style.display = 'none';
}