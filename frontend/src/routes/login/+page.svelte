<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount, onDestroy } from 'svelte';
    import { get } from 'svelte/store';
    import { accessToken, stopCamera } from '../../stores';
    import { getCookie } from '$lib/utils';

    let activeTab: 'login' | 'register' = 'login';
    let errorMessage = '';
    let successMessage = '';

    let email = '';
    let password = '';

    let regName = '';
    let regEmail = '';
    let regPassword = '';
    let regConfirmPassword = '';

    let isLoggedIn = false;
    let loggedUserEmail = '';

    function switchTab(tab: 'login' | 'register') {
        activeTab = tab;
        errorMessage = '';
        successMessage = ''; 
    }

    async function handleLogin() {
        errorMessage = '';
        successMessage = ''; 
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();

                document.cookie = 'access_token=; path=/; max-age=0; SameSite=Lax';
                document.cookie = 'access_token=; max-age=0; SameSite=Lax';
                document.cookie = `access_token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;
                accessToken.set(data.access_token);

                await goto('/mainpage');
            } else {
                const errorData = await response.json();
                errorMessage = errorData.detail || 'Błąd logowania';
            }
        } catch (e) {
            console.error(e);
            errorMessage = 'Nie można połączyć się z serwerem.';
        }
    }

    async function handleRegister() {
        errorMessage = '';
        successMessage = '';

        if (regPassword !== regConfirmPassword) {
            errorMessage = 'Hasła nie są identyczne.';
            return;
        }

        const parts = regName.trim().split(' ');
        const firstName = parts[0];
        const lastName = parts.length > 1 ? parts.slice(1).join(' ') : 'Brak';

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: regEmail,
                    password: regPassword,
                    name: firstName,
                    surname: lastName,
                    online_status: false,
                }),
            });

            if (response.ok) {
                switchTab('login');
                successMessage = 'Konto utworzone pomyślnie! Możesz się zalogować.';
            } else {
                const errorData = await response.json();
                errorMessage = errorData.detail || 'Błąd rejestracji';
            }
        } catch (e) {
            console.error(e);
            errorMessage = 'Nie można połączyć się z serwerem.';
        }
    }

    async function handleLogout() {
        const token = getCookie('access_token');

        if (token) {
            try {
                const response = await fetch('http://127.0.0.1:8000/auth/logout', {
                    method: 'POST',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    console.warn(`Błąd wylogowania na serwerze: Status ${response.status}`);
                } else {
                    console.log('✅ Status online_status zaktualizowany w bazie.');
                }
            } catch (e) {
                console.error('Błąd połączenia z backendem podczas wylogowywania:', e);
            }
        }

        document.cookie = 'access_token=; path=/; max-age=0; SameSite=Lax';

        stopCamera();

        isLoggedIn = false;
        loggedUserEmail = '';
        activeTab = 'login';
        successMessage = '';
        errorMessage = '';

        console.log('✅ Wylogowanie zakończone');
    }

    function handleBeforeUnload() {
        const token = getCookie('access_token');
        if (token && isLoggedIn) {
            const blob = new Blob([JSON.stringify({})], { type: 'application/json' });
            navigator.sendBeacon('http://127.0.0.1:8000/auth/logout-beacon?token=' + token, blob);
        }
    }

    onMount(() => {
        checkLoginStatus();
        window.addEventListener('beforeunload', handleBeforeUnload);
    });

    onDestroy(() => {
        if (typeof window !== 'undefined') {
            window.removeEventListener('beforeunload', handleBeforeUnload);
        }
    });

    function checkLoginStatus() {
        const token = get(accessToken) || getCookie('access_token');

        if (token) {
            try {
                const base64Url = token.split('.')[1];
                const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                const jsonPayload = decodeURIComponent(
                    window
                        .atob(base64)
                        .split('')
                        .map(function (c) {
                            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                        })
                        .join('')
                );

                const payload = JSON.parse(jsonPayload);

                const now = Math.floor(Date.now() / 1000);
                if (payload.exp && payload.exp > now) {
                    loggedUserEmail = payload.sub || 'Użytkownik';
                    isLoggedIn = true;
                    accessToken.set(token);
                } else {
                    console.warn('Token wygasł - czyszczenie sesji');
                    document.cookie = 'access_token=; path=/; max-age=0; SameSite=Lax';
                    accessToken.set(null);
                    isLoggedIn = false;
                    loggedUserEmail = '';
                }
            } catch (e) {
                console.error('Błąd tokena:', e);
                document.cookie = 'access_token=; path=/; max-age=0; SameSite=Lax';
                accessToken.set(null);
                isLoggedIn = false;
                loggedUserEmail = '';
            }
        } else {
            accessToken.set(null);
            isLoggedIn = false;
            loggedUserEmail = '';
        }
    }
</script>

<style>
    .login-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        width: 100%;
        padding: var(--spacing-md);
    }

    .login-card {
        background: rgba(36, 11, 54, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-lg);
        padding: var(--spacing-xl);
        width: 100%;
        max-width: 480px;
    }

    .card-header {
        text-align: center;
        margin-bottom: var(--spacing-xl);
    }

    .card-header h1 {
        font-size: 2rem;
        text-shadow: var(--text-shadow);
        margin-bottom: var(--spacing-sm);
    }

    .card-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: var(--spacing-xs);
    }

    .tabs {
        display: flex;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-lg);
        background: rgba(0, 0, 0, 0.2);
        padding: var(--spacing-xs);
        border-radius: var(--border-radius-sm);
    }

    .tab {
        flex: 1;
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: var(--border-radius-sm);
        transition: all var(--animation-time) var(--animation-type);
        font-weight: var(--font-weight-normal);
        opacity: 0.7;
        cursor: pointer;
        color: var(--text-color);
        background: transparent;
        border: none;
    }

    .tab:hover {
        opacity: 1;
        background: rgba(255, 255, 255, 0.05);
    }

    .tab.active {
        background: linear-gradient(45deg, #c83279, #8e2de2);
        opacity: 1;
        font-weight: var(--font-weight-bold);
        box-shadow: var(--box-shadow);
    }

    .form {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .form-group label {
        font-weight: var(--font-weight-bold);
        font-size: 0.9rem;
        opacity: 0.9;
    }

    .form-group input {
        padding: var(--spacing-md);
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius-sm);
        color: var(--text-color);
        font-size: 1rem;
        transition: all var(--animation-time) var(--animation-type);
    }

    .form-group input::placeholder {
        color: rgba(255, 255, 255, 0.4);
    }

    .form-group input:focus {
        outline: none;
        border-color: #c83279;
        background: rgba(0, 0, 0, 0.4);
        box-shadow: 0 0 10px rgba(200, 50, 121, 0.3);
    }

    .submit-button {
        padding: var(--spacing-md) var(--spacing-xl);
        font-size: 1.1rem;
        font-weight: var(--font-weight-bold);
        color: var(--text-color);
        background: linear-gradient(45deg, #c83279, #8e2de2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius-sm);
        box-shadow: var(--box-shadow-lg);
        transition: all var(--animation-time) ease;
        margin-top: var(--spacing-sm);
        text-align: center;
        cursor: pointer;
    }

    .submit-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(200, 50, 121, 0.7);
    }

    .error-msg {
        color: #ff4d4d;
        text-align: center;
        background: rgba(255, 0, 0, 0.1);
        padding: 10px;
        border-radius: 4px;
        border: 1px solid rgba(255, 0, 0, 0.3);
    }

    .success-msg {
        color: #28a745;
        text-align: center;
        background: rgba(40, 167, 69, 0.1);
        padding: 10px;
        border-radius: 4px;
        border: 1px solid rgba(40, 167, 69, 0.3);
    }

    .logged-in-view {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-top: var(--spacing-lg);
        width: 100%;
        text-align: center;
        align-items: center;
    }

    .user-email {
        font-size: 1.2rem;
        font-weight: var(--font-weight-bold);
        color: #c83279;
    }

    .logout-button {
        padding: var(--spacing-md) var(--spacing-xl);
        font-size: 1rem;
        font-weight: var(--font-weight-bold);
        color: #fff;
        background: #e63946;
        border: none;
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        transition: background 0.3s ease;
        width: 100%;
    }

    @media (max-width: 640px) {
        .login-card {
            padding: var(--spacing-lg);
        }

        .card-header h1 {
            font-size: 1.75rem;
        }
    }
</style>

<div class="login-container">
    <div class="login-card">
        {#if isLoggedIn}
            <header class="card-header">
                <h1>Witaj ponownie!</h1>
                <p>Jesteś już zalogowany jako:</p>
            </header>

            <div class="logged-in-view">
                <div class="user-email">
                    {loggedUserEmail}
                </div>

                <button class="submit-button" on:click={() => goto('/mainpage')}>
                    Przejdź do Panelu
                </button>

                <button class="logout-button" on:click={handleLogout}> Wyloguj się </button>
            </div>
        {:else}
            <header class="card-header">
                <h1>Zaloguj się lub utwórz nowe konto</h1>
            </header>

            <div class="tabs">
                <button
                    class="tab"
                    class:active={activeTab === 'login'}
                    on:click={() => switchTab('login')}
                >
                    Logowanie
                </button>
                <button
                    class="tab"
                    class:active={activeTab === 'register'}
                    on:click={() => switchTab('register')}
                >
                    Rejestracja
                </button>
            </div>

            {#if errorMessage}
                <div class="error-msg">{errorMessage}</div>
            {/if}

            {#if successMessage}
                <div class="success-msg">{successMessage}</div>
            {/if}

            {#if activeTab === 'login'}
                <form class="form" on:submit|preventDefault={handleLogin}>
                    <div class="form-group">
                        <label for="login-email">Adres email</label>
                        <input
                            type="email"
                            id="login-email"
                            placeholder="twoj@email.com"
                            autocomplete="email"
                            required
                            bind:value={email}
                        />
                    </div>

                    <div class="form-group">
                        <label for="login-password">Hasło</label>
                        <input
                            type="password"
                            id="login-password"
                            placeholder="••••••••"
                            autocomplete="current-password"
                            required
                            bind:value={password}
                        />
                    </div>

                    <button type="submit" class="submit-button"> Zaloguj się </button>
                </form>
            {:else}
                <form class="form" on:submit|preventDefault={handleRegister}>
                    <div class="form-group">
                        <label for="register-name">Imię i nazwisko</label>
                        <input
                            type="text"
                            id="register-name"
                            placeholder="Jan Kowalski"
                            autocomplete="name"
                            required
                            bind:value={regName}
                        />
                    </div>

                    <div class="form-group">
                        <label for="register-email">Adres email</label>
                        <input
                            type="email"
                            id="register-email"
                            placeholder="twoj@email.com"
                            autocomplete="email"
                            required
                            bind:value={regEmail}
                        />
                    </div>

                    <div class="form-group">
                        <label for="register-password">Hasło</label>
                        <input
                            type="password"
                            id="register-password"
                            placeholder="••••••••"
                            autocomplete="new-password"
                            required
                            bind:value={regPassword}
                        />
                    </div>

                    <div class="form-group">
                        <label for="register-password-confirm">Potwierdź hasło</label>
                        <input
                            type="password"
                            id="register-password-confirm"
                            placeholder="••••••••"
                            autocomplete="new-password"
                            required
                            bind:value={regConfirmPassword}
                        />
                    </div>

                    <button type="submit" class="submit-button"> Utwórz konto </button>
                </form>
            {/if}
        {/if}
    </div>
</div>
