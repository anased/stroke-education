// static/js/multi-step-form.js
document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-hide
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Risk factors selection limit
    const riskFactorsSelect = document.querySelector('select[name="risk_factors"]');
    if (riskFactorsSelect) {
        // Add selection counter
        const selectionCounter = document.createElement('div');
        selectionCounter.className = 'selection-counter';
        selectionCounter.innerHTML = 'Selected: <span>0</span>/3';
        riskFactorsSelect.parentNode.insertBefore(selectionCounter, riskFactorsSelect.nextSibling);
        
        const counterSpan = selectionCounter.querySelector('span');
        
        // Update counter and limit selections
        riskFactorsSelect.addEventListener('change', function() {
            const selectedOptions = Array.from(this.selectedOptions);
            counterSpan.textContent = selectedOptions.length;
            
            if (selectedOptions.length > 3) {
                // Deselect the last selected option
                const lastIndex = selectedOptions.length - 1;
                selectedOptions[lastIndex].selected = false;
                
                // Update counter
                counterSpan.textContent = "3";
                
                // Show warning
                alert('Please select up to three risk factors');
            }
        });
        
        // Add helper buttons
        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'selection-buttons';
        
        const clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'btn btn-sm btn-secondary';
        clearBtn.textContent = 'Clear Selection';
        
        clearBtn.addEventListener('click', function() {
            const options = riskFactorsSelect.options;
            for (let i = 0; i < options.length; i++) {
                options[i].selected = false;
            }
            counterSpan.textContent = "0";
        });
        
        buttonsContainer.appendChild(clearBtn);
        riskFactorsSelect.parentNode.insertBefore(buttonsContainer, riskFactorsSelect.nextSibling);
    }
    
    // Date of birth validation
    const dateOfBirthInput = document.querySelector('input[name="date_of_birth"]');
    if (dateOfBirthInput) {
        // Set max date to today
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateOfBirthInput.max = `${year}-${month}-${day}`;
    }
    
    // Print functionality for education page
    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
});