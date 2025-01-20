document.addEventListener('DOMContentLoaded', function () {
            const passwordField = document.getElementById('registerPassword');
            const confirmPasswordField = document.getElementById('confirmPassword');
            const message = document.getElementById('passwordMatchMessage');

            function checkPasswords() {
                const password = passwordField.value;
                const confirmPassword = confirmPasswordField.value;

                if (confirmPassword === '') {
                    message.textContent = '';
                    passwordField.classList.remove('match', 'no-match');
                    confirmPasswordField.classList.remove('match', 'no-match');
                    return;
                }

                if (password === confirmPassword) {
                    message.textContent = 'Passwords match!';
                    message.style.color = 'green';
                    passwordField.classList.add('match');
                    passwordField.classList.remove('no-match');
                    confirmPasswordField.classList.add('match');
                    confirmPasswordField.classList.remove('no-match');
                } else {
                    message.textContent = 'Passwords do not match!';
                    message.style.color = 'red';
                    passwordField.classList.add('no-match');
                    passwordField.classList.remove('match');
                    confirmPasswordField.classList.add('no-match');
                    confirmPasswordField.classList.remove('match');
                }
            }

            passwordField.addEventListener('input', checkPasswords);
            confirmPasswordField.addEventListener('input', checkPasswords);
        });