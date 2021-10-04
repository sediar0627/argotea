$(document).ready(function () {
    $(".link_lista_bebidas").click(function (e) {
        window.location.href = "lista_bebidas.html";
    })

    $(".link_lista_deseos").click(function (e) {
        window.location.href = "lista_deseos.html";
    })

    $(".link_realizar_pedido").click(function (e) {
        window.location.href = "realizar_pedido.html";
    })

    $("#btn-buscar-bebida").click(function (e) {
        window.location.href = "bebida.html?" + $("#txt-buscar-bebida").val();
    })

    $(".calificacion").click(function () {
        for (let i = 5; i >= 1; i--) {
            $("#calificacion" + i).css({ "color": "#858796" });
        }
        let index = $(this).attr("data-index");
        localStorage.removeItem("calificacion-bebida-estrellas");
        localStorage.setItem("calificacion-bebida-estrellas", index);
        for (let i = index; i >= 1; i--) {
            $("#calificacion" + i).css({ "color": "#51732F" });
        }
    })

    $(".calificacion").mouseenter(function () {
        let index = $(this).attr("data-index");
        for (let i = index; i >= 1; i--) {
            $("#calificacion" + i).css({ "color": "#51732F" });
        }
    });

    $(".calificacion").mouseleave(function () {
        let index_seleccionado = localStorage.getItem("calificacion-bebida-estrellas");
        if (index_seleccionado) {
            for (let i = 5; i > index_seleccionado; i--) {
                $("#calificacion" + i).css({ "color": "#858796" });
            }
        } else {
            for (let i = 5; i >= 1; i--) {
                $("#calificacion" + i).css({ "color": "#858796" });
            }
        }
    });

    $(".btn-limpiar-calificacion").click(function (e) {
        localStorage.removeItem("calificacion-bebida-estrellas");
        for (let i = 5; i >= 1; i--) {
            $("#calificacion" + i).css({ "color": "#858796" });
        }
    })


})