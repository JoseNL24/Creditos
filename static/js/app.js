document.addEventListener('DOMContentLoaded', function() {

    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            const fechaInput = form.querySelector('input[type="date"]');
            if (fechaInput && !isValidDate(fechaInput.value)) {
                isValid = false;
                fechaInput.classList.add('is-invalid');
            }
            
            if (!isValid) {
                event.preventDefault();
                alert('Por favor complete todos los campos requeridos correctamente.');
            }
        });
    });
    
    function isValidDate(dateString) {
        const regEx = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateString.match(regEx)) return false;
        
        const d = new Date(dateString);
        if (Number.isNaN(d.getTime())) return false;
        
        return d.toISOString().slice(0,10) === dateString;
    }
});