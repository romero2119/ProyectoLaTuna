document.addEventListener("DOMContentLoaded", () => {

    const passwordInput = document.querySelector(".password-input");
    const togglePassword = document.querySelector(".toggle-password");

    if (passwordInput && togglePassword) {

        togglePassword.addEventListener("click", () => {

            const icon = togglePassword.querySelector("i");

            if (passwordInput.type === "password") {

                passwordInput.type = "text";
                icon.classList.remove("ri-eye-line");
                icon.classList.add("ri-eye-off-line");

            } else {

                passwordInput.type = "password";
                icon.classList.remove("ri-eye-off-line");
                icon.classList.add("ri-eye-line");

            }

        });

    }

});