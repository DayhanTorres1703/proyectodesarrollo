$(function(){
    $("#enviarRespaldo").click(function() {
        var cron_unido = $("#minutos").val() + " " + $("#horas").val() + " " + $("#dias_mes").val() + " " + $("#meses").val() + " " + $("#dias_semana").val();
        var cron_cadena = cron_unido.toString();
        $.post( "/respaldar_servidor/", 
        { ipOrigen: $("#servidorOrigen").val(), 
        ipDestino: $("#servidorDestino").val(), 
        dirOrigen: $("#directorioOrigen").val(), 
        dirDestino: $("#directorioDestino").val(), 
        cron: cron_cadena},
        function(data, status){
            if(status == "error"){
                if(data.status != "OK"){
                    alert("No se lograron mandar los datos");
                }
            }
        });
    });
});