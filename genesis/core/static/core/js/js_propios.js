$(function(){
	var enlace = $('#link-busqueda');
	enlace.on('click',function(){
		var texto = $('#textob');
		// alert(texto.val())
		enlace.attr('href','http://127.0.0.1:8000/proyectos/lista?duplica=0&criterio=' + texto.val());
		// enlace.attr('href',"{% url 'proyectos:lista' %}" + '?criterio=' + texto);
		// enlace.attr('href','http://www.microsoft.com');
	});
}())

// @busquedas