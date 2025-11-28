<script lang="ts">
    import '../styles/style.css';
    import '../app.css'; // Upewnij się, że ten import istnieje
    import { page } from '$app/stores';
    let isMenuExpanded = false;

    function toggleMenu() {
        isMenuExpanded = !isMenuExpanded;
    }
</script>

<style>
    .layout {
        display: flex;
        min-height: 100vh;
        width: 100%;
    }

    .sidebar {
        background-color: rgba(36, 11, 54, 0.95);
        width: 250px;
        min-height: 100vh;
        padding: var(--spacing-md);
        border-right: var(--border);
        transition: width var(--animation-time) var(--animation-type);
        position: relative;
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    .sidebar.collapsed {
        width: 80px;
    }

    .toggle-btn {
        position: absolute;
        top: var(--spacing-md);
        right: calc(var(--spacing-md) * -0.5);
        background-color: rgba(36, 11, 54, 0.95);
        border: var(--border);
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform var(--animation-time) var(--animation-type);
        z-index: 10;
    }

    .toggle-btn:hover {
        transform: scale(1.1);
    }

    .menu-list {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
        margin-top: var(--spacing-xl);
    }

    .menu-item {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: var(--border-radius-sm);
        transition: background-color var(--animation-time) var(--animation-type);
        white-space: nowrap;
        overflow: hidden;
    }

    .sidebar.collapsed .menu-item {
        justify-content: center;
        padding: var(--spacing-sm);
    }

    .menu-item:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .menu-item.active {
        background-color: rgba(255, 255, 255, 0.15);
        font-weight: var(--font-weight-bold);
    }

    .menu-icon {
        flex-shrink: 0;
    }

    .menu-item span {
        transition: opacity var(--animation-time) var(--animation-type);
    }

    .sidebar.collapsed .menu-item span {
        opacity: 0;
        width: 0;
        overflow: hidden;
    }

    .content {
        flex: 1;
        padding: var(--spacing-xl);
        overflow-x: hidden;
    }

    @media (max-width: 768px) {
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            z-index: 100;
            box-shadow: var(--box-shadow-lg);
        }

        .sidebar.collapsed {
            width: 0;
            padding: 0;
            border: none;
        }

        .content {
            margin-left: 0;
            padding: var(--spacing-md);
        }
    }
</style>

<div class="layout">
    <nav class="sidebar" class:collapsed={!isMenuExpanded}>
        <button class="toggle-btn" on:click={toggleMenu} aria-label="Przełącz menu">
            <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
            >
                {#if isMenuExpanded}
                    <path d="M15 18l-6-6 6-6" />
                {:else}
                    <path d="M9 18l6-6-6-6" />
                {/if}
            </svg>
        </button>

        <ul class="menu-list">
            <li>
                <a href="/login" class="menu-item">
                    <svg
                        class="menu-icon"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                        <polyline points="10 17 15 12 10 7" />
                        <line x1="15" y1="12" x2="3" y2="12" />
                    </svg>
                    {#if isMenuExpanded}
                        <span>Logowanie</span>
                    {/if}
                </a>
            </li>
            <li>
                <a href="/" class="menu-item">
                    <svg
                        class="menu-icon"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                        <polyline points="9 22 9 12 15 12 15 22" />
                    </svg>
                    {#if isMenuExpanded}
                        <span>Strona Główna</span>
                    {/if}
                </a>
            </li>
            <li>
                <a href="/users" class="menu-item">
                    <svg
                        class="menu-icon"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                        <circle cx="9" cy="7" r="4" />
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                    </svg>
                    {#if isMenuExpanded}
                        <span>Lista użytkowników</span>
                    {/if}
                </a>
            </li>
            <li>
                <a href="/camera" class="menu-item">
                    <svg
                        class="menu-icon"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"
                        />
                        <circle cx="12" cy="13" r="4" />
                    </svg>
                    {#if isMenuExpanded}
                        <span>Podgląd kamery</span>
                    {/if}
                </a>
            </li>
        </ul>
    </nav>

    <main class="content">
        <slot />
    </main>
</div>
