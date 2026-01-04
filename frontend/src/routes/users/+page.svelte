<script lang="ts">
    import type { PageData } from './$types';

    export let data: PageData;

    interface User {
        id: number;
        name: string;
        email: string;
        created_at: string;
        online_status: boolean;
    }

    $: users = data.users as User[];
</script>

<style>
    .users-page {
        max-width: 1200px;
        margin: 0 auto;
    }

    .page-header {
        text-align: center;
        margin-bottom: var(--spacing-xl);
    }

    .page-header h1 {
        font-size: 2.5rem;
        text-shadow: var(--text-shadow);
        margin-bottom: var(--spacing-sm);
    }

    .page-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    .users-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: var(--spacing-lg);
    }

    .user-card {
        background: rgba(255, 255, 255, 0.05);
        border: var(--border);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        transition: all var(--animation-time) var(--animation-type);
        backdrop-filter: blur(10px);
    }

    .user-card:hover {
        background: rgba(255, 255, 255, 0.1);
        box-shadow: var(--box-shadow-lg);
        transform: translateY(-4px);
    }

    .user-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-lg);
    }

    .user-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #c83279, #8e2de2);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--box-shadow);
    }

    .user-status {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--border-radius-sm);
        font-size: 0.85rem;
        font-weight: var(--font-weight-bold);
    }

    .user-status.online {
        background: rgba(40, 167, 69, 0.2);
        color: var(--success-color);
    }

    .user-status.offline {
        background: rgba(108, 117, 125, 0.2);
        color: rgba(255, 255, 255, 0.6);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    .user-status.online .status-dot {
        background: var(--success-color);
    }

    .user-status.offline .status-dot {
        background: rgba(255, 255, 255, 0.6);
        animation: none;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .user-info h2 {
        font-size: 1.5rem;
        margin-bottom: var(--spacing-md);
        font-weight: var(--font-weight-bold);
    }

    .info-row {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-sm);
        opacity: 0.85;
        font-size: 0.95rem;
    }

    .info-row svg {
        flex-shrink: 0;
        opacity: 0.7;
    }

    @media (max-width: 768px) {
        .users-grid {
            grid-template-columns: 1fr;
        }

        .page-header h1 {
            font-size: 2rem;
        }
    }
</style>

<div class="users-page">
    <header class="page-header">
        <h1>Lista Użytkowników</h1>
        <p>Zarządzaj użytkownikami systemu monitorowania</p>
    </header>

    <div class="users-grid">
        {#each users as user}
            <div class="user-card">
                <div class="user-header">
                    <div class="user-avatar">
                        <svg
                            width="40"
                            height="40"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                            <circle cx="12" cy="7" r="4" />
                        </svg>
                    </div>
                    <div
                        class="user-status"
                        class:online={user.online_status}
                        class:offline={!user.online_status}
                    >
                        <span class="status-dot"></span>
                        <span class="status-text">{user.online_status ? 'Online' : 'Offline'}</span>
                    </div>
                </div>

                <div class="user-info">
                    <h2>{user.name}</h2>
                    <div class="info-row">
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <path
                                d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                            />
                            <polyline points="22,6 12,13 2,6" />
                        </svg>
                        <span>{user.email}</span>
                    </div>
                    <div class="info-row">
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                            <line x1="16" y1="2" x2="16" y2="6" />
                            <line x1="8" y1="2" x2="8" y2="6" />
                            <line x1="3" y1="10" x2="21" y2="10" />
                        </svg>
                        <span>Dołączył: {user.created_at}</span>
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
