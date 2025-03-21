document.addEventListener("DOMContentLoaded", function() {
    
    const tipMesajSelect = document.querySelector(".styled-choicefield");
    const dataNasteriiInput = document.querySelector(".styled-date");

    tipMesajSelect.addEventListener("change", function() {
        if (tipMesajSelect.value !== "") {
            tipMesajSelect.classList.add("changed");
        } else {
            tipMesajSelect.classList.remove("changed");
        }
    });
    
    dataNasteriiInput.addEventListener("change", function() {
        if (dataNasteriiInput.value !== "") {
            dataNasteriiInput.classList.add("changed");
        } else {
            dataNasteriiInput.classList.remove("changed");
        }
    });

});
