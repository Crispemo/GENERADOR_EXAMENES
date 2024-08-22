function validateForm() {
    var x = document.forms["myForm"]["num_questions"].value;
    if (x == "") {
        alert("El número de preguntas debe ser completado.");
        return false;
    }
}

document.getElementById("myButton").onclick = function() {
    document.getElementById("message").innerText = "Formulario enviado!";
    document.getElementById("myDiv").style.transition = "transform 2s";
    document.getElementById("myDiv").style.transform = "rotate(20deg)";
};

document.getElementById("myButton").addEventListener("click", function() {
    alert("¡Botón clicado!");
});
