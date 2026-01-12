/* static/js/scripts.js - WERSJA POPRAWIONA (Strefy czasowe + Auto-start) */

document.addEventListener('DOMContentLoaded', function() {

    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');
    const insuranceInput = document.getElementById('id_insurance_accepted');
    const carIdElement = document.getElementById('car-id-hidden');
    const costDisplay = document.getElementById('total-cost-display');
    const form = document.querySelector('form');

    // Funkcja pomocnicza: Tworzy datę lokalną z napisu "YYYY-MM-DD"
    // Rozwiązuje problem, gdzie "dziś" było uznawane za "wczoraj" przez strefy czasowe
    function parseDate(dateString) {
        if (!dateString) return null;
        const parts = dateString.split('-');
        // new Date(rok, miesiąc-1, dzień) tworzy datę lokalną 00:00:00
        return new Date(parts[0], parts[1] - 1, parts[2]);
    }

    // Funkcja pomocnicza: Zwraca dzisiejszą datę lokalną z wyzerowaną godziną
    function getToday() {
        const d = new Date();
        d.setHours(0, 0, 0, 0);
        return d;
    }

    function setStatus(type, message) {
        if (!costDisplay) return;

        costDisplay.className = 'alert fw-bold';
        if (type === 'error') {
            costDisplay.classList.add('alert-danger');
            costDisplay.style.color = '#dc3545';
        } else if (type === 'success') {
            costDisplay.classList.add('alert-success');
            costDisplay.style.color = '#198754';
        } else {
            costDisplay.classList.add('alert-secondary');
            costDisplay.style.color = 'black';
        }
        costDisplay.innerHTML = message;
    }

    if (startDateInput && endDateInput && carIdElement) {

        function updateCost() {
            const startVal = startDateInput.value;
            const endVal = endDateInput.value;
            const carId = carIdElement.value;

            // 1. Brak dat -> Tekst domyślny
            if (!startVal || !endVal) {
                setStatus('neutral', 'Wybierz termin rezerwacji');
                return;
            }

            const start = parseDate(startVal);
            const end = parseDate(endVal);
            const today = getToday();

            // 2. Walidacja logiczna (JS)
            // Używamy getTime(), żeby bezpiecznie porównać daty
            if (start.getTime() < today.getTime()) {
                setStatus('error', 'Data odbioru nie może być z przeszłości!');
                return;
            }

            if (end.getTime() <= start.getTime()) {
                setStatus('error', 'Data zwrotu musi być późniejsza niż odbioru!');
                return;
            }

            // 3. Pobieranie ceny z API
            fetch(`/api/cars/${carId}/`)
                .then(response => response.json())
                .then(data => {
                    const pricePerDay = parseFloat(data.price_per_day);

                    const timeDiff = end - start;
                    const days = Math.ceil(timeDiff / (1000 * 3600 * 24));

                    let total = days * pricePerDay;

                    if (insuranceInput && insuranceInput.checked) {
                        total += 50;
                    }

                    setStatus('success', `Szacowany koszt: ${total.toFixed(2)} PLN`);
                })
                .catch(error => {
                    console.error(error);
                    setStatus('error', 'Błąd połączenia z serwerem.');
                });
        }

        // Podpinamy zdarzenia
        startDateInput.addEventListener('change', updateCost);
        endDateInput.addEventListener('change', updateCost);
        if (insuranceInput) insuranceInput.addEventListener('change', updateCost);

        // KLUCZOWE: Uruchamiamy obliczanie od razu po załadowaniu strony
        // Dzięki temu, jak strona się przeładuje z błędami, JS od razu pokaże cenę/błąd
        updateCost();
    }

    // Walidacja przed wysłaniem (blokada formularza)
    if (form) {
        form.addEventListener('submit', function(event) {
            const startVal = startDateInput.value;
            const endVal = endDateInput.value;

            if (startVal && endVal) {
                const start = parseDate(startVal);
                const end = parseDate(endVal);
                const today = getToday();

                if (start.getTime() < today.getTime() || end.getTime() <= start.getTime()) {
                    event.preventDefault();
                    alert("Popraw błędy w datach przed wysłaniem!");
                }
            } else {
                event.preventDefault();
                alert("Uzupełnij obie daty!");
            }
        });
    }
});