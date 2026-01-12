<script lang="ts">
    import '../styles/style.css';
    import '../app.css';
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    import { isCameraPageActive, accessToken } from '../stores';
    import { getCookie } from '$lib/utils';

    // --- Logika Menu ---
    let isMenuExpanded = false;

    function toggleMenu() {
        isMenuExpanded = !isMenuExpanded;
    }

    async function nav(e: MouseEvent, path: string) {
        e.preventDefault();

        // WAŻNE: jeśli przechodzisz do /camera, zamknij mini-stream ZANIM strona /camera odpali swój stream
        if (path === '/camera') {
            isCameraPageActive.set(true);
            videoStreamUrl = null; // wymusi odmontowanie <img> i przerwanie requestu
            isVideoLoading = true;
        }

        await goto(path);
    }

    async function openCamera(e: MouseEvent) {
        e.preventDefault();
        if ($isCameraPageActive) return;
        isCameraPageActive.set(true);
        await goto('/camera');
    }

    async function closeCamera(e: MouseEvent) {
        e.preventDefault();
        e.stopPropagation();
        isCameraPageActive.set(false);
        await goto('/mainpage');
    }

    // --- Logika Kamery (globalny podgląd) ---
    let videoStreamUrl: string | null = null;
    let isVideoLoading = true;
    let imgElement: HTMLImageElement | null = null;

    // NAJPIERW załaduj token w onMount (synchronicznie)
    onMount(() => {
        const token = getCookie('access_token');
        accessToken.set(token);
    });

    // URL zawsze gdy jest token (NIE uzależniaj od isCameraPageActive)
    $: {
        if ($accessToken) {
            videoStreamUrl = `http://127.0.0.1:8000/video/stream?token=${$accessToken}`;
            isVideoLoading = true;
        } else {
            // Wymuś zatrzymanie strumienia jeśli img element istnieje
            if (imgElement) {
                imgElement.src = '';
                imgElement.srcset = '';
                imgElement.removeAttribute('src');

                // Wymuś przeładowanie przeglądarki aby przerwać request
                imgElement.onerror = null;
                imgElement.onload = null;
            }

            // Wyczyść URL - to usunie element <img> z DOM
            videoStreamUrl = null;
            isVideoLoading = true;
        }
    }

    function handleVideoLoad() {
        if (videoStreamUrl) {
            isVideoLoading = false;
        }
    }

    function handleVideoError() {
        isVideoLoading = true;
    }

    // Cleanup przy odmontowaniu komponentu
    onDestroy(() => {
        if (imgElement) {
            imgElement.src = '';
            imgElement.removeAttribute('src');
        }
    });

    onMount(() => {
        // Sprawdź uprawnienia do powiadomień przy starcie
        if (Notification.permission !== 'granted') {
            Notification.requestPermission();
        }

        // Ustaw interwał na 1 godzinę (3600000 ms) - obecnie w twoim kodzie jest 5000ms (5s) do testów
        const workInterval = setInterval(() => {
            showWorkNotification();
        }, 3600000);

        return () => {
            clearInterval(workInterval);
        };
    });

    function showWorkNotification() {
        // Dodany warunek: jeśli brak tokena, nie rób nic
        if (!$accessToken) return;

        if (Notification.permission === 'granted') {
            new Notification('Przerwa w pracy ☕🤎🥯🍪', {
                body: 'Minęła godzina pracy. Czas na krótką przerwę!',
            });
        }
    }
</script>

<style>
    /* --- Style Menu --- */
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

    /* --- Style dla kamery --- */
    .global-camera-preview {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 240px;
        background-color: #000;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        overflow: hidden;
        z-index: 9999;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .global-camera-preview.expanded {
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100vw;
        height: 100vh;
        border-radius: 0;
        border: none;
        cursor: default;
    }

    .global-camera-preview img {
        width: 100%;
        height: auto;
        display: block;
    }

    .global-camera-preview.expanded img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .close-btn {
        position: absolute;
        top: 12px;
        left: 12px;
        z-index: 10000;
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        background: rgba(0, 0, 0, 0.35);
        color: white;
        cursor: pointer;
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 132px;
        width: 100%;
        color: white;
        font-size: 0.8rem;
    }

    .spinner {
        width: 24px;
        height: 24px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
        margin-bottom: 8px;
    }

    .status-indicator {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 10px;
        height: 10px;
        background-color: #28a745;
        border-radius: 50%;
        box-shadow: 0 0 5px #28a745;
    }

    .status-indicator.false {
        background-color: #d10e0e;
        box-shadow: 0 0 5px #a907073e;
    }

    .global-camera-preview.hidden-preview {
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
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

        .global-camera-preview {
            width: 120px;
            bottom: 10px;
            right: 10px;
        }
    }
</style>

<!-- Sidebar Nav -->
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
                <a href="/login" class="menu-item" on:click={(e) => nav(e, '/login')}>
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
                <a href="/mainpage" class="menu-item" on:click={(e) => nav(e, '/mainpage')}>
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
                <a href="/users" class="menu-item" on:click={(e) => nav(e, '/users')}>
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
        </ul>
    </nav>

    <main class="content">
        <slot />
    </main>

    <!-- Global Camera Preview -->
    {#if videoStreamUrl}
        <div
            class="global-camera-preview"
            class:expanded={$isCameraPageActive}
            role="button"
            tabindex="0"
            on:click={openCamera}
        >
            {#if $isCameraPageActive}
                <button class="close-btn" on:click={closeCamera}>Wróć</button>
            {/if}

            {#if isVideoLoading}
                <div class="loading-container">
                    <div class="status-indicator false" title="Kamera nieaktywna"></div>
                    <div class="spinner"></div>
                    <span>Łączenie...</span>
                </div>
            {/if}

            <img
                bind:this={imgElement}
                src={videoStreamUrl}
                alt="Strumień wideo z kamery"
                class:hidden={isVideoLoading}
                on:load={handleVideoLoad}
                on:error={handleVideoError}
            />
        </div>
    {:else}{/if}
</div>
