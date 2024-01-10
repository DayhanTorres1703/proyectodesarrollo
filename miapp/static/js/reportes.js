$(function() {
    //Definir intervalo
    //en el intervalo hacer peticiones get ajax a la vista leerReportes
    //recargar el div de mensajes
    setInterval(function(){
        $.get("/leer_reportes/", function(data){
            $("#reportes").html("");
            $.each(data, function(i, mensajes){
                $("#reportes").append("<div>" + + "</div>")
            });
        });
    }, 3000);

});