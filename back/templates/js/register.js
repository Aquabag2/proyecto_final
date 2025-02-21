document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('.register-form');
    const passwordInput = document.querySelector('input[name="password"]');
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
    const togglePassword = document.querySelector('.toggle-password');

    // Toggle password visibility
    if (togglePassword) {
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
            const email = document.querySelector('input[name="email"]').value;
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;

            if (!email || !password || !confirmPassword) {
                e.preventDefault();
                showAlert('Por favor completa todos los campos', 'error');
                return;
            }

            if (password !== confirmPassword) {
                e.preventDefault();
                showAlert('Las contraseñas no coinciden', 'error');
                return;
            }
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
}); 