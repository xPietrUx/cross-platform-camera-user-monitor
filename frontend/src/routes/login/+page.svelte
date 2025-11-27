<script lang="ts">
    let activeTab: 'login' | 'register' = 'login';

    function switchTab(tab: 'login' | 'register') {
        activeTab = tab;
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

    .form-options {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: var(--spacing-sm);
        font-size: 0.9rem;
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        cursor: pointer;
        user-select: none;
    }

    .checkbox-label input[type='checkbox'] {
        width: 18px;
        height: 18px;
        cursor: pointer;
        accent-color: #c83279;
    }

    .link {
        color: #c83279;
        text-decoration: none;
        transition: opacity var(--animation-time);
    }

    .link:hover {
        opacity: 0.8;
        text-decoration: underline;
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
    }

    .submit-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(200, 50, 121, 0.7);
    }

    @media (max-width: 640px) {
        .login-card {
            padding: var(--spacing-lg);
        }

        .card-header h1 {
            font-size: 1.75rem;
        }

        .form-options {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>

<div class="login-container">
    <div class="login-card">
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

        {#if activeTab === 'login'}
            <form class="form">
                <div class="form-group">
                    <label for="login-email">Adres email</label>
                    <input
                        type="email"
                        id="login-email"
                        placeholder="twoj@email.com"
                        autocomplete="email"
                    />
                </div>

                <div class="form-group">
                    <label for="login-password">Hasło</label>
                    <input
                        type="password"
                        id="login-password"
                        placeholder="••••••••"
                        autocomplete="current-password"
                    />
                </div>

                <button type="submit" class="submit-button"> Zaloguj się </button>
            </form>
        {:else}
            <form class="form">
                <div class="form-group">
                    <label for="register-name">Imię i nazwisko</label>
                    <input
                        type="text"
                        id="register-name"
                        placeholder="Jan Kowalski"
                        autocomplete="name"
                    />
                </div>

                <div class="form-group">
                    <label for="register-email">Adres email</label>
                    <input
                        type="email"
                        id="register-email"
                        placeholder="twoj@email.com"
                        autocomplete="email"
                    />
                </div>

                <div class="form-group">
                    <label for="register-password">Hasło</label>
                    <input
                        type="password"
                        id="register-password"
                        placeholder="••••••••"
                        autocomplete="new-password"
                    />
                </div>

                <div class="form-group">
                    <label for="register-password-confirm">Potwierdź hasło</label>
                    <input
                        type="password"
                        id="register-password-confirm"
                        placeholder="••••••••"
                        autocomplete="new-password"
                    />
                </div>

                <button type="submit" class="submit-button"> Utwórz konto </button>
            </form>
        {/if}
    </div>
</div>
