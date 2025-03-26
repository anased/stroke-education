// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.querySelector('form');
    const strokeTypeSelect = document.querySelector('select[name="stroke_type"]');
    const riskFactorsSelect = document.querySelector('select[name="risk_factors"]');

    if (form) {
        form.addEventListener('submit', function(e) {
            if (!strokeTypeSelect.value) {
                e.preventDefault();
                alert('Please select a stroke type');
                return;
            }
        });
    }

    // Enhanced multiple select functionality
    if (riskFactorsSelect) {
        // Add "Select All" option
        const selectAllOption = document.createElement('button');
        selectAllOption.type = 'button';
        selectAllOption.className = 'btn btn-secondary btn-sm';
        selectAllOption.style.marginBottom = '0.5rem';
        selectAllOption.textContent = 'Select All Risk Factors';
        
        selectAllOption.addEventListener('click', function() {
            const options = riskFactorsSelect.options;
            for (let i = 0; i < options.length; i++) {
                options[i].selected = true;
            }
        });

        riskFactorsSelect.parentNode.insertBefore(selectAllOption, riskFactorsSelect);

        // Add "Clear All" option
        const clearAllOption = document.createElement('button');
        clearAllOption.type = 'button';
        clearAllOption.className = 'btn btn-secondary btn-sm';
        clearAllOption.style.marginBottom = '0.5rem';
        clearAllOption.style.marginLeft = '0.5rem';
        clearAllOption.textContent = 'Clear All';
        
        clearAllOption.addEventListener('click', function() {
            const options = riskFactorsSelect.options;
            for (let i = 0; i < options.length; i++) {
                options[i].selected = false;
            }
        });

        selectAllOption.parentNode.insertBefore(clearAllOption, riskFactorsSelect);
    }

    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Print functionality
    const printButton = document.createElement('button');
    printButton.type = 'button';
    printButton.className = 'btn btn-secondary';
    printButton.textContent = 'Print Education Information';
    printButton.addEventListener('click', function() {
        window.print();
    });

    const educationResults = document.querySelector('.education-results');
    if (educationResults) {
        educationResults.insertBefore(printButton, educationResults.firstChild);
    }
});