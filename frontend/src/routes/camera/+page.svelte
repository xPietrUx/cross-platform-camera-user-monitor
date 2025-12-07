<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { isCameraPageActive } from '../../stores';

    const videoStreamUrl = 'http://127.0.0.1:8000/video/stream';

    let isLoading = true;

    onMount(() => {
        isCameraPageActive.set(true);
    });

    onDestroy(() => {
        isCameraPageActive.set(false);
    });

    function handleVideoLoad() {
        isLoading = false;
    }
</script>

<style>
    .video-wrapper {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #000;
        border-radius: var(--border-radius);
        position: relative;
        overflow: hidden;
    }

    .video-wrapper img {
        height: 100%;
        width: 100%;
        object-fit: contain;
        border-radius: var(--border-radius);
        transition: opacity 0.3s ease;
    }

    .video-wrapper img.hidden {
        opacity: 0;
    }

    .loader-container {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        color: white;
        gap: 10px;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>

<div class="video-wrapper">
    {#if isLoading}
        <div class="loader-container">
            <div class="spinner"></div>
            <span>Łączenie z kamerą...</span>
        </div>
    {/if}

    <img
        src={videoStreamUrl}
        alt="Strumień wideo z kamery"
        class:hidden={isLoading}
        on:load={handleVideoLoad}
    />
</div>
