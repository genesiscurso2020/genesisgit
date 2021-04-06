$(function(){
	// #@[p_js_general_01] //
	var enlace = $('#link-busqueda');
	// #@[p_js_general_02] //
	enlace.on('click',function(){
	// #@[p_js_general_03] //
		var texto = $('#textob');
	// #@[p_js_general_04] //
		enlace.attr('href','http://127.0.0.1:8000/');
	// #@[p_js_general_05] //
		// enlace.attr('href',"{% url 'proyectos:lista' %}" + '?criterio=' + texto);
		// enlace.attr('href','http://www.microsoft.com');
	});
	// #@[p_js_general_06] //
}())
	// #@[p_js_general_07] //

@busqueda