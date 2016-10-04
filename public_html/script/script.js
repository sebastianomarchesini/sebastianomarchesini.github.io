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

// Funzioni per la form della pagina "Contattaci"
/*
chiave: nome dell'input da controllare
[0]: prima indicazione per la compilazione dell'input
[1]: l'espressione regolare da controllare
[2]: hint nel caso in cui l'inpuit fornito sia sbagliato
*/
var dettagli_form={
	"first_name":["Mario", /^[A-Z][a-z]+/, "Inserisci il tuo nome"],
	"last_name":["Rossi", /^[A-Z][a-z]+( ([A-Z][a-z]+))?/, "Inserisci il tuo cognome"],
	"email":["Inserire e-mail", /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/, "Inserisci un indirizzo email valido"]
}

function caricamento() //carica i dati nei campi
{
for (var key in dettagli_form)
	{
		var input=document.getElementById(key);
		campoDefault(input);

		input.onfocus=function(){campoPerInput(this);}; //toglie l'aiuto
		input.onblur=function(){validazioneCampo(this);}; //fa la validazione del campo
	}
}

function campoDefault(input)
{
	if (input.value=="")
	{
		input.className="";
		input.value=dettagli_form[input.id][0];
	}
}

function campoPerInput(input)
{
	if (input.value==dettagli_form[input.id][0])
	{
		input.value="";
		input.className="";
	}
}

function validazioneCampo(input)
{
	var p=input.parentNode; //prende lo span

var errore=document.getElementById(input.id+"errore");

if (errore)
{
	p.removeChild(errore)
}

	var regex=dettagli_form[input.id][1];
	var text=input.value;
	if ((text==dettagli_form[input.id][0]) || text.search(regex)!=0) //occhio! controllo che l'input sia diverso dal placeholder (con il primo check)
	{
		mostraErrore(input);
		return false;
	}
	return true;
}

function validazioneForm()
{
	var corretto=true;
	for (var key in dettagli_form)
	{
		var input=document.getElementById(key);
		var risultato=validazioneCampo(input);
		corretto=corretto&&risultato;
	}
	return corretto;
}


function mostraErrore(input)
{
	console.log(input);
	var p=input.parentNode;
	var e=document.createElement("strong");
	e.className="errorSuggestion";
	e.id=input.id+"errore";
	//
	//input.id="errore";

	e.appendChild(document.createTextNode(dettagli_form[input.id][2]));
	p.appendChild(e);
}

//funzione che sostituisce l'immagine della mappa con la mappa in google maps
function replaceMap() {
	var map = document.getElementById("visualizzaMappa");
	map.innerHTML = "<iframe id='frameMappa' class='noprint' src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2800.9012391702986!2d11.885443115555669!3d45.41133107910034!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x477eda58b44676df%3A0xfacae5884fca17f5!2sTorre+Archimede%2C+Via+Trieste%2C+63%2C+35121+Padova+PD!5e0!3m2!1sit!2sit!4v1472819512186'></iframe><img id=\"fotoMappa\" class=\"print\" src=\"img/mappa.png\" alt=\"Mappa della sede di GGarden\" />";
}