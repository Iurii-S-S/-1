// Конфигурация API
const API_BASE = 'http://localhost:5000';

// Простое приложение для входа
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorDiv = document.getElementById('error');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const submitBtn = document.querySelector('button[type="submit"]');
            
            // Показываем индикатор загрузки
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Вход...';
            
            try {
                const response = await fetch(API_BASE + '/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Сохраняем данные пользователя
                    localStorage.setItem('currentUser', JSON.stringify(data.user));
                    localStorage.setItem('authToken', 'authenticated');
                    
                    // Перенаправляем на дашборд
                    window.location.href = 'dashboard.html';
                } else {
                    errorDiv.textContent = data.error || 'Ошибка авторизации';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Ошибка соединения с сервером';
                errorDiv.style.display = 'block';
                console.error('Login error:', error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Войти';
            }
        });
    }
    
    // Проверяем авторизацию на других страницах
    if (!window.location.pathname.includes('index.html')) {
        const currentUser = localStorage.getItem('currentUser');
        if (!currentUser) {
            window.location.href = 'index.html';
        }
    }
});