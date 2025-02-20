document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('.register-form');
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('input[name="password"]');
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');

    // Toggle password visibility
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            confirmPasswordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Form validation
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.querySelector('input[name="email"]').value;
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            const terms = document.querySelector('input[name="terms"]').checked;

            // Validaciones
            if (!email || !password || !confirmPassword) {
                showAlert('Por favor completa todos los campos', 'error');
                return;
            }

            if (password !== confirmPassword) {
                showAlert('Las contraseñas no coinciden', 'error');
                return;
            }

            if (!terms) {
                showAlert('Debes aceptar los términos y condiciones', 'error');
                return;
            }

            // Si todo está bien, enviar el formulario
            this.submit();
        });
    }

    // Alert function
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        const registerHeader = document.querySelector('.register-header');
        registerHeader.insertAdjacentElement('afterend', alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    // Animate register button
    const registerButton = document.querySelector('.register-button');
    if (registerButton) {
        registerButton.addEventListener('mouseenter', function() {
            this.querySelector('i').style.transform = 'translateX(5px)';
        });

        registerButton.addEventListener('mouseleave', function() {
            this.querySelector('i').style.transform = 'translateX(0)';
        });
    }
}); 