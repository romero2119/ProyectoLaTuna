document.addEventListener("DOMContentLoaded", () => {

    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");

    if (!password1) return;

    const strengthFill = document.getElementById("strength-fill");
    const strengthText = document.getElementById("strength-text");
    const submitBtn = document.getElementById("submit-btn");
    const matchMessage = document.getElementById("match-message");

    const reqLength = document.getElementById("req-length");
    const reqLetter = document.getElementById("req-letter");
    const reqNumber = document.getElementById("req-number");
    const reqSpecial = document.getElementById("req-special");

    /*==============================
        MOSTRAR / OCULTAR PASSWORD
    ==============================*/

    document.querySelectorAll(".toggle-password").forEach(toggle => {

        toggle.addEventListener("click", () => {

            const target = document.getElementById(toggle.dataset.target);

            const icon = toggle.querySelector("i");

            if (target.type === "password") {

                target.type = "text";

                icon.classList.remove("ri-eye-line");
                icon.classList.add("ri-eye-off-line");

            } else {

                target.type = "password";

                icon.classList.remove("ri-eye-off-line");
                icon.classList.add("ri-eye-line");

            }

        });

    });

    /*==============================
            VALIDACIONES
    ==============================*/

    function validarPassword() {

        const value = password1.value;

        let score = 0;

        const lengthOK = value.length >= 8;
        const letterOK = /[A-Za-z]/.test(value);
        const numberOK = /[0-9]/.test(value);
        const specialOK = /[^A-Za-z0-9]/.test(value);

        actualizarRequisito(reqLength, lengthOK);
        actualizarRequisito(reqLetter, letterOK);
        actualizarRequisito(reqNumber, numberOK);
        actualizarRequisito(reqSpecial, specialOK);

        if (lengthOK) score++;
        if (letterOK) score++;
        if (numberOK) score++;
        if (specialOK) score++;

        switch (score) {

            case 0:

                strengthFill.style.width = "0%";
                strengthFill.style.background = "#ccc";
                strengthText.innerHTML = "Escribe una contraseña";

                break;

            case 1:

                strengthFill.style.width = "25%";
                strengthFill.style.background = "#ff4d4d";
                strengthText.innerHTML = "Muy débil";

                break;

            case 2:

                strengthFill.style.width = "50%";
                strengthFill.style.background = "#ff9800";
                strengthText.innerHTML = "Media";

                break;

            case 3:

                strengthFill.style.width = "75%";
                strengthFill.style.background = "#9acd32";
                strengthText.innerHTML = "Buena";

                break;

            case 4:

                strengthFill.style.width = "100%";
                strengthFill.style.background = "#107E38";
                strengthText.innerHTML = "Muy segura";

                break;

        }

        validarCoincidencia();

    }

    /*==============================
        ACTUALIZAR REQUISITOS
    ==============================*/

    function actualizarRequisito(elemento, valido) {

        const icon = elemento.querySelector("i");

        if (valido) {

            elemento.classList.add("valid");

            icon.classList.remove("ri-checkbox-blank-circle-line");

            icon.classList.add("ri-checkbox-circle-fill");

        } else {

            elemento.classList.remove("valid");

            icon.classList.remove("ri-checkbox-circle-fill");

            icon.classList.add("ri-checkbox-blank-circle-line");

        }

    }

    /*==============================
        CONFIRMAR CONTRASEÑA
    ==============================*/

    function validarCoincidencia() {

        if (!password2) return;

        if (password2.value.length === 0) {

            matchMessage.innerHTML = "";

            submitBtn.disabled = true;

            submitBtn.style.opacity = ".6";

            return;

        }

        if (password1.value === password2.value) {

            matchMessage.innerHTML =
                "Las contraseñas coinciden";

            matchMessage.style.color = "#107E38";

            submitBtn.disabled = false;

            submitBtn.style.opacity = "1";

        } else {

            matchMessage.innerHTML =
                "Las contraseñas no coinciden";

            matchMessage.style.color = "#d62828";

            submitBtn.disabled = true;

            submitBtn.style.opacity = ".6";

        }

    }

    /*==============================
            EVENTOS
    ==============================*/

    password1.addEventListener("input", validarPassword);

    if (password2) {

        password2.addEventListener("input", validarCoincidencia);

    }

    submitBtn.disabled = true;

    submitBtn.style.opacity = ".6";

});