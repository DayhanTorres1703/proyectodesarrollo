// miapp/static/js/validacion.js

//EJEMPLO PARA VALIDAR DATOS EN FORMULARIO
$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault();

        var nombre = $('input[name="nombre"]').val();
        
        //var edad = $('input[name="edad"]').val();

        //if (nombre === '' || edad === '') {
          if(nombre === '') {
            alert('Todos los campos deben ser completados');
            return;
        }

        this.submit();
    });
});
