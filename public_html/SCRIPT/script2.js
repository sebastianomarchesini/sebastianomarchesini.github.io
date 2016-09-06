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

// $("#image").change(function() {

//     var val = $(this).val();

//     switch(val.substring(val.lastIndexOf('.') + 1).toLowerCase()){
//         case 'gif': case 'jpg': case 'png':
//             alert("an image");
//             break;
//         default:
//             $(this).val('');
//             // error message here
//             alert("not an image");
//             break;
//     }
// });
// Funzioni per la form della pagina "Contattaci"
/*
chiave: nome dell'input da controllare
[0]: prima indicazione per la compilazione dell'input
[1]: l'espressione regolare da controllare
[2]: hint nel caso in cui l'inpuit fornito sia sbagliato
*/

var dettagli_form_plant={
	"name":["Nome pianta", /^[A-Z][a-z]+/, "Inserisci il nome della pianta"],
	"scientificName":["Nome scientifico", /.*/, "" ],
	"type":["Tipo", /.*/ ,"" ],
	"price":["", /^\d+(.\d{1,2})?$/, "Inserisci il prezzo separato da una virgola"],
	"format":["per una confezione di 10 fiori", /.*/,""],
	"dataName":["Nome del dato", /.*/, ""],
	"dataContent":["valore", /.*/,""]
} 

var dettagli_form_tool={
	"name":["Nome pianta", /^[A-Z][a-z]+/, "Inserisci il nome dell'attrezzo'"],
	 "type":["Tipo", /.*/, ""],
	"price":["", /^\d+(.\d{1,2})?$/, "Inserisci il prezzo separato da una virgola"],
	"format":["al pezzo",/.*/,""],
	"dataName":["Nome del dato", /.*/, ""],
	"dataContent":["valore", /.*/,""]

}

function caricamentoPianta(){
	return caricamento(dettagli_form_plant);
}

function caricamentoAttrezzi(){
	return caricamento(dettagli_form_tool);
}


function caricamento(matrix) //carica i dati nei campi
{
	var img=document.getElementById("image");
	img.onchange=function(){checkImage(this);};
for (var key in matrix)
	{
		var input=document.getElementById(key);
		campoDefault(matrix, input);

		input.onfocus=function(){campoPerInput(matrix, this);}; //toglie l'aiuto
		input.onblur=function(){validazioneCampo(matrix, this);}; //fa la validazione del campo
	}
}

function campoDefault(matrix, input)
{
	if (input.value=="")
	{
		input.className="";
		input.value=matrix[input.id][0];
	}
}

function campoPerInput(matrix, input)
{
	if (input.value==matrix[input.id][0])
	{
		input.value="";
		input.className="";
	}
}

function validazioneCampo(matrix, input)
{
	var p=input.parentNode; //prende lo span
	var errore=document.getElementById(input.id+"errore");
	if (errore)
	{
		p.removeChild(errore)
	}

	var regex=matrix[input.id][1];
	var text=input.value;
	if ((text==matrix[input.id][0]) || text.search(regex)!=0) //occhio! controllo che l'input sia diverso dal placeholder (con il primo check)
	{
		mostraErrore(matrix, input);
		return false;
	}
	return true;
}


function checkPictureType(Extension){
	return (Extension == "gif" || Extension == "png" || Extension == "bmp"
                || Extension == "jpeg" || Extension == "jpg");
}

function checkImage() {
    var fuData = document.getElementById('image');
    var p=fuData.parentNode; //prende lo span
	var errore=document.getElementById(fuData.id+"errore");
	if(errore){
		p.removeChild(errore);
	}
    var FileUploadPath = fuData.value;

    if (FileUploadPath == '') {
        // alert("Please upload an image");
        // errImg(fuData);
        return true;
    } else {
        var Extension = FileUploadPath.substring(
                FileUploadPath.lastIndexOf('.') + 1).toLowerCase();
 	if (checkPictureType(Extension)) {
            if (fuData.files && fuData.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $('#image').attr('src', e.target.result);
                }
                reader.readAsDataURL(fuData.files[0]);
            }
            return true;
        } 
  else {
            // alert("Photo only allows file types of GIF, PNG, JPG, JPEG and BMP. ");
            errImg(fuData);
            return false;
        }
    }
}


function validazioneFormPlant(){
	return validazioneForm(dettagli_form_plant);
}

function validazioneFormTool(){
	return validazioneForm(dettagli_form_tool);
}

function validazioneForm(matrix)
{
	var corretto=true;
	var resImg=checkImage();
	console.log("image", resImg);
	corretto=corretto&&resImg;
	for (var key in matrix)
	{
		var input=document.getElementById(key);
		var risultato=validazioneCampo(matrix, input);
		console.log(key, risultato);
		corretto=corretto&&risultato;
	}
	return corretto;
}


function mostraErrore(matrix, input)
{
	console.log(input);
	var p=input.parentNode;
	var e=document.createElement("strong");
	e.className="errorSuggestion";
	e.id=input.id+"errore";
	//
	//input.id="errore";

	e.appendChild(document.createTextNode(matrix[input.id][2]));
	p.appendChild(e);
}

function errImg(){
	console.log("image");
	var p=(document.getElementById("image")).parentNode;
	var e=document.createElement("strong");
	e.className="errorSuggestion";
	e.id=(document.getElementById("image")).id+"errore";
	//
	//input.id="errore";

	e.appendChild(document.createTextNode("Inserisci un file immagine"));
	p.appendChild(e);
}

var n_Prezzo=1;
var n_Valore=1;

function addPrezzo(){
	var container=document.getElementsByClassName('create');
	// container.appendChild(document.createTextNode("Member " + (i+1)));
    // Create an <input> element, set its type and name attributes
    var ln=document.createElement("li");
    var par=document.createElement("p");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "price" + n_Prezzo;
    var lbl=document.createElement("label");
    lbl.setAttribute("for", "price" + (n_Prezzo + 1));
    var t = document.createTextNode("Prezzo: &euro; ");
    lbl.appendChild(t);
    par.appendChild(lbl);
    par.appendChild(input);
    ln.appendChild(par)
    container.appendChild(ln);
    n_Prezzo=n_Prezzo+1;
}

var counter_prezzo = 1;
var counter_valore = 1;
var limit_prezzo = 3;
var limit_valore=3;

function addInputPrice(divName){
	var toInsert='<label for="price">Prezzo: &euro; </label><input type="text" name="price'+ (counter_prezzo+1) +'" id="price'+ (counter_prezzo+1) +'" placeholder="3.99"/><label for="format'+ (counter_prezzo+1) +'">Formato:</label><input type="text" name="format'+ (counter_prezzo+1) +'" id="format'+ (counter_prezzo+1) +'" placeholder="al pezzo"/>';
	counter_prezzo = addInput(divName, counter_prezzo, limit_valore, toInsert);
}

function addInputValue(divName){
	var toInsert='<label for="dataName">Dato:</label><input type="text" name="dataName" id="dataName'+ (counter_prezzo+1) +'" placeholder="Lunghezza manico"/><label for="dataContent'+ (counter_prezzo+1) +'">Contenuto:</label><input type="text" name="dataContent'+ (counter_prezzo+1) +'" id="dataContent'+ (counter_prezzo+1) +'" placeholder="10 cm"/>';
	counter_valore = addInput(divName, counter_valore, limit_valore, toInsert);
}

function addInput(divName, counter, limit, toInsert){
    if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
    }
    else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = toInsert;
          document.getElementById(divName).appendChild(newdiv);
          counter++;
          return counter;
     }
}
