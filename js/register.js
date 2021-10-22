$(document).ready(function() {

    $("#btn_registrarse").click(function(){
        let nombres = $("#txt_nombre_completo").val();
        let identificacion = $("#txt_identificacion").val();
        let edad = $("#txt_edad").val();
        let telefono = $("#txt_telefono").val();
        let correo = $("#txt_correo").val();
        let password = $("#txt_password").val();
        let repeat_password = $("#txt_repeat_password").val();
        if(
            nombres != "" && 
            identificacion != "" &&
            edad != "" &&
            telefono != "" &&
            correo != "" &&
            password != "" &&
            repeat_password != ""
        ){
            if (password == repeat_password){
                $.ajax({
                    type: 'POST',
                    url: 'http://localhost:8080/persona/registrar/usuario_final',
                    data: JSON.stringify({
                        "identificacion": identificacion,
                        "nombre": nombres, 
                        "correo_electronico": correo,
                        "password": password, 
                        "edad": edad,
                        "telefono" : telefono
                    }),
                    contentType: "application/json",
                }).done((res) => {
                    console.log(res);
                }).fail((err) => {
                    alert("Se ha presentado un problema con el servidor");
                    console.log("Error servidor registrarse", err);
                });
            } else {
                alert("Las contraseña no coinciden") 
            }
        } else {
            alert("Dejo un campo vacio")
        }
    })    
})