function AjaxAgregar(agregar_url){
    elemento = document.getElementById("carritospan");
    elemento.classList.remove("animacioncarrito");
    $.ajax({
        url: agregar_url,
        success: function(data) {
            elemento.classList.add("animacioncarrito");
            document.getElementById("carritospan").innerHTML = data;
            $("#liveToast").toast('show');
        },
        error: function() {alert("Hubo un error al agregar el producto!");}
    })
}

function AjaxComprar(agregar_url){
    $.ajax({
        url: agregar_url,
        success: function(data) {
            $("#carrito2").show(500);
            $("#carrito1").hide(500);
        },
        error: function() {alert("Hubo un error al agregar el producto!");}
    })
}