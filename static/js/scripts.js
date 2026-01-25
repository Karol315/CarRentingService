document.addEventListener("DOMContentLoaded", function () {
    // 1. Uruchom walidację rezerwacji (jeśli jesteśmy na podstronie rezerwacji)
    initBookingForm();

    // 2. Uruchom walidację rejestracji (jeśli jesteśmy na podstronie rejestracji)
    initRegistrationForm();
});

/**
 * Walidacja Rezerwacji (Ceny, Daty, Kolory)
 */
function initBookingForm() {
    const bookingForm = document.getElementById('booking-form');
    if (!bookingForm) return;

    const startInput = document.getElementById('id_start_date');
    const endInput = document.getElementById('id_end_date');
    const colorInput = document.getElementById('id_car_color');
    const paymentInput = document.getElementById('id_payment_method');
    const insuranceInput = document.getElementById('id_insurance_accepted');

    const costDisplay = document.getElementById('live-cost-display');
    const daysDisplay = document.getElementById('live-days-display');
    const submitBtn = document.getElementById('submit-btn');

    const startError = document.getElementById('start-error');
    const endError = document.getElementById('end-error');
    const colorError = document.getElementById('color-error');
    const paymentError = paymentInput.nextElementSibling;

    const priceDataEl = document.getElementById('car-price-data');
    if (!priceDataEl) return;
    const pricePerDay = parseFloat(priceDataEl.dataset.price.replace(',', '.'));

    // Flagi sprawdzające, czy użytkownik dotknął już pola
    let colorTouched = false;
    let paymentTouched = false;

    function updateState(showAllErrors = false) {
        const startVal = startInput.value;
        const endVal = endInput.value;
        const today = new Date().toISOString().split('T')[0];

        let isValid = true;

        // Reset stanów
        [startInput, endInput, colorInput, paymentInput].forEach(el => el.classList.remove('is-invalid'));
        startError.textContent = "";
        endError.textContent = "";
        colorError.textContent = "";
        if (paymentError) paymentError.textContent = "";

        // 1. Walidacja Dat
        if (startVal && startVal < today) {
            setError(startInput, startError, "Data nie może być z przeszłości.");
            isValid = false;
        }
        if (endVal) {
            if (endVal < today) {
                setError(endInput, endError, "Data nie może być z przeszłości.");
                isValid = false;
            }
            if (startVal && endVal <= startVal) {
                setError(endInput, endError, "Data zwrotu musi być późniejsza niż odbioru.");
                isValid = false;
            }
        } else if (showAllErrors) {
            setError(endInput, endError, "Data zwrotu jest wymagana.");
            isValid = false;
        }

        // 2. Walidacja Koloru
        if (!colorInput.value || colorInput.value === "") {
            if (showAllErrors || colorTouched) {
                setError(colorInput, colorError, "Proszę wybrać wariant auta.");
            }
            isValid = false;
        } else if (colorInput.selectedIndex !== -1) {
            const selectedText = colorInput.options[colorInput.selectedIndex].text;
            if (selectedText.includes("Wolne: 0") || selectedText.includes("niedostępny")) {
                setError(colorInput, colorError, "Ten wariant jest niestety niedostępny.");
                isValid = false;
            }
        }

        // 3. Walidacja Płatności
        if (!paymentInput.value || paymentInput.value === "") {
            if (showAllErrors || paymentTouched) {
                setError(paymentInput, paymentError, "Proszę wybrać metodę płatności.");
            }
            isValid = false;
        }

        // 4. Kalkulacja (tylko gdy daty są poprawne)
        if (startVal && endVal && !startInput.classList.contains('is-invalid') && !endInput.classList.contains('is-invalid')) {
            const d1 = new Date(startVal);
            const d2 = new Date(endVal);
            const diffTime = Math.abs(d2 - d1);
            let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            if (diffDays < 1) diffDays = 1;

            let total = diffDays * pricePerDay;
            if (insuranceInput.checked) total += 50;

            costDisplay.textContent = total.toFixed(2) + " PLN";
            daysDisplay.textContent = "(" + diffDays + " dni)";
        } else {
            costDisplay.textContent = "0.00 PLN";
            daysDisplay.textContent = "(uzupełnij dane)";
        }

        // Przycisk jest zawsze aktywny
        submitBtn.disabled = false;
        return isValid;
    }

    function setError(input, label, msg) {
        input.classList.add('is-invalid');
        if (label) label.textContent = msg;
    }

    // Obsługa kliknięcia "Potwierdź"
    bookingForm.addEventListener('submit', function(e) {
        const formIsValid = updateState(true); // Wymuszamy pokazanie wszystkich błędów
        if (!formIsValid) {
            e.preventDefault(); // Zatrzymujemy wysyłkę jeśli są błędy
        }
    });

    // Listenery "na żywo"
    startInput.addEventListener('input', () => updateState());
    endInput.addEventListener('input', () => updateState());

    colorInput.addEventListener('change', () => {
        colorTouched = true;
        updateState();
    });

    paymentInput.addEventListener('change', () => {
        paymentTouched = true;
        updateState();
    });

    insuranceInput.addEventListener('change', () => updateState());

    // Inicjalizacja bez błędów na starcie
    updateState();
}

function initEditForm() {
    const cancelBtn = document.querySelector('button[name="cancel"]');

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function(e) {
            // Wyświetlamy systemowe potwierdzenie
            const confirmed = confirm("Czy na pewno chcesz anulować tę rezerwację?\n\nTej operacji nie można cofnąć!");

            if (!confirmed) {
                // Jeśli użytkownik kliknie "Anuluj", blokujemy wysłanie formularza
                e.preventDefault();
            }
        });
    }
}

/**
 * Walidacja Rejestracji (Hasła)
 */
function initRegistrationForm() {
    // Zakładamy, że formularz rejestracji ma ID 'signup-form' lub szukamy po polach
    // Django domyślnie generuje id_password1 i id_password1
    const pass1 = document.getElementById('id_password1'); // Hasło
    const pass2 = document.getElementById('id_password1'); // Powtórz hasło (czasem id_password2 w custom formach)

    // Jeśli nie ma pól, to nie rejestracja
    if (!pass1) return;

    // Znajdźmy ewentualne pole powtórzenia (zależy jak nazwałeś w forms.py)
    // Jeśli używasz standardowego UserCreationForm, to pola mają specyficzne ID.
    // Tutaj prosty przykład: walidacja długości hasła "na żywo".

    pass1.addEventListener('input', function() {
        if (pass1.value.length > 0 && pass1.value.length < 8) {
            pass1.classList.add('is-invalid');
            // Jeśli masz placeholder na błąd, możesz go tu wypełnić
        } else {
            pass1.classList.remove('is-invalid');
        }
    });
}