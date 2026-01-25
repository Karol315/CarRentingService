document.addEventListener("DOMContentLoaded", function () {

    const passwordFields = document.querySelectorAll('input[type="password"]');
    const passRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

    passwordFields.forEach(field => {
        field.addEventListener('blur', function() {
            const errorSpan = document.getElementById(field.id + '_error');

            if (field.name === 'password_repeat') return;

            if (field.value && !passRegex.test(field.value)) {
                if(errorSpan) errorSpan.textContent = "Hasło: min 8 znaków, litera, cyfra, znak specjalny.";
            } else {
                if(errorSpan) errorSpan.textContent = "";
            }
        });
    });

    const pass1 = document.getElementById("id_password");
    const pass2 = document.getElementById("id_password_repeat");

    if (pass1 && pass2) {
        pass2.addEventListener('blur', function() {
            const errorSpan = document.getElementById(pass2.id + '_error');
            if (pass1.value !== pass2.value) {
                if(errorSpan) errorSpan.textContent = "Hasła muszą być identyczne!";
            } else {
                if(errorSpan) errorSpan.textContent = "";
            }
        });
    }

    const emailField = document.getElementById("id_email");
    if (emailField) {
        emailField.addEventListener('input', function() {
            const errorSpan = document.getElementById(emailField.id + '_error');
            if(errorSpan) errorSpan.textContent = "";
        });
    }
});